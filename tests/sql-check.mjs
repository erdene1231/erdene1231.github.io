// Executes real PostgreSQL migrations in WASM with a small pre-existing Supabase mock.
// This is not a production Supabase/auth integration test.
import {PGlite} from '@electric-sql/pglite';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const db=new PGlite(),root=new URL('../',import.meta.url),read=name=>fs.readFileSync(new URL(name,root),'utf8');
const A='00000000-0000-0000-0000-000000000001',B='00000000-0000-0000-0000-000000000002',ADMIN='00000000-0000-0000-0000-000000000003';
await db.exec(`
create schema auth;create role anon;create role authenticated;
create table auth.users(id uuid primary key,created_at timestamptz default now());insert into auth.users(id) values('${A}'),('${B}'),('${ADMIN}');
create function auth.uid() returns uuid language sql stable as $$ select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid $$;
grant usage on schema auth to anon,authenticated;grant execute on function auth.uid() to public;
create table public.profiles(user_id uuid primary key references auth.users(id),username text,full_name text default '',school text default '',avatar_path text);
insert into public.profiles(user_id,username) values('${A}','alpha'),('${B}','beta'),('${ADMIN}','admin');
alter table public.profiles enable row level security;grant select,update on public.profiles to authenticated;
create policy "own profile" on public.profiles for all to authenticated using(auth.uid()=user_id) with check(auth.uid()=user_id);
create table public.problem_catalog(problem_id text primary key,number bigint unique,body jsonb,archived boolean default false,revision integer default 1,updated_at timestamptz default now());
create sequence public.problem_number_seq start 1000;
create table public.problem_changes(problem_id text,actor_id uuid,action text,previous_body jsonb,next_body jsonb);
create table public.progress(user_id uuid references auth.users(id),problem_id text,status text check(status in ('new','trying','solved')),hints integer default 0,notes text default '',primary key(user_id,problem_id));
insert into public.progress(user_id,problem_id,status,notes) values('${A}','task-87','solved','private secret note');
alter table public.progress enable row level security;grant select,insert,update on public.progress to authenticated;
create policy "own progress" on public.progress for all to authenticated using(auth.uid()=user_id) with check(auth.uid()=user_id);
create function public.is_admin() returns boolean language sql stable as $$ select auth.uid()='${ADMIN}'::uuid $$;
create function public.get_public_profile(p_user_id uuid) returns table(user_id uuid,username text,full_name text,school text,avatar_path text,solved_count bigint,trying_count bigint,rank bigint)
language sql stable security definer as $$ select p.user_id,p.username,p.full_name,p.school,p.avatar_path,0::bigint,0::bigint,1::bigint from public.profiles p where p.user_id=p_user_id $$;
create function public.test_count_catalog() returns bigint language sql security definer as $$ select count(*) from public.problem_catalog where problem_id<>'task-87' $$;
`);
const oldProblem={id:'task-87',number:87,title:'Number Spiral',source:'CSES',ref:'legacy-ref',url:'https://cses.fi/problemset/task/1071',rating:1100,ratingKind:'estimated',priority:false,level:'Practice',tags:['math'],hints:[],hintsEn:[],lesson:''};
await db.query('insert into public.problem_catalog(problem_id,number,body) values($1,$2,$3)',[oldProblem.id,87,oldProblem]);
const four=read('supabase/004-following-admin.sql'),urlStart=four.indexOf('create or replace function public.valid_task_url('),urlEnd=four.indexOf('$$;',urlStart)+3;await db.exec(four.slice(urlStart,urlEnd));
const seven=read('supabase/007-custom-sources.sql');await db.exec(seven.slice(0,seven.indexOf('create or replace function public.admin_save_problem('))+'\ncommit;');
await db.exec("insert into public.problem_sources(name) values('atcoder') on conflict do nothing");
const eight=read('supabase/008-tutorials.sql');await db.exec(eight.slice(0,eight.indexOf('-- Seed only missing lessons'))+'\ncommit;');
const migrations=['015-problem-metadata.sql','016-learning-records.sql','017-real-progress-dates.sql','018-learning-profiles.sql','019-safe-learning-import.sql','020-new-tutorials.sql'];
for(const file of migrations)await db.exec(read('supabase/'+file));
async function auth(uid,role='authenticated'){await db.exec('reset role');await db.query("select set_config('request.jwt.claim.sub',$1,false)",[uid||'']);await db.exec('set role '+role);}
async function denied(action,label){let error;try{await action();}catch(e){error=e;}assert.equal(error?.code,'42501',label);}
await auth(A);await db.query("insert into public.learning_records(user_id,kind,key,value) values($1,'tutorial','binary-search',$2)",[A,{checks:['purpose'],secret:'learning-private'}]);
await auth(B);assert.equal((await db.query('select * from public.learning_records')).rows.length,0,'Cross-user read hidden');
await denied(()=>db.query("insert into public.learning_records(user_id,kind,key,value) values($1,'bookmark','x','{}')",[A]),'Cross-user write denied');
await auth(null,'anon');await denied(()=>db.query('select * from public.learning_records'),'Anonymous private-table read denied');
await auth(A);await db.query('update public.profiles set bio=$1 where user_id=$2',['Owned bio',A]);assert.equal((await db.query('update public.profiles set bio=$1 where user_id=$2 returning user_id',['bad',B])).rows.length,0,'Profile ownership');
let row=(await db.query('select * from public.progress where problem_id=$1',['task-87'])).rows[0];assert.equal(row.first_solved_at,null,'No legacy backfill');
await db.query('update public.progress set notes=$1 where problem_id=$2',['private secret note edited','task-87']);row=(await db.query('select * from public.progress where problem_id=$1',['task-87'])).rows[0];assert.equal(row.first_solved_at,null,'Notes edits do not invent a solve');
await db.query("insert into public.progress(user_id,problem_id,status,first_solved_at) values($1,'imported','solved','1999-01-01')",[A]);assert.equal((await db.query("select first_solved_at from public.progress where problem_id='imported'")).rows[0].first_solved_at,null,'Undated backup import stays unknown');
await db.query("insert into public.progress(user_id,problem_id,status,record_activity,first_solved_at) values($1,'new-action','solved',true,'1999-01-01')",[A]);
const first=(await db.query("select first_solved_at,record_activity from public.progress where problem_id='new-action'")).rows[0];assert(first.first_solved_at instanceof Date);assert.notEqual(first.first_solved_at.getUTCFullYear(),1999);assert.equal(first.record_activity,false,'Intent is consumed');
await db.query("update public.progress set status='trying',record_activity=true where problem_id='new-action'");await db.query("update public.progress set status='solved',record_activity=true,first_solved_at='1999-01-01' where problem_id='new-action'");assert.equal((await db.query("select first_solved_at from public.progress where problem_id='new-action'")).rows[0].first_solved_at.getTime(),first.first_solved_at.getTime(),'Repeated solve preserves first recorded date');
await denied(()=>db.query('select public.admin_import_learning_problems($1,false)',[[{title:'bad'}]]),'Non-admin importer denied');
const content=JSON.parse(read('learning-problems.json')).problems,problem=content[0];await auth(ADMIN);
const before=(await db.query('select public.test_count_catalog() as count')).rows[0].count;
let invalid=false;try{await db.query('select public.admin_import_learning_problems($1,true)',[[{...problem,rating:1}]]);}catch{invalid=true;}assert(invalid,'Dry run fully validates metadata');
const preview=(await db.query('select public.admin_import_learning_problems($1,true)',[[problem,problem]])).rows[0].admin_import_learning_problems;assert.equal(preview[1].status,'duplicate_batch');assert.equal((await db.query('select public.test_count_catalog() as count')).rows[0].count,before,'Dry run writes nothing');
const duplicateURL=(await db.query('select public.admin_import_learning_problems($1,false)',[[{...oldProblem,ref:'1071'}]])).rows[0].admin_import_learning_problems;assert.equal(duplicateURL[0].id,'task-87','Canonical URL deduplicates to original ID');
const saved=(await db.query('select public.admin_save_problem($1,87,1)',[{...oldProblem,ref:'1071'}])).rows[0].admin_save_problem;assert.equal(saved.id,'task-87','Editing retains original progress ID');
await db.query('select public.admin_import_learning_problems($1,false)',[[problem]]);await db.query('select public.admin_import_learning_problems($1,false)',[[problem]]);assert.equal((await db.query('select public.test_count_catalog() as count')).rows[0].count,1,'Idempotent import');
const another={...problem,ref:'another',url:'https://example.com/another'},bad={...problem,ref:'bad',url:'https://example.com/bad',rating:1};try{await db.query('select public.admin_import_learning_problems($1,false)',[[another,bad]]);}catch{}assert.equal((await db.query('select public.test_count_catalog() as count')).rows[0].count,1,'Atomic failed batch');
const tutorial=JSON.parse(read('tutorials.json')).tutorials.find(t=>t.id==='lower-bound');await db.query('select public.admin_store_learning_tutorial($1,0)',[tutorial]);let conflict=false;try{await db.query('select public.admin_store_learning_tutorial($1,0)',[tutorial]);}catch(e){conflict=e.code==='40001';}assert(conflict,'Tutorial revision conflict');
for(let i=0;i<content.length;i+=50)await db.query('select public.admin_import_learning_problems($1,true)',[content.slice(i,i+50)]);
for(let i=0;i<content.length;i+=50)await db.query('select public.admin_import_learning_problems($1,false)',[content.slice(i,i+50)]);
assert.equal((await db.query('select public.test_count_catalog() as count')).rows[0].count,content.length,'All 405 import in small batches');
await db.exec('reset role');const stored=(await db.query("select problem_id,body from public.problem_catalog where problem_id<>'task-87'")).rows;
for(const p of content){const actual=stored.find(x=>x.problem_id===p.id);assert(actual,'Stable ID '+p.id);assert.equal(actual.body.rating,p.rating);assert.equal(actual.body.ratingConfidence,p.ratingConfidence);assert.equal(actual.body.pack,p.pack);}
await auth(A);await db.query("insert into public.learning_records(user_id,kind,key,value) values($1,'plan','olympiad-100-v1',$2)",[A,{completedDays:[1,1,2,101,'3'],paused:'bad',private:'hidden plan note'}]);
await auth(null,'anon');const profile=(await db.query('select public.get_learning_profile($1) as data',[A])).rows[0].data;assert.equal(profile.plan.completedDays,2);assert.equal(profile.plan.paused,false);assert(!JSON.stringify(profile).includes('secret'));assert(!JSON.stringify(profile).includes('learning-private'));assert(!JSON.stringify(profile).includes('hidden plan note'));
await db.exec('reset role');const count=(await db.query('select count(*) from public.learning_records')).rows[0].count;for(const file of migrations)await db.exec(read('supabase/'+file));assert.equal((await db.query('select count(*) from public.learning_records')).rows[0].count,count,'Rerun preserves records');
const tutorials=JSON.parse(read('tutorials.json')).tutorials;for(const t of tutorials)await db.query('select public.validate_tutorial_body($1,$2)',[t.id,t]);
await db.exec(read('supabase/VERIFY-learning.sql'));
const report={engine:'PGlite PostgreSQL WASM; mocked existing Supabase environment, not production',migrations:migrations.length,tutorial_payloads:tutorials.length,metadata_imported:content.length,owner_rls:'PASS',profile_ownership:'PASS',legacy_undated:'PASS',backup_import_undated:'PASS',timestamp_tampering:'PASS',repeated_solve:'PASS',nonadmin_import:'PASS',dry_run_validation:'PASS',batch_dedup:'PASS',stable_ids_and_rating_provenance:'PASS',atomic_batch:'PASS',revision_conflict:'PASS',private_notes:'PASS',repeatable_migrations:'PASS'};fs.writeFileSync(new URL('tests/sql-report.json',root),JSON.stringify(report,null,2)+'\n');console.log(report);await db.close();
