import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {editorialDatabase} from './problem-editorial-fixture.mjs';
import {buildAtcoderJob,preflightSql,statementPatches,abcAdditions} from '../tools/atcoder_catalog_job.mjs';
import {validateProblem,parseCatalog} from '../problem-store.js';
import {assertProblemSelectionReady} from '../problem-content-policy.js';
const original=JSON.parse(fs.readFileSync('audit/atcoder-expansion/before-targets.json'));
async function fixture(){
 const db=await editorialDatabase({installPriority:false});await db.exec(fs.readFileSync('supabase/proposals/036-new-problem-metadata-import.sql','utf8'));await db.exec(fs.readFileSync('supabase/038-native-inline-problem-statements.sql','utf8'));
 await db.exec(`create table tutorial_changes(id integer,body jsonb);create table tutorial_drafts(tutorial_id text,editor_id text,body jsonb);create table learning_records(user_id text,body jsonb);create table profiles(id text,name text);insert into tutorial_catalog values('mongolia','{"keep":true}',false);insert into tutorial_drafts values('mongolia','private','{"base":7}');insert into profiles values('fixture','Keep');insert into problem_sources values('AtCoder');`);
 for(const p of original)await db.query('insert into problem_catalog(problem_id,number,body,revision,archived,updated_at)values($1,$2,$3,$4,$5,$6)',[p.problem_id,p.number,p.body,p.revision,p.archived,p.updated_at]);
 await db.query("insert into problem_catalog(problem_id,number,body)values('unrelated',1,$1)",[{...original[0].body,id:'unrelated',number:1,source:'Other',ref:'keep',url:'https://example.org/keep'}]);
 await db.exec("select setval('problem_number_seq',1010,true)");return db;
}
const guard=async db=>(await db.query(preflightSql())).rows[0].recovery;
const snap=async db=>({catalog:(await db.query('select * from problem_catalog order by number')).rows,history:(await db.query('select * from problem_changes order by change_id')).rows,protected:(await guard(db)).protected,authority:(await guard(db)).authority});
test('54 individually verified English ABC records have justified metadata, global task identities and no statement/editorial fabrication',()=>{
 assert.equal(abcAdditions.length,54);assert.equal(new Set(abcAdditions.map(p=>p.canonical_task_id)).size,54);
 for(const p of abcAdditions){assertProblemSelectionReady(p.body);validateProblem(p.body);assert.equal(p.body.ratingKind,'estimated');assert.equal(p.body.ratingSource,p.source_url);assert.equal(new URL(p.body.url).pathname.split('/').at(-1),p.canonical_task_id);assert.equal(p.english_available,true);assert.equal('statement'in p.body,false);assert.equal('editorial'in p.body,false);}
 assert.equal(abcAdditions.find(p=>p.selection_key==='abc086_c').canonical_task_id,'arc089_a');
});
test('atomic AtCoder job edits exactly51 native statements and allocates54 new ABC rows with exact field/history preservation and no replay',async()=>{
 const db=await fixture();try{
  const g=await guard(db),before=await snap(db),sql=await buildAtcoderJob(g);await db.exec(sql);const after=await snap(db);
  assert.equal(after.catalog.length,before.catalog.length+54);assert.equal(after.history.length,before.history.length+105);assert.deepEqual(after.protected,before.protected);assert.deepEqual(after.authority,before.authority);
  for(const b of before.catalog){const a=after.catalog.find(p=>p.problem_id===b.problem_id),patch=statementPatches.find(p=>p.id===b.problem_id);if(!patch){assert.deepEqual(a,b);continue;}assert.deepEqual(a.body,{...b.body,statement:patch.statement,statementProvenance:patch.statementProvenance});assert.equal(a.revision,b.revision+1);assert.deepEqual({...a,body:b.body,revision:b.revision,updated_at:b.updated_at},b);}
  const added=after.catalog.filter(p=>!before.catalog.some(b=>b.problem_id===p.problem_id));assert.equal(added.length,54);
  for(const p of added){const m=abcAdditions.find(r=>r.body.ref===p.body.ref);assert.ok(m);assert.equal(p.problem_id,'task-'+p.number);assert.equal(p.revision,1);assert.equal(p.archived,false);const{id,number,pack,...metadata}=p.body;assert.deepEqual(metadata,m.body);assert.equal(id,p.problem_id);assert.equal(number,p.number);}
  assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,1064);
  assert.equal(parseCatalog((await db.query('select get_catalog()r')).rows[0].r).problems.filter(p=>p.hasStatement).length,51);
  await assert.rejects(db.exec(sql),/Catalog baseline drift/);assert.deepEqual(await snap(db),after);
 }finally{await db.close();}
});
test('allowlist, native revisions, canonical mirror conflicts, protected drift and late failures fail safely without recycling allocator gaps',async()=>{
 const db=await fixture();try{
  let g=await guard(db);const before=await snap(db),sql=await buildAtcoderJob(g),changed=structuredClone(abcAdditions);changed[0].body.rating=4000;await assert.rejects(buildAtcoderJob(g,statementPatches,changed),/allowlist differs/);
  await assert.rejects(db.exec(sql.replace('AtCoder ABC081 B','AtCoder WRONG B')),/Reviewed plan differs/);
  const duplicate=structuredClone(g);duplicate.problems.push({...g.problems[0],problem_id:'mirror',body:{...g.problems[0].body,ref:'different-ref',url:'https://atcoder.jp/contests/arc089/tasks/arc089_a?lang=ja'}});await assert.rejects(buildAtcoderJob(duplicate),/canonical task duplicate/);
  await db.exec("update problem_catalog set revision=revision+1 where problem_id='task-749'");await assert.rejects(buildAtcoderJob(await guard(db)),/target CAS differs/);await db.exec("update problem_catalog set revision=revision-1 where problem_id='task-749';update profiles set name='Concurrent'");await assert.rejects(db.exec(sql),/Protected state\/authority drift/);await db.exec("update profiles set name='Keep'");
  await assert.rejects(db.exec(sql.replace('-- Atomic ABC create and history complete.',"IF cardinality(created_ids)=17 THEN RAISE EXCEPTION 'Injected create failure'; END IF;")),/Injected create failure/);assert.deepEqual(await snap(db),before);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,1027);await assert.rejects(db.exec(sql),/Sequence\/source drift/);
  g=await guard(db);const later=await buildAtcoderJob(g);await assert.rejects(db.exec(later.replace('-- Atomic native statement edit and history complete.',"IF cardinality(edited_ids)=25 THEN RAISE EXCEPTION 'Injected statement failure'; END IF;")),/Injected statement failure/);assert.deepEqual(await snap(db),before);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,1081);
 }finally{await db.close();}
});
