import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {editorialDatabase} from './problem-editorial-fixture.mjs';
import {assertProblemStatementReady} from '../problem-statement-policy.js';
import {validateProblem,parseCatalog} from '../problem-store.js';
import {problemBackend,readProblemStatement,requireInlineStatementBackend} from '../problem-backend.js';
const patches=JSON.parse(fs.readFileSync('audit/atcoder-expansion/statement-patches.json'));
const migration=fs.readFileSync('supabase/038-native-inline-problem-statements.sql','utf8');
const admin='00000000-0000-0000-0000-000000000001';
const oldNames=['validate_learning_problem','admin_save_problem','get_catalog','get_admin_catalog'];
const acl=async db=>(await db.query("select proname,proacl::text from pg_proc where proname=any($1) order by proname",[oldNames])).rows;
async function fixture(){
 const db=await editorialDatabase({installPriority:false});await db.exec(fs.readFileSync('supabase/proposals/036-new-problem-metadata-import.sql','utf8'));
 await db.query('insert into admin_accounts values($1)',[admin]);await db.exec("insert into problem_sources values('AtCoder');grant select on problem_catalog to anon,authenticated;alter table problem_catalog enable row level security;create policy read_catalog on problem_catalog for select to anon,authenticated using(not archived or public.is_admin());");
 const base=JSON.parse(fs.readFileSync('problems.json')).problems.find(p=>p.id==='egoi-2023-inflation');
 for(const p of patches)await db.query('insert into problem_catalog(problem_id,number,body,revision)values($1,$2,$3,$4)',[p.id,p.number,{...base,id:p.id,number:p.number,source:'AtCoder',ref:p.ref,title:p.title,url:p.source_url},p.expected_revision]);
 await db.exec("select setval('problem_number_seq',1010,true)");return db;
}
test('51 bilingual documents use actual tutorial schema, exact bilingual samples and source/rights provenance',()=>{
 assert.equal(patches.length,51);assert.equal(new Set(patches.map(p=>p.id)).size,51);
 for(const p of patches){assertProblemStatementReady(p);const normalized=validateProblem({title:p.title,source:'AtCoder',ref:p.ref,url:p.source_url,rating:1400,ratingKind:'estimated',priority:false,tags:['implementation'],...p});assert.deepEqual(normalized.statement,p.statement);assert.equal(p.statementProvenance.rightsBasis,'original-functional-restatement');assert.equal(p.statementProvenance.sourceSha256,p.source_html_sha256);assert.equal(p.statement.sections.length>=5,true);}
});
test('minimal migration changes no data or existing ACLs; actual admin save/lazy catalog retain native documents, CAS and history',async()=>{
 const db=await fixture();try{
  const before=(await db.query('select * from problem_catalog order by number')).rows,grants=await acl(db);await db.exec(migration);assert.deepEqual(await acl(db),grants);assert.deepEqual((await db.query('select * from problem_catalog order by number')).rows,before);
  await db.query("select set_config('request.jwt.claim.sub',$1,false)",[admin]);
  for(const p of patches){const body=before.find(r=>r.problem_id===p.id).body,saved=(await db.query('select admin_save_problem($1,$2,$3) r',[{...body,statement:p.statement,statementProvenance:p.statementProvenance},p.number,p.expected_revision])).rows[0].r;assert.deepEqual(saved.statement,p.statement);assert.equal(saved.revision,p.expected_revision+1);}
  const catalog=(await db.query('select get_catalog() r')).rows[0].r;assert.equal(catalog.problems.filter(p=>p.hasStatement).length,51);assert.ok(catalog.problems.every(p=>!p.statement&&!p.statementProvenance));assert.equal(parseCatalog(catalog).problems.length,51);
  assert.equal((await db.query('select count(*) n from problem_changes')).rows[0].n,51);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,1010);
  const p=patches[0],row=(await db.query('select * from problem_catalog where problem_id=$1',[p.id])).rows[0];await assert.rejects(db.query('select admin_save_problem($1,$2,$3)',[row.body,p.number,p.expected_revision]),e=>e.code==='40001');
  const metadata={...row.body,title:row.body.title+' edited'};delete metadata.statement;delete metadata.statementProvenance;let saved=(await db.query('select admin_save_problem($1,$2,$3)r',[metadata,p.number,row.revision])).rows[0].r;assert.deepEqual(saved.statement,p.statement);
  saved=(await db.query('select admin_save_problem($1,$2,$3)r',[{...saved,statement:null,statementProvenance:null},p.number,saved.revision])).rows[0].r;assert.equal('statement'in saved,false);assert.equal('statementProvenance'in saved,false);
  await assert.rejects(db.exec(migration),/helper exists/);await db.exec('rollback');
 }finally{await db.close();}
});
test('existing read policy hides archived documents, denies writes/helpers and rejects invalid native content without allocation',async()=>{
 const db=await fixture();try{
  await db.exec(migration);await db.query("select set_config('request.jwt.claim.sub',$1,false)",[admin]);const p=patches[0],row=(await db.query('select * from problem_catalog where problem_id=$1',[p.id])).rows[0],body={...row.body,statement:p.statement,statementProvenance:p.statementProvenance};await db.query('select admin_save_problem($1,$2,$3)',[body,p.number,row.revision]);
  const invalids=[x=>x.statement.translations={},x=>x.statementProvenance.rightsBasis='unknown',x=>x.statementProvenance.checks.translation=false,x=>x.statement.translations.en.sections[4].blocks.find(b=>b.type==='code').text+='wrong',x=>x.statement.sections[0].blocks.push({type:'image',path:'untracked/file.webp',alt:'bad',width:100,align:'center'})];
  for(const mutate of invalids){const bad=structuredClone(body);mutate(bad);await assert.rejects(db.query('select admin_save_problem($1)',[bad]));}
  assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,1010);
  await db.exec("update problem_catalog set archived=true where problem_id='"+p.id+"'");await db.query("select set_config('request.jwt.claim.sub','',false)");await db.exec('set role anon');assert.equal((await db.query('select * from problem_catalog where problem_id=$1',[p.id])).rows.length,0);await assert.rejects(db.query('select validate_native_problem_statement($1,$2)',[p.statement,p.statementProvenance]));await assert.rejects(db.query('select admin_save_problem($1)',[body]));
  await db.exec('reset role');await db.query("select set_config('request.jwt.claim.sub',$1,false)",[admin]);await db.exec('set role authenticated');assert.equal((await db.query('select * from problem_catalog where problem_id=$1',[p.id])).rows.length,1);await db.exec('reset role');
 }finally{await db.close();}
});
test('inline capability reads one existing RLS route and probes only a guaranteed validation failure',async()=>{
 const c=problemBackend({problemBackendVersion:32,problemStatementStorage:'catalog-inline-v1'});assert.equal(c.statement,true);assert.equal(c.editorial,false);assert.equal(c.bulkImport,false);
 const p=patches[0],calls=[];const client={from(table){calls.push(table);return{select(columns){calls.push(columns);return{eq(field,id){calls.push([field,id]);return{maybeSingle:async()=>({data:{body:{statement:p.statement,statementProvenance:p.statementProvenance},revision:3}})};}};}};}};
 assert.deepEqual((await readProblemStatement(client,p.id,c)).body,p.statement);assert.deepEqual(calls,['problem_catalog','body,revision',['problem_id',p.id]]);
 const db=await fixture();try{await db.query("select set_config('request.jwt.claim.sub',$1,false)",[admin]);const probe={rpc:async(name,args)=>{try{await db.query('select admin_save_problem($1,$2,$3)',[args.p_body,args.p_number,args.p_revision]);return{data:null};}catch(e){return{error:{code:e.code,message:e.message}};}}};await assert.rejects(requireInlineStatementBackend(probe),/баталгаажаагүй/);await db.exec(migration);await requireInlineStatementBackend(probe);assert.equal((await db.query('select last_value from problem_number_seq')).rows[0].last_value,1010);assert.equal((await db.query('select count(*)n from problem_changes')).rows[0].n,0);}finally{await db.close();}
});
