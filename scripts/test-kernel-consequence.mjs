import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const dir = fs.mkdtempSync(path.join(os.tmpdir(),'agalmic-kernel-consequence-'));
const file = path.join(dir,'records.jsonl');

function run(args) {
  const r = spawnSync(process.execPath,args,{encoding:'utf8'});
  if (r.status !== 0) throw new Error(r.stderr || r.stdout);
  return r.stdout;
}

const common = [
  '--file',file,
  '--pair-id','pair-001',
  '--task-id','task-001',
  '--task-family','research-synthesis',
  '--generator-family','test-family',
  '--started-at','2026-09-14T08:00:00Z',
  '--completed-at','2026-09-14T08:10:00Z',
  '--rework-count','0',
  '--boundary-violations','0',
  '--downstream-failures','0',
  '--verification-method','fixture-check',
  '--independence-level','fresh-agent-context',
  '--base-state','fixture-base-sha',
  '--assignment-id','assignment-001',
  '--evidence','fixture://verified'
];

run(['scripts/record-kernel-consequence.mjs',...common,'--record-id','control-001','--condition','control','--human-minutes','8','--verified-completion','true']);
run(['scripts/record-kernel-consequence.mjs',...common,'--record-id','kernel-001','--condition','kernel','--human-minutes','5','--verified-completion','true']);

const lines = fs.readFileSync(file,'utf8').trim().split(/\r?\n/);
assert.equal(lines.length,2);

const summary = JSON.parse(run(['scripts/summarize-kernel-consequences.mjs',file]));
assert.equal(summary.matched_pairs,1);
assert.equal(summary.task_family_count,1);
assert.equal(summary.overall.human_minutes.mean,-3);
assert.equal(summary.overall.human_minutes.signs.favors_kernel,1);
assert.match(summary.claim_status,/descriptive-only/);

const duplicate = spawnSync(process.execPath,['scripts/record-kernel-consequence.mjs',...common,'--record-id','kernel-002','--condition','kernel','--human-minutes','4','--verified-completion','true'],{encoding:'utf8'});
assert.notEqual(duplicate.status,0);
assert.match(duplicate.stderr + duplicate.stdout,/already has condition kernel/);

console.log('kernel consequence capture tests passed');
