import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {PGlite} from '@electric-sql/pglite';

const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
const a='00000000-0000-0000-0000-000000000001',b='00000000-0000-0000-0000-000000000002',student='00000000-0000-0000-0000-000000000003';

test('028 permanent tutorial deletion: authorization, references, stable IDs, progress and no resurrection',async t=>{
 const db=new PGlite();
 try{
  await db.exec(`create role anon;create role authenticated;create schema auth;create schema storage;
   create table auth.users(id uuid primary key);
   create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;
   grant usage on schema auth,storage to anon,authenticated;
   create table admin_accounts(user_id uuid primary key);
   create table tutorial_catalog(id text primary key,body jsonb,revision integer,updated_at timestamptz default now(),updated_by uuid references auth.users(id));
   create table tutorial_changes(change_id bigserial primary key,tutorial_id text references tutorial_catalog(id),actor_id uuid references auth.users(id),revision integer,previous_body jsonb,new_body jsonb,created_at timestamptz default now());
   create table problem_catalog(problem_id text,body jsonb,archived boolean default false);
   create table learning_records(user_id uuid,kind text,record_key text,body jsonb);
   create table progress(user_id uuid,problem_id text,status text);
   create table storage.buckets(id text primary key,name text,public boolean,file_size_limit bigint,allowed_mime_types text[]);
   create table storage.objects(bucket_id text,name text,created_at timestamptz default now(),metadata jsonb default '{"size":50}',primary key(bucket_id,name));
   alter table storage.objects enable row level security;grant select,insert,update,delete on storage.objects to anon,authenticated;
   alter default privileges in schema public grant all on tables to anon,authenticated;
   alter default privileges in schema public grant all on functions to anon,authenticated;`);
  for(const id of [a,b,student])await db.query('insert into auth.users values ($1)',[id]);
  for(const id of [a,b])await db.query('insert into admin_accounts values ($1)',[id]);
  const baseline=JSON.parse(read('supabase/audit/production-after-023.json'));
  for(const name of ['is_admin','tutorial_require_text','safe_tutorial_link','validate_tutorial_inline','validate_tutorial_extended_block','validate_tutorial_body','get_tutorials'])await db.exec(baseline.functions.find(f=>f.name===name).definition);
  for(const path of ['023-tutorial-drafts.sql','024-tutorial-publication.sql','025-tutorial-media.sql'])await db.exec(read('supabase/'+path));
  const original=JSON.parse(read('tutorials.json')).tutorials[0];
  const body=id=>{const x={...structuredClone(original),id,title:id,prerequisiteIds:[],related:[],sections:[{title:'Fixture',blocks:[{type:'rich',content:[{text:'Preserve original content.',marks:[]}]}]}]};delete x.translations;delete x.learningRelations;return x;};
  const doomed=body('delete-fixture'),survivor=body('survivor-stable-id');
  const image=`delete-fixture/${a}/11111111-1111-1111-1111-111111111111.webp`;
  doomed.sections[0].blocks.push({type:'image',path:image,alt:'Fixture diagram',width:80,align:'center'});
  await db.query("insert into storage.objects(bucket_id,name,created_at) values('tutorial-media',$1,now()-interval '8 days')",[image]);
  for(const value of [doomed,survivor])await db.query('insert into tutorial_catalog(id,body,revision) values($1,$2,7)',[value.id,value]);
  await db.query('insert into tutorial_changes(tutorial_id,actor_id,revision,previous_body,new_body) values($1,$2,7,$3,$3)',[doomed.id,a,doomed]);
  await db.query('insert into tutorial_drafts(tutorial_id,editor_id,body,base_revision,revision) values($1,$2,$3,7,1),($1,$4,$3,7,1)',[doomed.id,a,doomed,b]);
  for(const id of [doomed.id,survivor.id])await db.query("insert into learning_records values($1,'tutorial',$2,'{\"readSections\":[0],\"selfCheck\":true}')",[student,id]);
  await db.query("insert into progress values($1,'stable-problem-id','solved')",[student]);
  const snapshot=async table=>(await db.query('select * from '+table+' order by 1'+(table==='tutorial_deleted_ids'?'':',2'))).rows;
  const before=await snapshot('tutorial_catalog'),learning=await snapshot('learning_records'),progress=await snapshot('progress'),media=await snapshot('storage.objects');
  const definitions=await db.query("select p.proname,pg_get_functiondef(p.oid) definition from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('validate_tutorial_body','validate_tutorial_publication','admin_save_tutorial_draft','admin_rebase_tutorial_draft','admin_publish_tutorial_draft','admin_set_tutorial_publication') order by 1");
  const migration=read('supabase/028-tutorial-deletion.sql');
  await db.exec(migration);
  const actor=async(id,role='authenticated')=>{await db.exec('reset role');await db.query("select set_config('request.jwt.claim.sub',$1,false)",[id]);await db.exec('set role '+role);};
  const rpc=async(name,args=[])=>(await db.query(`select ${name}(${args.map((_,i)=>'$'+(i+1)).join(',')}) value`,args)).rows[0].value;
  const remove=(revision=8,confirmation=doomed.id,who=a)=>rpc('admin_delete_tutorial',[doomed.id,revision,confirmation,who]);
  const reject=(fn,code,message)=>assert.rejects(fn,e=>e.code===code&&(!message||message.test(e.message)));

  await t.test('install changes no existing rows or validation functions',async()=>{
   assert.deepEqual(await snapshot('tutorial_catalog'),before);
   assert.deepEqual(await snapshot('learning_records'),learning);assert.deepEqual(await snapshot('progress'),progress);
   assert.deepEqual((await db.query("select p.proname,pg_get_functiondef(p.oid) definition from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('validate_tutorial_body','validate_tutorial_publication','admin_save_tutorial_draft','admin_rebase_tutorial_draft','admin_publish_tutorial_draft','admin_set_tutorial_publication') order by 1")).rows,definitions.rows);
  });
  await t.test('anonymous, non-admin, mismatched actor, confirmation, stale revision and published rejection',async()=>{
   await actor('', 'anon');await reject(()=>remove(),'42501');await reject(()=>rpc('admin_tutorial_document',[doomed.id]),'42501');
   await actor(student);await reject(()=>remove(7,doomed.id,student),'42501');await reject(()=>rpc('admin_tutorial_document',[doomed.id]),'42501');
   await actor(a);await reject(()=>remove(7,doomed.id,b),'42501');
   assert.equal((await rpc('admin_tutorial_document',[doomed.id])).deleted,false);
   assert.deepEqual(await rpc('admin_tutorial_document',['new-unused-id']),{current:null,draft:null,deleted:false});
   await reject(()=>remove(7,'wrong-id'),'22023',/TYPE_ID_TO_CONFIRM/);
   await reject(()=>remove(6),'40001',/REVISION_CONFLICT/);
   await reject(()=>remove(7),'22023',/UNPUBLISH_FIRST/);
   await reject(()=>db.query('insert into tutorial_deleted_ids values ($1)',[doomed.id]),'42501');
   await rpc('admin_set_tutorial_publication',[doomed.id,7,false,a]);
   await reject(()=>remove(7),'40001');
  });
  await t.test('all supported incoming catalog/draft references block without exposing private bodies',async()=>{
   const references=[
    {prerequisiteIds:[doomed.id]},
    {related:[doomed.id]},
    {learningRelations:{next:doomed.id}},
    {learningRelations:{variants:[{tutorialId:doomed.id}]}},
    {sections:[{blocks:[{type:'tutorial',tutorialId:doomed.id}]}]},
    {translations:{en:{sections:[{blocks:[{type:'rich',content:[{text:'Read',href:'#tutorial/'+doomed.id+'/part/0'}]}]}]}}},
    {_draftRelationsText:JSON.stringify({variants:[{tutorialId:doomed.id}],next:null,practice:[]})},
    {_draftRelationsText:JSON.stringify({variants:[],next:doomed.id,practice:[]})}
   ];
   for(const [index,ref] of references.entries()){
    await db.exec('reset role');
    const linked={...body('private-link-source'),...ref,title:'Never disclose private draft title'};
    await db.query('insert into tutorial_drafts(tutorial_id,editor_id,body,base_revision,revision) values($1,$2,$3,0,1)',[linked.id,b,linked]);
    await actor(a);
    await assert.rejects(remove(),e=>e.code==='22023'&&/TUTORIAL_REFERENCED/.test(e.message)&&!e.message.includes(linked.title),'draft reference '+index);
    await db.exec('reset role');await db.query('delete from tutorial_drafts where tutorial_id=$1',[linked.id]);
   }
   // An unpublished catalog document is also retained until its link is edited.
   const linked={...body('archived-link-source'),related:[doomed.id]};
   await db.query('insert into tutorial_catalog(id,body,revision,published) values($1,$2,1,false)',[linked.id,linked]);
   await actor(a);await reject(remove,'22023',/TUTORIAL_REFERENCED/);
   await db.exec('reset role');await db.query('delete from tutorial_catalog where id=$1',[linked.id]);
   // Incomplete draft metadata must not make the reference scanner throw.
   await db.query('insert into tutorial_drafts(tutorial_id,editor_id,body,base_revision,revision) values($1,$2,$3,0,1)',
    ['incomplete-draft',b,{id:'incomplete-draft',prerequisiteIds:null,related:{unfinished:true},sections:'typing',_draftRelationsText:'{"next":'}]);
   await db.query('insert into tutorial_drafts(tutorial_id,editor_id,body,base_revision,revision) values($1,$2,$3,0,1)',
    ['invalid-json-number',b,{id:'invalid-json-number',_draftRelationsText:'{"incomplete":1e1000000}'}]);
  });
  await t.test('permanent removal erases selected catalog/drafts/history, keeps all survivor IDs and progress',async()=>{
   await actor(a);assert.deepEqual(await remove(),{id:doomed.id,deleted:true});
   await reject(remove,'40001');await db.exec('reset role');
   assert.deepEqual(await snapshot('tutorial_catalog'),before.filter(row=>row.id!==doomed.id));
   assert.equal((await db.query('select * from tutorial_drafts where tutorial_id=$1',[doomed.id])).rows.length,0);
   assert.equal((await db.query('select * from tutorial_changes where tutorial_id=$1',[doomed.id])).rows.length,0);
   assert.equal((await db.query('select * from tutorial_drafts where tutorial_id=$1',['incomplete-draft'])).rows.length,1);
   assert.deepEqual(await snapshot('learning_records'),learning);assert.deepEqual(await snapshot('progress'),progress);
   assert.deepEqual(await snapshot('tutorial_deleted_ids'),[{id:doomed.id}]);
   assert.deepEqual(await snapshot('storage.objects'),media);
   assert.equal((await db.query('select * from tutorial_media_references where object_path=$1',[image])).rows.length,0);
   await actor('', 'anon');assert.equal(await rpc('get_published_tutorial',[doomed.id]),null);
   assert((await rpc('get_tutorials')).some(row=>row.body.id===survivor.id));
   await reject(()=>db.query('select * from tutorial_deleted_ids'),'42501');
   await actor(a);assert.deepEqual(await rpc('admin_tutorial_document',[doomed.id]),{current:null,draft:null,deleted:true});
   assert.equal((await rpc('admin_tutorial_document',[survivor.id])).deleted,false);
   assert.deepEqual(await rpc('admin_tutorial_history',[doomed.id]),[]);
  });
  await t.test('stale clients cannot recreate a deleted ID or save new links to it',async()=>{
   await actor(a);
   await reject(()=>rpc('admin_save_tutorial_draft',[doomed.id,doomed,0,0,a]),'22023',/TUTORIAL_DELETED/);
   await reject(()=>rpc('admin_rebase_tutorial_draft',[doomed.id,doomed,0,0,a]),'22023',/TUTORIAL_DELETED/);
   const linked={...body('new-private-lesson'),related:[doomed.id]};
   await reject(()=>rpc('admin_save_tutorial_draft',[linked.id,linked,0,0,a]),'22023',/TUTORIAL_DELETED_REFERENCE/);
   await db.exec('reset role');
   await reject(()=>db.query('insert into tutorial_catalog(id,body,revision,published) values($1,$2,1,false)',[doomed.id,doomed]),'22023',/TUTORIAL_DELETED/);
   await reject(()=>db.query('update tutorial_catalog set body=$1 where id=$2',[{...survivor,related:[doomed.id]},survivor.id]),'22023',/TUTORIAL_DELETED_REFERENCE/);
   assert.deepEqual(await snapshot('tutorial_catalog'),before.filter(row=>row.id!==doomed.id));
   await assert.rejects(db.exec(migration),/re-audit instead of replaying/);await db.exec('rollback');
  });
 }finally{await db.close();}
});
