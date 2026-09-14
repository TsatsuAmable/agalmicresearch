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

const required = ['pair_id','task_id','condition','human_minutes','verified_completion','rework_count','boundary_violations','downstream_failures'];
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

const diffs = matched.map(([pair_id,p]) => ({
  pair_id,
  task_id: p.control.task_id,
  human_minutes: Number(p.kernel.human_minutes) - Number(p.control.human_minutes),
  completion: Number(p.kernel.verified_completion) - Number(p.control.verified_completion),
  rework_count: Number(p.kernel.rework_count) - Number(p.control.rework_count),
  boundary_violations: Number(p.kernel.boundary_violations) - Number(p.control.boundary_violations),
  downstream_failures: Number(p.kernel.downstream_failures) - Number(p.control.downstream_failures),
}));

const mean = key => diffs.reduce((s,d) => s + d[key], 0) / diffs.length;
const median = key => {
  const xs = diffs.map(d => d[key]).sort((a,b)=>a-b);
  const m = Math.floor(xs.length/2);
  return xs.length % 2 ? xs[m] : (xs[m-1] + xs[m]) / 2;
};

console.log(JSON.stringify({
  matched_pairs: diffs.length,
  incomplete_pairs: incomplete,
  interpretation: {
    human_minutes_delta: 'negative favors kernel',
    completion_delta: 'positive favors kernel',
    rework_delta: 'negative favors kernel',
    boundary_violations_delta: 'negative favors kernel',
    downstream_failures_delta: 'negative favors kernel'
  },
  paired_delta_summary: {
    human_minutes: { mean: mean('human_minutes'), median: median('human_minutes') },
    completion: { mean: mean('completion'), median: median('completion') },
    rework_count: { mean: mean('rework_count'), median: median('rework_count') },
    boundary_violations: { mean: mean('boundary_violations'), median: median('boundary_violations') },
    downstream_failures: { mean: mean('downstream_failures'), median: median('downstream_failures') }
  },
  claim_status: diffs.length < 5
    ? 'descriptive-only: fewer than 5 matched pairs'
    : 'descriptive: inferential claims require a pre-specified analysis plan',
  pairs: diffs
}, null, 2));
