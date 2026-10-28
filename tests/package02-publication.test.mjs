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
test('finished foundation documents save, publish and reload through native 031 RPCs without losing private drafts or progress', async()=>{
    const {db,baseline,proposals,problems} = await foundationDatabase();
    try {
        const actor='00000000-0000-0000-0000-000000000001', other='00000000-0000-0000-0000-000000000002';
        for (const id of [actor,other]) await db.query('insert into admin_accounts values($1)',[id]);
        const rpc=async(name,args)=>(await db.query('select '+name+'('+args.map((_,i)=>'$'+(i+1)).join(',')+') value',args)).rows[0].value;
        const identity=async id=>db.query("select set_config('request.jwt.claim.sub',$1,false)",[id]);
        const beforeJoke=(await db.query("select * from tutorial_catalog where id='mongolia'")).rows;
        const beforeProgress=(await db.query('select * from progress')).rows;
        const beforeLearning=(await db.query('select * from learning_records')).rows;
        const binary=baseline.find(row=>row.body.id==='binary-search');
        await identity(other);
        await rpc('admin_save_tutorial_draft',['binary-search',{...binary.body,_draftRelationsText:'{"variants":[],"practice":[],"next":null}'},5,0,other]);
        const otherDraft=(await db.query('select * from tutorial_drafts where editor_id=$1',[other])).rows;
        await identity(actor);
        for (const id of ['binary-search','greedy','dynamic-programming']) {
            const body=publicationBody(proposals.find(row=>row.body.id===id).body,proposals.map(row=>row.body),problems);
            await rpc('admin_save_tutorial_draft',[id,body,5,0,actor]);
            const saved=await rpc('admin_publish_tutorial_draft',[id,body,5,1,actor]);
            assert.equal(saved.revision,6); assert.equal(saved.published,true);
            const reloaded=(await db.query('select body from tutorial_catalog where id=$1',[id])).rows[0].body;
            assert.deepEqual(reloaded,body);
            assert.deepEqual(publicationBody(JSON.parse(JSON.stringify(reloaded)),proposals.map(row=>row.body),problems),body);
            await assert.rejects(rpc('admin_publish_tutorial_draft',[id,body,5,1,actor]),error=>error.code==='40001');
        }
        assert.deepEqual((await db.query('select * from tutorial_drafts where editor_id=$1',[other])).rows,otherDraft);
        await identity(other);
        await assert.rejects(rpc('admin_publish_tutorial_draft',['binary-search',binary.body,5,1,other]),error=>error.code==='40001');
        assert.deepEqual((await db.query("select * from tutorial_catalog where id='mongolia'")).rows,beforeJoke);
        assert.deepEqual((await db.query('select * from progress')).rows,beforeProgress);
        assert.deepEqual((await db.query('select * from learning_records')).rows,beforeLearning);
        assert.equal((await db.query('select count(*) n from tutorial_changes')).rows[0].n,3);
        assert.equal((await db.query('select count(*) n from problem_catalog')).rows[0].n,993);
    } finally { await db.close(); }
});

async function localOwnerGuard(db) {
    const names=['admin_save_tutorial','admin_store_learning_tutorial','admin_publish_tutorial_draft',
        'validate_tutorial_body','validate_tutorial_publication','refresh_tutorial_media_references','check_tutorial_media_exists'];
    const functions=(await db.query(`select p.oid::regprocedure::text signature,md5(pg_get_functiondef(p.oid)) definition_md5,proacl::text acl
        from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname=any($1) order by p.proname`,[names])).rows;
    const catalog_triggers=(await db.query(`select jsonb_agg(pg_get_triggerdef(oid) order by tgname) value from pg_trigger
        where tgrelid='public.tutorial_catalog'::regclass and not tgisinternal`)).rows[0].value;
    const draft_fingerprint=(await db.query(`select md5(coalesce(jsonb_agg(to_jsonb(d) order by tutorial_id,editor_id)::text,'[]')) value
        from tutorial_drafts d where tutorial_id in ('binary-search','dynamic-programming','greedy')`)).rows[0].value;
    return {functions,catalog_triggers,draft_fingerprint};
}

test('separately proposed owner publication is atomic, guarded and leaves drafts, Mongolia, bank and progress untouched', async()=>{
    const {ownerPublicationSql}=await import('../tools/package02_owner_publication.mjs');
    const {db}=await foundationDatabase();
    try {
        const batch=JSON.parse(fs.readFileSync('audit/PACKAGE02-FOUNDATION-PUBLISH-BATCH01.json'));
        await db.query(`insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)
            select id,'00000000-0000-0000-0000-000000000002',body||'{"_draftRelationsText":"retained private fixture"}',1,5
            from tutorial_catalog where id='binary-search'`);
        const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,
            drafts:(await db.query('select * from tutorial_drafts')).rows,history:(await db.query('select * from tutorial_changes')).rows,
            progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows,
            problems:(await db.query('select * from problem_catalog order by number')).rows});
        const before=await snapshot(),guard=await localOwnerGuard(db),sql=ownerPublicationSql(batch,guard);
        const fail=sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected late failure';");
        await assert.rejects(db.exec(fail),/Injected late failure/);
        assert.deepEqual(await snapshot(),before);
        await db.query("update tutorial_drafts set revision=revision+1 where tutorial_id='binary-search'");
        await assert.rejects(db.exec(sql),/Private draft changed/);
        assert.deepEqual((await snapshot()).catalog,before.catalog);
        await db.query("update tutorial_drafts set revision=revision-1 where tutorial_id='binary-search'");
        await db.exec(sql);
        const after=await snapshot();
        assert.deepEqual(after.drafts,before.drafts);assert.deepEqual(after.problems,before.problems);
        assert.deepEqual(after.progress,before.progress);assert.deepEqual(after.learning,before.learning);
        const wanted=new Set(batch.targets.map(t=>t.id));
        assert.deepEqual(after.catalog.filter(t=>!wanted.has(t.id)),before.catalog.filter(t=>!wanted.has(t.id)));
        assert.equal(after.history.length,3);assert.ok(after.history.every(h=>h.actor_id===null&&h.revision===6));
        for(const target of batch.targets)assert.deepEqual(after.catalog.find(t=>t.id===target.id).body,target.body);
        await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
        assert.deepEqual(await snapshot(),after);
    } finally { await db.close(); }
});
