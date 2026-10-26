import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {PGlite} from '@electric-sql/pglite';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('024 publication preserves baseline, enforces actor/CAS, hides private drafts and validates public content',async()=>{
 const db=new PGlite(),a='00000000-0000-0000-0000-000000000001',b='00000000-0000-0000-0000-000000000002',c='00000000-0000-0000-0000-000000000003';
 try{
 await db.exec(`create role anon;create role authenticated;create schema auth;create table auth.users(id uuid primary key);
 create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;grant usage on schema auth to anon,authenticated;
 create table admin_accounts(user_id uuid primary key);create table tutorial_catalog(id text primary key,body jsonb,revision integer,updated_at timestamptz default now(),updated_by uuid);
 create table tutorial_changes(tutorial_id text,actor_id uuid,revision integer,previous_body jsonb,new_body jsonb,created_at timestamptz default now());
 create table problem_catalog(problem_id text,body jsonb,archived boolean default false);create table progress(id text,status text);insert into progress values ('stable-user-problem','solved');`);
 for(const id of [a,b,c])await db.query('insert into auth.users values ($1)',[id]);for(const id of [a,b])await db.query('insert into admin_accounts values ($1)',[id]);
 const baseline=JSON.parse(read('supabase/audit/production-after-023.json'));
 for(const name of ['is_admin','tutorial_require_text','safe_tutorial_link','validate_tutorial_inline','validate_tutorial_extended_block','validate_tutorial_body','get_tutorials'])await db.exec(baseline.functions.find(f=>f.name===name).definition);
 const topics=JSON.parse(read('tutorials.json')).tutorials;for(const t of topics)await db.query('insert into tutorial_catalog(id,body,revision) values($1,$2,7)',[t.id,t]);
 const before=(await db.query('select id,body,revision from tutorial_catalog order by id')).rows;
 await db.exec(read('supabase/023-tutorial-drafts.sql'));const migration=read('supabase/024-tutorial-publication.sql');await db.exec(migration);
 assert.deepEqual((await db.query('select id,body,revision from tutorial_catalog order by id')).rows,before);
 const actor=async(id,role='authenticated')=>{await db.exec('reset role');await db.query("select set_config('request.jwt.claim.sub',$1,false)",[id]);await db.exec('set role '+role);};
 const rpc=async(name,args=[])=> (await db.query(`select ${name}(${args.map((_,i)=>'$'+(i+1)).join(',')}) value`,args)).rows[0].value;
 const body={...structuredClone(topics[0]),id:'publication-fixture',prerequisiteIds:[],related:[],title:'Private candidate'};
 const save=(value,base=0,rev=0,who=a)=>rpc('admin_save_tutorial_draft',[body.id,value,base,rev,who]);
 const publish=(value,base=0,rev=1,who=a)=>rpc('admin_publish_tutorial_draft',[body.id,value,base,rev,who]);
 const fails=(fn,code)=>assert.rejects(fn,e=>e.code===code);
 await actor(a);await save(body);await actor('', 'anon');assert.equal(await rpc('get_published_tutorial',[body.id]),null);await fails(()=>publish(body),'42501');
 await actor(c);await fails(()=>publish(body,0,1,c),'42501');await actor(b);await fails(()=>publish(body,0,1,a),'42501');await fails(()=>publish(body,0,1,b),'40001');await save({...body,title:'Other admin'},0,0,b);
 await actor(a);await fails(()=>publish({...body,_draftRelationsText:'private'}),'22023');await fails(()=>publish({...body,prerequisiteIds:[42]}),'22023');await fails(()=>publish({...body,prerequisiteIds:['missing']}),'22023');
 await fails(()=>publish({...body,sections:[{title:'unsafe',blocks:[{type:'rich',content:[{text:'x',href:'javascript:alert(1)'}]}]}]}),'22023');
 await fails(()=>publish({...body,learningRelations:{practice:[],variants:[],next:null}}),'22023');
 const published=await publish(body);assert.equal(published.revision,1);assert.equal(published.draft,null);await fails(()=>publish(body),'40001');await actor(b);await fails(()=>publish({...body,title:'Other admin'},0,1,b),'40001');await actor(a);
 await actor('', 'anon');assert.deepEqual((await rpc('get_published_tutorial',[body.id])).body,body);assert.equal((await rpc('get_tutorial_index')).tutorials.find(t=>t.body.id===body.id).body.sections,undefined);
 await actor(a);await save({...body,_draftRelationsText:'local only'},1);const clean=await publish({...body,title:'Public edited'},1);assert.equal(clean.draft.revision,2);assert.equal(clean.draft.base_revision,2);
 await rpc('admin_set_tutorial_publication',[body.id,2,false,a]);await actor('', 'anon');assert.equal(await rpc('get_published_tutorial',[body.id]),null);assert(!(await rpc('get_tutorials')).some(t=>t.body.id===body.id));
 await actor(a);await rpc('admin_set_tutorial_publication',[body.id,3,true,a]);
 await db.exec('reset role');await db.query('delete from admin_accounts where user_id=$1',[a]);await actor(a);await fails(()=>rpc('admin_set_tutorial_publication',[body.id,4,false,a]),'42501');
 await db.exec('reset role');assert.deepEqual((await db.query('select * from progress')).rows,[{id:'stable-user-problem',status:'solved'}]);
 await assert.rejects(db.exec(migration),/re-audit instead of replaying/);await db.exec('rollback');
 }finally{await db.close();}
});
