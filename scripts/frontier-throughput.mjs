import fs from 'node:fs';
import path from 'node:path';

const file = process.argv[2] ?? 'research/frontier_throughput/events.jsonl';
const raw = fs.readFileSync(file, 'utf8').split(/\r?\n/).filter(Boolean);
const events = raw.map((line, i) => {
  try { return JSON.parse(line); }
  catch (err) { throw new Error(`Invalid JSON on line ${i + 1}: ${err.message}`); }
});

const stages = ['generate','select','validate','realize','assimilate'];
const allowedTypes = new Set(['entered','completed','disposition','human_attention','machine_effort']);
const allowedActors = new Set(['human','machine','hybrid']);
const byStage = new Map(stages.map(s => [s, { entered: 0, completed: 0, human_minutes: 0, machine_minutes: 0, dispositions: {} }]));
const seen = new Set();

for (const e of events) {
  for (const key of ['event_id','candidate_id','timestamp','stage','event_type','actor']) {
    if (e[key] == null || e[key] === '') throw new Error(`Missing ${key} in event ${JSON.stringify(e)}`);
  }
  if (seen.has(e.event_id)) throw new Error(`Duplicate event_id: ${e.event_id}`);
  seen.add(e.event_id);
  if (!byStage.has(e.stage)) throw new Error(`Unknown stage: ${e.stage}`);
  if (!allowedTypes.has(e.event_type)) throw new Error(`Unknown event_type: ${e.event_type}`);
  if (!allowedActors.has(e.actor)) throw new Error(`Unknown actor: ${e.actor}`);
  if (Number.isNaN(Date.parse(e.timestamp))) throw new Error(`Invalid timestamp: ${e.timestamp}`);

  const s = byStage.get(e.stage);
  if (e.event_type === 'entered') s.entered++;
  if (e.event_type === 'completed') s.completed++;
  if (e.event_type === 'human_attention') s.human_minutes += Number(e.minutes ?? 0);
  if (e.event_type === 'machine_effort') s.machine_minutes += Number(e.minutes ?? 0);
  if (e.event_type === 'disposition') s.dispositions[e.disposition] = (s.dispositions[e.disposition] ?? 0) + 1;
}

console.log(JSON.stringify({
  source: path.normalize(file),
  event_count: events.length,
  candidate_count: new Set(events.map(e => e.candidate_id)).size,
  stages: Object.fromEntries([...byStage]),
}, null, 2));
