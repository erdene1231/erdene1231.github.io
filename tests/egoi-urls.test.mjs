import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {editorialDatabase} from './problem-editorial-fixture.mjs';
import {manifest,buildEgoiUrlJob,preflightSql} from '../tools/egoi_url_job.mjs';
import {parseCatalog} from '../problem-store.js';
const read=p=>JSON.parse(fs.readFileSync(p));
async function fixture(){
 const db=await editorialDatabase({installPriority:false});
 await db.exec(fs.readFileSync('supabase/proposals/036-new-problem-metadata-import.sql','utf8'));
 await db.exec(`create table tutorial_changes(id integer,body jsonb);create table tutorial_drafts(tutorial_id text,editor_id text,body jsonb);create table learning_records(user_id text,body jsonb);create table profiles(id text,name text);
 insert into tutorial_catalog values('mongolia','{"keep":true}',false);insert into tutorial_drafts values('mongolia','private','{"base":7}');insert into profiles values('fixture','Keep');insert into problem_sources values('EGOI');`);
 const base=read('problems.json').problems.find(p=>p.id==='egoi-2023-inflation');
 for(const m of [...manifest.matched,...manifest.unmatched]){
  const body={...base,id:m.id,number:m.number,title:m.catalog_title,ref:m.catalog_ref,url:m.before_url};
  await db.query('insert into problem_catalog(problem_id,number,body,revision) values($1,$2,$3,$4)',[m.id,m.number,body,m.revision]);
 }
 await db.query("insert into problem_catalog(problem_id,number,body) values('unrelated',2000,$1)",[{...base,id:'unrelated',number:2000,source:'Other'}]);
 await db.exec("select setval('problem_number_seq',2000,true)");return db;
}
const guard=async db=>(await db.query(preflightSql())).rows[0].recovery;
const rows=async db=>(await db.query('select * from problem_catalog order by number')).rows;
test('all identities map to verified individual pages; absent tasks stay separate and fallback changes only three URLs',()=>{
 assert.equal(manifest.listing.length,38);assert.equal(manifest.matched.length,36);assert.equal(manifest.unmatched.length,9);
 for(const m of manifest.matched){assert.ok(manifest.listing.some(l=>l.alias===m.alias&&l.year===m.year&&l.url===m.after_url));assert.equal(new URL(m.after_url).pathname,'/problem/view/'+m.alias);}
 assert.equal(manifest.matched.find(m=>m.id==='task-849').alias,'EGOI24_infiniterace2');
 const fallback=read('problems.json').problems;assert.equal(manifest.matched.filter(m=>fallback.some(p=>p.id===m.id)).length,3);
 for(const m of manifest.matched){const p=fallback.find(p=>p.id===m.id);if(p)assert.equal(p.url,m.after_url);}
 for(const m of manifest.unmatched){const p=fallback.find(p=>p.id===m.id);if(p)assert.equal(p.url,m.before_url);}
});
test('URL-only statement preserves identities, other fields, unmatched rows, protected data and edit history; refuses replay',async()=>{
 const db=await fixture();try{
  const g=await guard(db),before=await rows(db),sql=await buildEgoiUrlJob(g);await db.exec(sql);
  const after=await rows(db),h=(await db.query('select * from problem_changes order by change_id')).rows;
  assert.equal(h.length,36);assert.equal(after.length,before.length);assert.deepEqual((await guard(db)).protected,g.protected);assert.deepEqual((await guard(db)).authority,g.authority);assert.deepEqual((await guard(db)).sequence,g.sequence);
  for(const p of after){const b=before.find(b=>b.problem_id===p.problem_id),m=manifest.matched.find(m=>m.id===p.problem_id);
   if(!m){assert.deepEqual(p,b);continue;}
   assert.deepEqual(p.body,{...b.body,url:m.after_url});assert.equal(p.revision,b.revision+1);assert.equal(p.number,b.number);assert.equal(p.archived,b.archived);
   const edit=h.find(h=>h.problem_id===p.problem_id);assert.deepEqual(edit.previous_body,b.body);assert.deepEqual(edit.next_body,p.body);assert.equal(edit.action,'edit');assert.equal(edit.actor_id,null);
  }
  const catalog=parseCatalog({problems:after.map(p=>({...p.body,revision:p.revision})),knownIds:after.map(p=>p.problem_id)});assert.equal(catalog.problems.length,after.length);
  await assert.rejects(db.exec(sql),/Catalog baseline drift/);assert.deepEqual(await rows(db),after);
 }finally{await db.close();}
});
test('scope tampering, revisions, protected drift and a failure halfway roll back safely',async()=>{
 const db=await fixture();try{
  const g=await guard(db),before=await rows(db),sql=await buildEgoiUrlJob(g),changed=structuredClone(manifest);changed.matched[0].after_url='https://oj.uz/problems/source/egoi';await assert.rejects(buildEgoiUrlJob(g,changed),/allowlist differs/);
  await assert.rejects(db.exec(sql.replace('EGOI23_inflation','EGOI23_wrong')),/Allowlist differs/);
  await assert.rejects(db.exec(sql.replace('-- Atomic URL and corresponding edit history complete.',"IF cardinality(changed_ids)=18 THEN RAISE EXCEPTION 'Injected halfway failure'; END IF;")),/Injected halfway failure/);
  assert.deepEqual(await rows(db),before);assert.equal((await db.query('select count(*) n from problem_changes')).rows[0].n,0);
  await db.exec("update problem_catalog set revision=revision+1 where problem_id='task-119'");await assert.rejects(buildEgoiUrlJob(await guard(db)),/revision\/URL differs/);await assert.rejects(db.exec(sql),/Catalog baseline drift/);
  await db.exec("update problem_catalog set revision=revision-1 where problem_id='task-119';update profiles set name='Concurrent change'");await assert.rejects(db.exec(sql),/Protected state\/authority drift/);
 }finally{await db.close();}
});
