import fs from 'node:fs';

const input = process.argv[2];
if (!input) {
  console.error('usage: node scripts/summarize-kernel-consequences.mjs <records.jsonl>');
  process.exit(2);
}

const lines = fs.readFileSync(input, 'utf8').split(/\r?\n/).filter(Boolean);
const rows = lines.map((line, i) => {
  try { return JSON.parse(line); }
  catch (err) { throw new Error(`Invalid JSON on line ${i + 1}: ${err.message}`); }
});

const required = ['pair_id','task_id','task_family','condition','human_minutes','verified_completion','rework_count','boundary_violations','downstream_failures'];
const allowed = new Set(['control','kernel']);
const pairs = new Map();

for (const row of rows) {
  for (const key of required) {
    if (row[key] === undefined || row[key] === null) throw new Error(`Missing ${key} in ${JSON.stringify(row)}`);
  }
  if (!allowed.has(row.condition)) throw new Error(`Unknown condition ${row.condition}`);
  for (const key of ['human_minutes','rework_count','boundary_violations','downstream_failures']) {
    if (!Number.isFinite(Number(row[key])) || Number(row[key]) < 0) throw new Error(`Invalid ${key} in pair ${row.pair_id}`);
  }
  if (typeof row.verified_completion !== 'boolean') throw new Error(`verified_completion must be boolean in pair ${row.pair_id}`);
  const p = pairs.get(row.pair_id) ?? {};
  if (p[row.condition]) throw new Error(`Duplicate ${row.condition} record in pair ${row.pair_id}`);
  p[row.condition] = row;
  pairs.set(row.pair_id, p);
}

const matched = [...pairs.entries()].filter(([,p]) => p.control && p.kernel);
const incomplete = [...pairs.entries()].filter(([,p]) => !(p.control && p.kernel)).map(([id]) => id);
if (!matched.length) throw new Error('No matched control/kernel pairs');

const diffs = matched.map(([pair_id,p]) => {
  if (p.control.task_family !== p.kernel.task_family) throw new Error(`task_family mismatch in pair ${pair_id}`);
  return {
    pair_id,
    task_id: p.control.task_id,
    task_family: p.control.task_family,
    human_minutes: Number(p.kernel.human_minutes) - Number(p.control.human_minutes),
    completion: Number(p.kernel.verified_completion) - Number(p.control.verified_completion),
    rework_count: Number(p.kernel.rework_count) - Number(p.control.rework_count),
    boundary_violations: Number(p.kernel.boundary_violations) - Number(p.control.boundary_violations),
    downstream_failures: Number(p.kernel.downstream_failures) - Number(p.control.downstream_failures),
  };
});

const summarize = xs => {
  const mean = key => xs.reduce((s,d) => s + d[key], 0) / xs.length;
  const median = key => {
    const ys = xs.map(d => d[key]).sort((a,b)=>a-b);
    const m = Math.floor(ys.length/2);
    return ys.length % 2 ? ys[m] : (ys[m-1] + ys[m]) / 2;
  };
  const signCounts = (key, favorable) => xs.reduce((acc,d) => {
    const v = d[key];
    if (v === 0) acc.tie++;
    else if ((favorable === 'negative' && v < 0) || (favorable === 'positive' && v > 0)) acc.favors_kernel++;
    else acc.favors_control++;
    return acc;
  }, {favors_kernel:0,favors_control:0,tie:0});

  return {
    n: xs.length,
    human_minutes: {mean:mean('human_minutes'),median:median('human_minutes'),signs:signCounts('human_minutes','negative')},
    completion: {mean:mean('completion'),median:median('completion'),signs:signCounts('completion','positive')},
    rework_count: {mean:mean('rework_count'),median:median('rework_count'),signs:signCounts('rework_count','negative')},
    boundary_violations: {mean:mean('boundary_violations'),median:median('boundary_violations'),signs:signCounts('boundary_violations','negative')},
    downstream_failures: {mean:mean('downstream_failures'),median:median('downstream_failures'),signs:signCounts('downstream_failures','negative')}
  };
};

const families = [...new Set(diffs.map(d=>d.task_family))].sort();
const byFamily = Object.fromEntries(families.map(f => [f, summarize(diffs.filter(d=>d.task_family===f))]));

console.log(JSON.stringify({
  matched_pairs: diffs.length,
  incomplete_pairs: incomplete,
  task_family_count: families.length,
  interpretation: {
    human_minutes_delta: 'negative favors kernel',
    completion_delta: 'positive favors kernel',
    rework_delta: 'negative favors kernel',
    boundary_violations_delta: 'negative favors kernel',
    downstream_failures_delta: 'negative favors kernel'
  },
  overall: summarize(diffs),
  by_task_family: byFamily,
  claim_status: diffs.length < 5
    ? 'descriptive-only: fewer than 5 matched pairs'
    : 'descriptive pilot: inferential claims are not authorized by pilot manifest',
  pairs: diffs
}, null, 2));
