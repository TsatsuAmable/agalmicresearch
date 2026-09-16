import fs from 'node:fs';
import crypto from 'node:crypto';

const args=process.argv.slice(2);
const get=n=>{const i=args.indexOf(`--${n}`); return i>=0?args[i+1]:undefined;};
const required=['task-id','task-family','generator-family','base-state','task-spec-hash','verification-spec-hash'];
for(const k of required) if(!get(k)) throw new Error(`missing --${k}`);
const families=new Set(['research-synthesis','repository-change','benchmark-or-analysis','publication-or-documentation']);
if(!families.has(get('task-family'))) throw new Error('unknown task family');

const pairId=get('pair-id') ?? crypto.randomUUID();
const assignmentId=get('assignment-id') ?? crypto.randomUUID();
const salt=get('assignment-salt') ?? crypto.randomBytes(16).toString('hex');
const digest=crypto.createHash('sha256').update([pairId,assignmentId,get('base-state'),get('task-spec-hash'),salt].join('|')).digest('hex');
const kernelFirst=parseInt(digest.slice(0,8),16)%2===0;
const instances=['A','B'];
const conditions=kernelFirst?['kernel','control']:['control','kernel'];
const plan={
 schema_version:'0.1',
 pair_id:pairId,
 assignment_id:assignmentId,
 task_id:get('task-id'),
 task_family:get('task-family'),
 generator_family:get('generator-family'),
 generator_version:get('generator-version') ?? '',
 base_state:get('base-state'),
 task_spec_hash:get('task-spec-hash'),
 verification_spec_hash:get('verification-spec-hash'),
 independence_level:get('independence-level') ?? (get('task-family')==='repository-change'?'fresh-workspace':'fresh-agent-context'),
 assignment_method:'sha256(pair_id|assignment_id|base_state|task_spec_hash|secret_salt) parity',
 assignment_commitment:crypto.createHash('sha256').update(salt).digest('hex'),
 assignments:instances.map((instance,i)=>({instance,condition:conditions[i],context_id:`${pairId}-${instance}`,workspace_id:get('task-family')==='repository-change'?`${pairId}-workspace-${instance}`:null})),
 admissibility:{
   immutable_task_spec:true,
   immutable_verification_spec:true,
   shared_pinned_base_state:true,
   transcript_sharing_allowed:false,
   intermediate_artifact_sharing_allowed:false,
   outcome_visible_before_pair_complete:false
 }
};
const out=get('out');
if(out){fs.mkdirSync(new URL('.',`file://${process.cwd()}/${out}`).pathname,{recursive:true});fs.writeFileSync(out,JSON.stringify(plan,null,2)+'\n');}
console.log(JSON.stringify(plan,null,2));
