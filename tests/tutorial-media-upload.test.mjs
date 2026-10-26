import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {PGlite} from '@electric-sql/pglite';
import {imageSignature} from '../tutorial-media.js';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('upload rejects forbidden MIME, forged signatures and oversized input before decoding',async()=>{
 for(const blob of [new Blob(['<svg></svg>'],{type:'image/svg+xml'}),new Blob(['not an image at all'],{type:'image/png'}),new Blob([new Uint8Array(5242881)],{type:'image/webp'}),new Blob(['short'],{type:'image/jpeg'})])await assert.rejects(imageSignature(blob));
 for(const [type,bytes] of [['image/png',[137,80,78,71,13,10,26,10,0,0,0,0]],['image/jpeg',[255,216,255,0,0,0,0,0,0,0,0,0]],['image/webp',Array.from('RIFF0000WEBP',x=>x.charCodeAt(0))]])assert.equal(await imageSignature(new Blob([new Uint8Array(bytes)],{type})),true);
});
test('025 Storage policies isolate drafts, permit published reads and protect referenced/recent media',async()=>{
 const db=new PGlite(),a='00000000-0000-0000-0000-000000000001',b='00000000-0000-0000-0000-000000000002',c='00000000-0000-0000-0000-000000000003';
 try{
 await db.exec(`create role anon;create role authenticated;create schema auth;create schema storage;create table auth.users(id uuid primary key);
 create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;grant usage on schema auth,storage to anon,authenticated;
 create table admin_accounts(user_id uuid primary key);create table tutorial_catalog(id text primary key,body jsonb,revision integer,updated_at timestamptz default now(),updated_by uuid);
 create table tutorial_changes(change_id bigserial primary key,tutorial_id text,actor_id uuid,revision integer,previous_body jsonb,new_body jsonb,created_at timestamptz default now());
 create table problem_catalog(problem_id text,body jsonb,archived boolean default false);
 create table storage.buckets(id text primary key,name text,public boolean,file_size_limit bigint,allowed_mime_types text[]);
 create table storage.objects(bucket_id text,name text,created_at timestamptz default now(),metadata jsonb default '{"size":50}',primary key(bucket_id,name));
 alter table storage.objects enable row level security;grant select,insert,update,delete on storage.objects to anon,authenticated;
 alter default privileges in schema public grant all on tables to anon,authenticated;
 alter default privileges in schema public grant all on functions to anon,authenticated;`);
 for(const id of [a,b,c])await db.query('insert into auth.users values ($1)',[id]);for(const id of [a,b])await db.query('insert into admin_accounts values ($1)',[id]);
 const baseline=JSON.parse(read('supabase/audit/production-after-023.json'));
 for(const name of ['is_admin','tutorial_require_text','safe_tutorial_link','validate_tutorial_inline','validate_tutorial_extended_block','validate_tutorial_body','get_tutorials'])await db.exec(baseline.functions.find(f=>f.name===name).definition);
 await db.exec(read('supabase/023-tutorial-drafts.sql'));await db.exec(read('supabase/024-tutorial-publication.sql'));
 const migration=read('supabase/025-tutorial-media.sql');await db.exec(migration);
 const validators=(await db.query("select pg_get_functiondef('validate_tutorial_body(text,jsonb)'::regprocedure) value")).rows[0].value;
 assert.equal(validators,baseline.functions.find(f=>f.name==='validate_tutorial_body').definition);
 assert.deepEqual((await db.query('select public,file_size_limit,allowed_mime_types from storage.buckets')).rows,[{public:false,file_size_limit:5242880,allowed_mime_types:['image/webp']}]);
 const actor=async(id,role='authenticated')=>{await db.exec('reset role');await db.query("select set_config('request.jwt.claim.sub',$1,false)",[id]);await db.exec('set role '+role);};
 const rpc=async(name,args=[])=> (await db.query(`select ${name}(${args.map((_,i)=>'$'+(i+1)).join(',')}) value`,args)).rows[0].value;
 const path=(id,n)=>`media-fixture/${id}/11111111-1111-1111-1111-${String(n).padStart(12,'0')}.webp`,p=path(a,1),recent=path(a,2),unused=path(a,3),missing=path(a,4);
 const insert=name=>db.query("insert into storage.objects(bucket_id,name) values('tutorial-media',$1)",[name]);
 const visible=async()=> (await db.query("select name from storage.objects where bucket_id='tutorial-media' order by name")).rows.map(r=>r.name);
 await actor('', 'anon');await assert.rejects(insert(p),e=>e.code==='42501');
 await actor(c);await assert.rejects(insert(path(c,1)),e=>e.code==='42501');
 await actor(a);await assert.rejects(insert(path(b,1)),e=>e.code==='42501');await assert.rejects(insert('bad-path.webp'),e=>e.code==='42501');
 await insert(p);await insert(recent);await insert(unused);assert.deepEqual(await visible(),[p,recent,unused]);
 assert.equal((await db.query('update storage.objects set metadata=\'{}\' returning name')).rows.length,0);
 await actor(b);assert.deepEqual(await visible(),[]);await actor('', 'anon');assert.deepEqual(await visible(),[]);
 await assert.rejects(rpc('admin_unused_tutorial_media'),e=>e.code==='42501');await assert.rejects(rpc('can_cleanup_tutorial_media',[unused]),e=>e.code==='42501');
 const original=JSON.parse(read('tutorials.json')).tutorials[0];const body={...original,id:'media-fixture',prerequisiteIds:[],related:[],sections:[{title:'Image',blocks:[{type:'image',path:p,alt:'A test diagram',width:80,align:'center'}]}]};delete body.translations;delete body.learningRelations;
 await actor(a);await rpc('admin_save_tutorial_draft',[body.id,body,0,0,a]);
 await db.exec('reset role');await db.exec("update storage.objects set created_at=now()-interval '8 days' where name<> '"+recent+"'");
 await actor(a);assert.equal(await rpc('can_cleanup_tutorial_media',[p]),false);assert.equal(await rpc('can_cleanup_tutorial_media',[recent]),false);assert.equal(await rpc('can_cleanup_tutorial_media',[unused]),true);
 assert.deepEqual((await rpc('admin_unused_tutorial_media')).map(x=>x.path),[unused]);
 // Another admin cannot publish a guessed path belonging to a private upload.
 await actor(b);await rpc('admin_save_tutorial_draft',[body.id,body,0,0,b]);await assert.rejects(rpc('admin_publish_tutorial_draft',[body.id,body,0,1,b]),e=>e.code==='42501');
 await actor(a);const absent=structuredClone(body);absent.sections[0].blocks[0].path=missing;await assert.rejects(rpc('admin_publish_tutorial_draft',[body.id,absent,0,1,a]),e=>e.code==='22023');
 await rpc('admin_publish_tutorial_draft',[body.id,body,0,1,a]);
 await actor('', 'anon');assert.deepEqual(await visible(),[p]);await actor(b);assert.deepEqual(await visible(),[p]);
 await actor(a);await rpc('admin_set_tutorial_publication',[body.id,1,false,a]);await actor('', 'anon');assert.deepEqual(await visible(),[]);
 await actor(a);assert.equal(await rpc('can_cleanup_tutorial_media',[p]),false);
 // History alone must prevent deletion, even after both editors remove their drafts.
 await db.exec('reset role');await db.exec('delete from tutorial_drafts');assert((await db.query("select * from tutorial_media_references where scope='history'")).rows.length>0);
 await actor(a);assert.equal(await rpc('can_cleanup_tutorial_media',[p]),false);assert.equal((await db.query("delete from storage.objects where name=$1 returning name",[p])).rows.length,0);
 assert.equal((await db.query("delete from storage.objects where name=$1 returning name",[unused])).rows.length,1);
 await actor(c);assert.equal(await rpc('can_cleanup_tutorial_media',[recent]),false);await assert.rejects(rpc('admin_unused_tutorial_media'),e=>e.code==='42501');
 await db.exec('reset role');await assert.rejects(db.exec(migration),/re-audit instead of replaying/);await db.exec('rollback');
 }finally{await db.close();}
});
