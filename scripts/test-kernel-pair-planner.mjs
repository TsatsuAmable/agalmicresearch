import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
function run(extra=[]){
 const r=spawnSync(process.execPath,['scripts/plan-kernel-pair.mjs','--task-id','fixture-task','--task-family','repository-change','--generator-family','fixture-model','--base-state','abc123','--task-spec-hash','taskhash','--verification-spec-hash','verifyhash','--pair-id','pair-fixed','--assignment-id','assign-fixed','--assignment-salt','secret-fixture',...extra],{encoding:'utf8'});
 if(r.status!==0) throw new Error(r.stderr||r.stdout); return JSON.parse(r.stdout);
}
const a=run(),b=run();
assert.deepEqual(a,b);
assert.equal(a.assignments.length,2);
assert.deepEqual(new Set(a.assignments.map(x=>x.condition)),new Set(['control','kernel']));
assert.equal(a.independence_level,'fresh-workspace');
assert.equal(a.base_state,'abc123');
assert.equal(a.admissibility.transcript_sharing_allowed,false);
assert.ok(a.assignments.every(x=>x.workspace_id));
console.log('kernel pair planner tests passed');
