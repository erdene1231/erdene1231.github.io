import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {editorialDatabase} from './problem-editorial-fixture.mjs';
import {proposalProblems} from '../tools/package02_tutorial_proposals.mjs';
import {complexityPrioritySql,searchSortPrioritySql,recursionPrioritySql,differencePointersPrioritySql,windowPrioritySql,stackPrioritySql,bitsPrioritySql} from '../tools/package02_priority_promotions.mjs';
const plan=JSON.parse(fs.readFileSync('audit/PACKAGE02-COMPLEXITY-PRIORITY-PROMOTIONS.json'));
async function setup(){
 const db=await editorialDatabase({installPriority:false});
 await db.exec(JSON.parse(fs.readFileSync('supabase/audit/production-after-031.json')).functions.find(f=>f.name==='is_admin').definition);
 await db.exec(fs.readFileSync('supabase/proposals/036-new-problem-metadata-import.sql','utf8'));
 for(const body of proposalProblems())await db.query('insert into problem_catalog(problem_id,number,body,revision,archived) values($1,$2,$3,1,false)',[body.id,body.number,body]);
 await db.query("select setval('problem_number_seq',993,true)");return db;
}
async function guard(db){return{
 problems:(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number in(299,301) order by number")).rows,
 functions:(await db.query("select p.oid::regprocedure::text signature,md5(pg_get_functiondef(p.oid)) definition_md5,p.proacl::text acl from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in('validate_learning_problem','validate_priority_metadata') order by p.proname")).rows,
 problem_count:993,sequence:{last_value:993,is_called:true},catalog_triggers:null,
 non_target_fingerprint:(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id not in('cses-1083','cses-1094')")).rows[0].h,
 history_fingerprint:(await db.query("select md5(coalesce(jsonb_agg(to_jsonb(h) order by change_id::text)::text,'[]')) h from problem_changes h")).rows[0].h
};}
test('two core-practice promotions preserve every unrelated field/record, progress and authority; stale/tampered/replayed jobs fail',async()=>{
 const db=await setup();try{
  const snapshot=async()=>({catalog:(await db.query('select * from problem_catalog order by number')).rows,history:(await db.query('select * from problem_changes order by change_id::text')).rows,progress:(await db.query('select * from progress')).rows,sequence:(await db.query('select last_value,is_called from problem_number_seq')).rows});
  const before=await snapshot(),g=await guard(db),sql=complexityPrioritySql(plan,g);
  assert.throws(()=>complexityPrioritySql({...plan,patches:[{...plan.patches[0],changes:{...plan.patches[0].changes,rating:999}},plan.patches[1]]},g),/Only justified/);
  assert.throws(()=>complexityPrioritySql({...plan,patches:[plan.patches[0]]},g),/Only the reviewed/);
  await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected priority failure';")),/Injected priority failure/);assert.deepEqual(await snapshot(),before);
  await db.query('update problem_catalog set revision=revision+1 where number=301');await assert.rejects(db.exec(sql),/Priority CAS\/body drift/);await db.query('update problem_catalog set revision=revision-1 where number=301');
  assert.deepEqual((await snapshot()).catalog,before.catalog);
  await db.exec(sql);const after=await snapshot();
  assert.deepEqual(after.progress,before.progress);assert.deepEqual(after.sequence,before.sequence);assert.equal(after.history.length,before.history.length+2);
  assert.deepEqual(after.catalog.filter(r=>![299,301].includes(r.number)),before.catalog.filter(r=>![299,301].includes(r.number)));
  for(const patch of plan.patches){const old=before.catalog.find(r=>r.problem_id===patch.id),now=after.catalog.find(r=>r.problem_id===patch.id);assert.deepEqual(now.body,{...old.body,...patch.changes});assert.equal(now.revision,old.revision+1);assert.equal(now.archived,old.archived);assert.equal(now.number,old.number);}
  assert.equal((await db.query('select is_admin() value')).rows[0].value,false);
  await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS\/body drift/);assert.deepEqual(await snapshot(),after);
 }finally{await db.close();}
});


test('search/sort promotion scope is separate, justified and preserves all other tasks',async()=>{
 const db=await setup();try{
  const nextPlan=JSON.parse(fs.readFileSync('audit/PACKAGE02-SEARCH-SORT-PRIORITY-PROMOTIONS.json'));
  const g=await guard(db);g.problems=(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number in(85,312) order by number")).rows;g.non_target_fingerprint=(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id not in('cses-1623','cses-1621')")).rows[0].h;
  assert.throws(()=>complexityPrioritySql(nextPlan,g),/Only the reviewed/);assert.throws(()=>searchSortPrioritySql(plan,g),/Only the reviewed/);
  const before=(await db.query('select * from problem_catalog order by number')).rows,sql=searchSortPrioritySql(nextPlan,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected search/sort priority failure';")),/Injected search\/sort priority failure/);assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
  await db.exec(sql);const after=(await db.query('select * from problem_catalog order by number')).rows;
  assert.deepEqual(after.filter(r=>![85,312].includes(r.number)),before.filter(r=>![85,312].includes(r.number)));
  for(const patch of nextPlan.patches){const old=before.find(r=>r.problem_id===patch.id),now=after.find(r=>r.problem_id===patch.id);assert.deepEqual(now.body,{...old.body,...patch.changes});assert.equal(now.revision,old.revision+1);}
  assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,993);
  await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS\/body drift/);
 }finally{await db.close();}
});

test('one Hanoi core promotion is atomic and cannot spill into previous two-target scopes',async()=>{
 const db=await setup();try{
  const p=JSON.parse(fs.readFileSync('audit/PACKAGE02-RECURSION-PRIORITY-PROMOTIONS.json')),g=await guard(db);
  g.problems=(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number=22")).rows;
  g.non_target_fingerprint=(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id<>'cses-2165'")).rows[0].h;
  assert.throws(()=>complexityPrioritySql(p,g),/Only the reviewed/);assert.throws(()=>recursionPrioritySql(plan,g),/Only the reviewed/);
  const before=(await db.query('select * from problem_catalog order by number')).rows,sql=recursionPrioritySql(p,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected Hanoi failure';")),/Injected Hanoi failure/);
  assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
  await db.exec(sql);const after=(await db.query('select * from problem_catalog order by number')).rows;
  assert.deepEqual(after.filter(r=>r.number!==22),before.filter(r=>r.number!==22));
  const old=before.find(r=>r.number===22),now=after.find(r=>r.number===22);assert.deepEqual(now.body,{...old.body,...p.patches[0].changes});assert.equal(now.revision,2);
  assert.equal((await db.query('select count(*) n from problem_changes')).rows[0].n,1);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,993);
  await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS\/body drift/);
 }finally{await db.close();}
});


test('difference/pointer scope promotes only two reviewed direct core tasks',async()=>{
 const db=await setup();try{
 const p=JSON.parse(fs.readFileSync('audit/PACKAGE02-DIFFERENCE-POINTERS-PRIORITY.json')),g=await guard(db);g.problems=(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number in(316,318) order by number")).rows;g.non_target_fingerprint=(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id not in('cses-1619','cses-1640')")).rows[0].h;
 const before=(await db.query('select * from problem_catalog order by number')).rows,sql=differencePointersPrioritySql(p,g);assert.throws(()=>recursionPrioritySql(p,g),/Only the reviewed/);await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected core failure';")),/Injected core failure/);assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);await db.exec(sql);const after=(await db.query('select * from problem_catalog order by number')).rows;assert.deepEqual(after.filter(r=>![316,318].includes(r.number)),before.filter(r=>![316,318].includes(r.number)));for(const patch of p.patches){const old=before.find(r=>r.number===patch.number),now=after.find(r=>r.number===patch.number);assert.deepEqual(now.body,{...old.body,...patch.changes});assert.equal(now.revision,old.revision+1);}await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS/);
 }finally{await db.close();}
});

test('one positive-window core promotion is atomic and cannot spill into previous two-target scopes',async()=>{
 const db=await setup();try{
  const p=JSON.parse(fs.readFileSync('audit/PACKAGE02-WINDOW-PRIORITY.json')),g=await guard(db);
  g.problems=(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number=334")).rows;
  g.non_target_fingerprint=(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id<>'cses-1660'")).rows[0].h;
  assert.throws(()=>complexityPrioritySql(p,g),/Only the reviewed/);assert.throws(()=>windowPrioritySql(plan,g),/Only the reviewed/);
  const before=(await db.query('select * from problem_catalog order by number')).rows,sql=windowPrioritySql(p,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected window failure';")),/Injected window failure/);
  assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
  await db.exec(sql);const after=(await db.query('select * from problem_catalog order by number')).rows;
  assert.deepEqual(after.filter(r=>r.number!==334),before.filter(r=>r.number!==334));
  const old=before.find(r=>r.number===334),now=after.find(r=>r.number===334);assert.deepEqual(now.body,{...old.body,...p.patches[0].changes});assert.equal(now.revision,2);
  assert.equal((await db.query('select count(*) n from problem_changes')).rows[0].n,1);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,993);
  await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS\/body drift/);
 }finally{await db.close();}
});

test('one monotonic-stack core promotion is atomic and cannot spill into previous two-target scopes',async()=>{
 const db=await setup();try{
  const p=JSON.parse(fs.readFileSync('audit/PACKAGE02-STACK-PRIORITY.json')),g=await guard(db);
  g.problems=(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number=101")).rows;
  g.non_target_fingerprint=(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id<>'task-101'")).rows[0].h;
  assert.throws(()=>complexityPrioritySql(p,g),/Only the reviewed/);assert.throws(()=>windowPrioritySql(plan,g),/Only the reviewed/);
  const before=(await db.query('select * from problem_catalog order by number')).rows,sql=stackPrioritySql(p,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected stack failure';")),/Injected stack failure/);
  assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
  await db.exec(sql);const after=(await db.query('select * from problem_catalog order by number')).rows;
  assert.deepEqual(after.filter(r=>r.number!==101),before.filter(r=>r.number!==101));
  const old=before.find(r=>r.number===101),now=after.find(r=>r.number===101);assert.deepEqual(now.body,{...old.body,...p.patches[0].changes});assert.equal(now.revision,2);
  assert.equal((await db.query('select count(*) n from problem_changes')).rows[0].n,1);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,993);
  await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS\/body drift/);
 }finally{await db.close();}
});

test('one Gray-code core promotion is atomic and cannot spill into previous two-target scopes',async()=>{
 const db=await setup();try{
  const p=JSON.parse(fs.readFileSync('audit/PACKAGE02-BITS-PRIORITY.json')),g=await guard(db);
  g.problems=(await db.query("select *,md5(body::text) body_md5 from problem_catalog where number=304")).rows;
  g.non_target_fingerprint=(await db.query("select md5(jsonb_agg(to_jsonb(p) order by problem_id)::text) h from problem_catalog p where problem_id<>'cses-2205'")).rows[0].h;
  assert.throws(()=>complexityPrioritySql(p,g),/Only the reviewed/);assert.throws(()=>windowPrioritySql(plan,g),/Only the reviewed/);
  const before=(await db.query('select * from problem_catalog order by number')).rows,sql=bitsPrioritySql(p,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic priority target and edit history complete.',"raise exception 'Injected Gray failure';")),/Injected Gray failure/);
  assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
  await db.exec(sql);const after=(await db.query('select * from problem_catalog order by number')).rows;
  assert.deepEqual(after.filter(r=>r.number!==304),before.filter(r=>r.number!==304));
  const old=before.find(r=>r.number===304),now=after.find(r=>r.number===304);assert.deepEqual(now.body,{...old.body,...p.patches[0].changes});assert.equal(now.revision,2);
  assert.equal((await db.query('select count(*) n from problem_changes')).rows[0].n,1);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,993);
  await assert.rejects(db.exec(sql),/Problem history drift|Priority CAS\/body drift/);
 }finally{await db.close();}
});
