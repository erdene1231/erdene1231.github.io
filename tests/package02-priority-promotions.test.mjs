import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {editorialDatabase} from './problem-editorial-fixture.mjs';
import {proposalProblems} from '../tools/package02_tutorial_proposals.mjs';
import {complexityPrioritySql} from '../tools/package02_priority_promotions.mjs';
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
  assert.throws(()=>complexityPrioritySql({...plan,patches:[plan.patches[0]]},g),/Only the two/);
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
