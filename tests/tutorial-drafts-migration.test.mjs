// Historical migration fixtures use the original 55; current Introduction publication is tested separately.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {PGlite} from '@electric-sql/pglite';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('023 isolates editor drafts, enforces CAS/rebase/authorization, and preserves catalog',async()=>{
 const db=new PGlite(),a='00000000-0000-0000-0000-000000000001',b='00000000-0000-0000-0000-000000000002',c='00000000-0000-0000-0000-000000000003';
 try{
 await db.exec(`create role anon;create role authenticated;create schema auth;
 create table auth.users(id uuid primary key);
 create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;
 grant usage on schema auth to anon,authenticated;
 create table admin_accounts(user_id uuid primary key);
 create table tutorial_catalog(id text primary key,body jsonb not null,revision integer not null,updated_at timestamptz default now());
 create table tutorial_changes(tutorial_id text,revision integer,new_body jsonb,previous_body jsonb,created_at timestamptz default now());
 create table progress(id text primary key,status text);
 insert into progress values ('stable-user-problem','solved');`);
 for(const id of [a,b,c])await db.query('insert into auth.users values ($1)',[id]);
 for(const id of [a,b])await db.query('insert into admin_accounts values ($1)',[id]);
 const baseline=JSON.parse(read('supabase/audit/production-after-022.json'));
 for(const name of ['is_admin','tutorial_require_text','safe_tutorial_link','validate_tutorial_inline','validate_tutorial_extended_block','validate_tutorial_body'])await db.exec(baseline.functions.find(f=>f.name===name).definition);
 const lessons=JSON.parse(read('tutorials.json')).tutorials.filter(t=>t.id!=='introduction');
 for(const t of lessons)await db.query('insert into tutorial_catalog(id,body,revision) values ($1,$2,7)',[t.id,t]);
 const catalog=()=>db.query('select id,body,revision,updated_at from tutorial_catalog order by id');
 const before=(await catalog()).rows,validator=await db.query("select pg_get_functiondef('validate_tutorial_body(text,jsonb)'::regprocedure) as definition");
 const sql=read('supabase/023-tutorial-drafts.sql');await db.exec(sql);
 const actor=async(id,role='authenticated')=>{await db.exec('reset role');await db.query("select set_config('request.jwt.claim.sub',$1,false)",[id]);await db.exec('set role '+role);};
 const rpc=async(name,args=[])=> (await db.query(`select ${name}(${args.map((_,i)=>'$'+(i+1)).join(',')}) as value`,args)).rows[0].value;
 const save=(id,body,base,rev,who)=>rpc('admin_save_tutorial_draft',[id,body,base,rev,who]);
 const rebase=(base,rev,who=a)=>rpc('admin_rebase_tutorial_draft',['complexity',{id:'complexity',title:'Rebased'},base,rev,who]);
 const denied=fn=>assert.rejects(fn,e=>e.code==='42501');
 const conflict=fn=>assert.rejects(fn,e=>e.code==='40001');
 await actor(a);let draft=await save('complexity',{id:'complexity',title:'Private A'},7,0,a);assert.equal(draft.revision,1);assert.equal(draft.editor_id,undefined);
 await conflict(()=>save('complexity',{id:'complexity'},7,0,a));
 await conflict(()=>save('complexity',{id:'complexity'},8,1,a));
 await denied(()=>save('complexity',{id:'complexity'},7,1,b));
 for(const [id,body,base,rev] of [['BAD',{id:'BAD'},7,1],['complexity',[],7,1],['complexity',{id:'other'},7,1],['complexity',{id:'complexity'},null,1],['complexity',{id:'complexity'},7,-1]])await assert.rejects(()=>save(id,body,base,rev,a),e=>e.code==='22023');
 await actor(b);assert.equal((await rpc('admin_tutorial_document',['complexity'])).draft,null);
 assert.deepEqual((await rpc('admin_tutorial_workspace')).drafts,[]);
 await save('complexity',{id:'complexity',title:'Private B'},7,0,b);
 assert.equal((await rpc('admin_tutorial_document',['complexity'])).draft.body.title,'Private B');
 await actor(a);assert.equal((await rpc('admin_tutorial_document',['complexity'])).draft.body.title,'Private A');
 await conflict(()=>rebase(6,1));await conflict(()=>rebase(7,0));
 draft=await rebase(7,1);assert.equal(draft.revision,2);assert.equal(draft.base_revision,7);
 // Two queued saves with the same revision: one wins, the other is rejected.
 const attempts=await Promise.allSettled([save('complexity',{id:'complexity',title:'One'},7,2,a),save('complexity',{id:'complexity',title:'Two'},7,2,a)]);
 assert.equal(attempts.filter(x=>x.status==='fulfilled').length,1);assert.equal(attempts.find(x=>x.status==='rejected').reason.code,'40001');
 assert.equal((await rpc('admin_tutorial_history',['complexity']))[0].revision,7);
 assert.deepEqual(await rpc('admin_tutorial_history_body',['complexity',7]),lessons.find(t=>t.id==='complexity'));
 for(const role of ['authenticated','anon']){await actor(a,role);await denied(()=>db.query('select * from tutorial_drafts'));await denied(()=>db.query("delete from tutorial_drafts"));}
 await actor('', 'anon');await denied(()=>rpc('admin_tutorial_workspace'));
 await actor(c);await denied(()=>rpc('admin_tutorial_document',['complexity']));await denied(()=>save('complexity',{id:'complexity'},7,0,c));await denied(()=>rpc('admin_tutorial_history',['complexity']));await denied(()=>rpc('admin_tutorial_history_body',['complexity',7]));await denied(()=>rebase(7,0,c));
 await db.exec('reset role');await db.query('delete from admin_accounts where user_id=$1',[a]);await actor(a);await denied(()=>rpc('admin_tutorial_workspace'));await denied(()=>save('complexity',{id:'complexity'},7,3,a));
 await db.exec('reset role');assert.deepEqual((await catalog()).rows,before);assert.deepEqual((await db.query('select * from progress')).rows,[{id:'stable-user-problem',status:'solved'}]);
 assert.deepEqual(await db.query("select pg_get_functiondef('validate_tutorial_body(text,jsonb)'::regprocedure) as definition"),validator);
 assert.equal((await db.query('select count(*)::int as count from tutorial_catalog where published')).rows[0].count,55);
 await assert.rejects(db.exec(sql),/already exist/);await db.exec('rollback');
 }finally{await db.close();}
});
