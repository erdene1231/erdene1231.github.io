import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {PGlite} from '@electric-sql/pglite';
import {proposedTutorialRows, proposalProblems} from '../tools/package02_tutorial_proposals.mjs';
import {publicationBody} from '../tutorial-publication.js';

async function foundationDatabase() {
    const db = new PGlite();
    try {
        await db.exec(`
            create role anon; create role authenticated;
            create schema auth; create schema storage;
            create table auth.users(id uuid primary key);
            create function auth.uid() returns uuid language sql stable as $$
                select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid
            $$;
            grant usage on schema auth to anon,authenticated;
            create table admin_accounts(user_id uuid primary key);
            create table tutorial_catalog(id text primary key,body jsonb,revision integer,published boolean,published_at timestamptz,updated_at timestamptz default now(),updated_by uuid);
            create table tutorial_drafts(tutorial_id text,editor_id uuid,body jsonb,revision integer,base_revision integer,updated_at timestamptz default now(),primary key(tutorial_id,editor_id));
            create table tutorial_changes(change_id bigserial,tutorial_id text,actor_id uuid,revision integer,previous_body jsonb,new_body jsonb);
            create table problem_catalog(problem_id text,number bigint,body jsonb,archived boolean default false);
            create table tutorial_deleted_ids(id text primary key);
            create table tutorial_media_references(scope text,scope_id text,object_path text,primary key(scope,scope_id,object_path));
            create table storage.objects(bucket_id text,name text);
            create table progress(id text,status text); insert into progress values('stable','solved');
            create table learning_records(key text,value jsonb); insert into learning_records values('stable','{"readSections":[0,1],"checks":["purpose"]}');
        `);
        const snapshot = JSON.parse(fs.readFileSync('supabase/audit/production-before-032.json'));
        for (const name of ['is_admin','tutorial_require_text','tutorial_optional_text','safe_tutorial_link',
            'validate_tutorial_inline','validate_tutorial_extended_block','validate_tutorial_body',
            'validate_tutorial_publication','check_tutorial_publication','admin_save_tutorial_draft',
            'admin_publish_tutorial_draft','admin_save_tutorial','admin_store_learning_tutorial','tutorial_image_paths','refresh_tutorial_media_references','check_tutorial_media_exists']) {
            const fn = snapshot.functions.find(fn=>fn.name===name);
            assert.ok(fn,name); await db.exec(fn.definition);
        }
        const baseline = JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials;
        // The test-content exception's live metadata was separately confirmed read-only.
        const joke = baseline.find(row=>row.body.id==='mongolia'); joke.revision=2; joke.published=false;
        const proposals = proposedTutorialRows(baseline), problems = proposalProblems();
        for (const row of baseline) await db.query('insert into tutorial_catalog(id,body,revision,published) values($1,$2,$3,$4)',[row.body.id,row.body,row.revision,row.published]);
        for (const problem of problems) await db.query('insert into problem_catalog(problem_id,number,body) values($1,$2,$3)',[problem.id,problem.number,problem]);
        await db.exec(`create trigger publication_check before insert or update on tutorial_catalog for each row execute function check_tutorial_publication();
            create trigger media_check before insert or update on tutorial_catalog for each row execute function check_tutorial_media_exists();
            create trigger published_refs after insert or update on tutorial_catalog for each row execute function refresh_tutorial_media_references();
            create trigger draft_refs after insert or update or delete on tutorial_drafts for each row execute function refresh_tutorial_media_references();
            create trigger history_refs after insert on tutorial_changes for each row execute function refresh_tutorial_media_references();`);
        return {db, baseline, proposals, problems};
    } catch(error) { await db.close(); throw error; }
}

// Isolated synthetic accounts only. No connection to Supabase or real Auth users.
async function localOwnerGuard(db,scope_ids=['binary-search','dynamic-programming','greedy']) {
    const names=['admin_save_tutorial','admin_store_learning_tutorial','admin_publish_tutorial_draft',
        'validate_tutorial_body','validate_tutorial_publication','refresh_tutorial_media_references','check_tutorial_media_exists'];
    const functions=(await db.query(`select p.oid::regprocedure::text signature,md5(pg_get_functiondef(p.oid)) definition_md5,proacl::text acl
        from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname=any($1) order by p.proname`,[names])).rows;
    const catalog_triggers=(await db.query(`select jsonb_agg(pg_get_triggerdef(oid) order by tgname) value from pg_trigger
        where tgrelid='public.tutorial_catalog'::regclass and not tgisinternal`)).rows[0].value;
    const draft_fingerprint=(await db.query(`select md5(coalesce(jsonb_agg(to_jsonb(d) order by tutorial_id,editor_id)::text,'[]')) value
        from tutorial_drafts d where tutorial_id=any($1)` ,[scope_ids])).rows[0].value;
    return {functions,catalog_triggers,draft_fingerprint,scope_ids};
}


test('all52 mechanical style updates use guarded native lifecycle and preserve drafts, unrelated lessons, bank and progress',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs');const {db}=await foundationDatabase();
 try{
 const docs=fs.readdirSync('audit/package03-cp-style').filter(p=>p.endsWith('.json')).map(p=>JSON.parse(fs.readFileSync('audit/package03-cp-style/'+p))).filter(d=>d.changed);
 await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,7,revision from tutorial_catalog where id in('sorting','binary-search','mongolia')");
 const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,problems:(await db.query('select * from problem_catalog order by number')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
 const before=await snapshot();
 for(const [index,d]of docs.entries()){
  const old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[d.id])).rows[0];
  const target={...d,expected_revision:old.revision,expected_published:old.published,expected_body_md5:old.body_md5};
  const g=await localOwnerGuard(db,[d.id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
  if(index===0){const initial=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected style failure';")),/Injected style/);assert.deepEqual(await snapshot(),initial);}
  await db.exec(sql);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }
 const after=await snapshot();for(const k of ['drafts','problems','progress','learning'])assert.deepEqual(after[k],before[k]);
 const changed=new Set(docs.map(d=>d.id));assert.deepEqual(after.catalog.filter(r=>!changed.has(r.id)),before.catalog.filter(r=>!changed.has(r.id)));
 for(const d of docs){const row=after.catalog.find(r=>r.id===d.id),old=before.catalog.find(r=>r.id===d.id);assert.deepEqual(row.body,d.body);assert.equal(row.revision,old.revision+1);assert.equal(row.published,old.published);}
 assert.equal((await db.query('select count(*)::int n from tutorial_changes')).rows[0].n,52);
 }finally{await db.close();}
});
test('handbook LCA replacement publishes flexible11-section native content atomically without changing drafts or other lessons',async()=>{
 const{ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs');const{db}=await foundationDatabase();try{
 const d=JSON.parse(fs.readFileSync('audit/package03-lessons/lca.json'));const old=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='lca'")).rows[0];
 await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,3,revision from tutorial_catalog where id in('lca','mongolia','sorting')");
 const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows});const before=await snapshot();const target={...d,expected_revision:old.revision,expected_body_md5:old.body_md5};const sql=ownerReviewedLessonsSql({targets:[target]},await localOwnerGuard(db,['lca']));
 await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected handbook failure';")),/Injected handbook/);assert.deepEqual(await snapshot(),before);
 await db.exec(sql);const after=await snapshot();assert.deepEqual(after.drafts,before.drafts);assert.deepEqual(after.progress,before.progress);assert.deepEqual(after.catalog.filter(t=>t.id!=='lca'),before.catalog.filter(t=>t.id!=='lca'));const now=after.catalog.find(t=>t.id==='lca');assert.deepEqual(now.body,d.body);assert.equal(now.body.sections.length,11);assert.equal(now.revision,old.revision+1);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
test('time complexity exemplar preserves a private draft and all unrelated state through native owner publication',async()=>{
 const{ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs');const{db}=await foundationDatabase();try{
 const d=JSON.parse(fs.readFileSync('audit/package03-lessons/complexity.json'));const old=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='complexity'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) values('complexity','00000000-0000-0000-0000-000000000002',$1,10,$2)",[old.body,old.revision]);
 const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});const before=await snapshot();const target={...d,expected_revision:old.revision,expected_body_md5:old.body_md5};const sql=ownerReviewedLessonsSql({targets:[target]},await localOwnerGuard(db,['complexity']));
 await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected complexity failure';")),/Injected complexity/);assert.deepEqual(await snapshot(),before);
 await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!=='complexity'),before.catalog.filter(t=>t.id!=='complexity'));const now=after.catalog.find(t=>t.id==='complexity');assert.deepEqual(now.body,d.body);assert.equal(now.revision,old.revision+1);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
