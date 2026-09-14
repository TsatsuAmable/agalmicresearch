import fs from 'node:fs';
import crypto from 'node:crypto';

const args = process.argv.slice(2);
const get = name => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const has = name => args.includes(`--${name}`);

const file = get('file') ?? 'research/cognitive_kernel/data/consequence-records.jsonl';
const required = ['pair-id','task-id','task-family','generator-family','condition','started-at','completed-at','human-minutes','verified-completion','rework-count','boundary-violations','downstream-failures','verification-method'];
for (const key of required) {
  if (get(key) === undefined) {
    console.error(`missing --${key}`);
    process.exit(2);
  }
}

const parseBool = (value, key) => {
  if (value === 'true') return true;
  if (value === 'false') return false;
  throw new Error(`--${key} must be true or false`);
};
const parseNonNegative = (value, key, integer=false) => {
  const n = Number(value);
  if (!Number.isFinite(n) || n < 0 || (integer && !Number.isInteger(n))) throw new Error(`--${key} must be a non-negative ${integer ? 'integer' : 'number'}`);
  return n;
};

const taskFamilies = new Set(['research-synthesis','repository-change','benchmark-or-analysis','publication-or-documentation']);
const conditions = new Set(['control','kernel']);
const taskFamily = get('task-family');
const condition = get('condition');
if (!taskFamilies.has(taskFamily)) throw new Error(`unknown task family: ${taskFamily}`);
if (!conditions.has(condition)) throw new Error(`unknown condition: ${condition}`);

for (const [key,value] of [['started-at',get('started-at')],['completed-at',get('completed-at')]]) {
  if (Number.isNaN(Date.parse(value))) throw new Error(`--${key} must be an ISO date-time`);
}
if (Date.parse(get('completed-at')) < Date.parse(get('started-at'))) throw new Error('completed-at precedes started-at');

const evidence = args.flatMap((value, i) => value === '--evidence' && args[i+1] ? [args[i+1]] : []);
if (!evidence.length) throw new Error('at least one --evidence is required');

const record = {
  record_id: get('record-id') ?? crypto.randomUUID(),
  pair_id: get('pair-id'),
  task_id: get('task-id'),
  task_family: taskFamily,
  generator_family: get('generator-family'),
  generator_version: get('generator-version') ?? '',
  condition,
  started_at: get('started-at'),
  completed_at: get('completed-at'),
  human_minutes: parseNonNegative(get('human-minutes'),'human-minutes'),
  verified_completion: parseBool(get('verified-completion'),'verified-completion'),
  rework_count: parseNonNegative(get('rework-count'),'rework-count',true),
  boundary_violations: parseNonNegative(get('boundary-violations'),'boundary-violations',true),
  downstream_failures: parseNonNegative(get('downstream-failures'),'downstream-failures',true),
  verification_method: get('verification-method'),
  evidence,
  notes: get('notes') ?? ''
};

if (fs.existsSync(file)) {
  const lines = fs.readFileSync(file,'utf8').split(/\r?\n/).filter(Boolean);
  const prior = lines.map((line,i) => {
    try { return JSON.parse(line); }
    catch (err) { throw new Error(`invalid existing JSON on line ${i+1}: ${err.message}`); }
  });
  if (prior.some(x => x.record_id === record.record_id)) throw new Error(`duplicate record_id: ${record.record_id}`);
  if (prior.some(x => x.pair_id === record.pair_id && x.condition === record.condition)) throw new Error(`pair ${record.pair_id} already has condition ${record.condition}`);
}

fs.mkdirSync(new URL('.', `file://${process.cwd()}/${file}`).pathname, {recursive:true});
fs.appendFileSync(file, JSON.stringify(record) + '\n');
console.log(JSON.stringify(record, null, 2));
