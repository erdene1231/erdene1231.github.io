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

test('rewritten revision-6 replacements validate through native lifecycle, preserve unrelated data and reject replay/drift atomically', async()=>{
    const {ownerPublicationSql,ownerReplacementSql}=await import('../tools/package02_owner_publication.mjs');
    const {bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
    const {db}=await foundationDatabase();
    try {
        await db.query(`insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)
            select id,'00000000-0000-0000-0000-000000000002',body,1,5 from tutorial_catalog where id='binary-search'`);
        await db.exec(ownerPublicationSql(JSON.parse(fs.readFileSync('audit/PACKAGE02-FOUNDATION-PUBLISH-BATCH01.json')),await localOwnerGuard(db)));
        const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,
            drafts:(await db.query('select * from tutorial_drafts')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,
            progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows,
            problems:(await db.query('select * from problem_catalog order by number')).rows});
        const before=await snapshot(),targets=[];
        for(const id of ['binary-search','greedy','dynamic-programming']){
            const candidate=JSON.parse(fs.readFileSync(`audit/package02-rewrite/${id}.json`));
            const live=(await db.query('select md5(body::text) hash from tutorial_catalog where id=$1',[id])).rows[0];
            targets.push({...candidate,expected_body_md5:live.hash,expected_published:true,proposed_body_sha256:bodyHash(candidate.body)});
        }
        const batch={targets},guard=await localOwnerGuard(db),sql=ownerReplacementSql(batch,guard);
        assert.throws(()=>ownerPublicationSql(batch,guard),/payload guard/);
        await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected replacement failure';")),/Injected replacement failure/);
        assert.deepEqual(await snapshot(),before);
        await db.query("update tutorial_catalog set revision=revision+1 where id='greedy'");
        await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
        assert.deepEqual((await snapshot()).catalog.find(t=>t.id==='binary-search'),before.catalog.find(t=>t.id==='binary-search'));
        await db.query("update tutorial_catalog set revision=revision-1 where id='greedy'");
        await db.exec(sql);
        const after=await snapshot(),wanted=new Set(targets.map(t=>t.id));
        for(const key of ['drafts','progress','learning','problems'])assert.deepEqual(after[key],before[key]);
        assert.deepEqual(after.catalog.filter(t=>!wanted.has(t.id)),before.catalog.filter(t=>!wanted.has(t.id)));
        assert.deepEqual(after.history.slice(0,3),before.history);assert.equal(after.history.length,6);
        for(const target of targets){const row=after.catalog.find(t=>t.id===target.id);assert.equal(row.revision,7);assert.deepEqual(row.body,target.body);}
        await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);assert.deepEqual(await snapshot(),after);
    } finally {await db.close();}
});

test('small reviewed lesson publication freezes exact scope/review hashes and preserves existing private work', async()=>{
    const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs');
    const {bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
    const {db,problems}=await foundationDatabase();
    try {
        const candidate=JSON.parse(fs.readFileSync('audit/package02-lessons/complexity.json'));
        const initial=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='complexity'")).rows[0];
        assert.equal(initial.revision,candidate.expected_revision);assert.equal(bodyHash(initial.body),candidate.expected_body_sha256);
        await db.query(`insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)
            select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in ('complexity','binary-search')`);
        const topics=(await db.query('select body from tutorial_catalog')).rows.map(r=>r.body.id==='complexity'?candidate.body:r.body);
        assert.deepEqual(publicationBody(candidate.body,topics,problems),candidate.body);
        const target={...candidate,expected_body_md5:initial.body_md5,proposed_body_sha256:bodyHash(candidate.body),reviewed_body_sha256:bodyHash(candidate.body)};
        const guard=await localOwnerGuard(db,['complexity']),batch={targets:[target]},sql=ownerReviewedLessonsSql(batch,guard);
        assert.throws(()=>ownerReviewedLessonsSql(batch,{...guard,scope_ids:['binary-search']}),/exact reviewed scope/);
        assert.throws(()=>ownerReviewedLessonsSql({targets:[{...target,reviewed_body_sha256:'0'.repeat(64)}]},guard),/payload guard/);
        assert.throws(()=>ownerReviewedLessonsSql({targets:[target,target]},guard),/unique allowlist/);
        assert.throws(()=>ownerReviewedLessonsSql({targets:[{...target,id:'mongolia'}]},guard),/unique allowlist/);
        const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
        const before=await snapshot();
        await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected lesson failure';")),/Injected lesson failure/);assert.deepEqual(await snapshot(),before);
        await db.query("update tutorial_drafts set revision=revision+1 where tutorial_id='complexity'");await assert.rejects(db.exec(sql),/Private draft changed/);await db.query("update tutorial_drafts set revision=revision-1 where tutorial_id='complexity'");
        await db.exec(sql);const after=await snapshot();
        for(const key of ['drafts','progress','learning'])assert.deepEqual(after[key],before[key]);
        assert.deepEqual(after.catalog.filter(t=>t.id!=='complexity'),before.catalog.filter(t=>t.id!=='complexity'));
        const current=after.catalog.find(t=>t.id==='complexity');assert.equal(current.revision,initial.revision+1);assert.deepEqual(current.body,candidate.body);assert.equal(after.history.length,1);
        await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);assert.deepEqual(await snapshot(),after);
    } finally {await db.close();}
});

test('two finished prerequisite lessons publish atomically with exact separate draft guards and native lifecycle checks',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  const targets=[];for(const id of ['brute-force','sorting']){const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);targets.push({...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)});}
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id='brute-force'");
  const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
  const before=await snapshot(),guard=await localOwnerGuard(db,['brute-force','sorting']),sql=ownerReviewedLessonsSql({targets},guard);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected paired lesson failure';")),/Injected paired lesson failure/);assert.deepEqual(await snapshot(),before);
  await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(r=>!['brute-force','sorting'].includes(r.id)),before.catalog.filter(r=>!['brute-force','sorting'].includes(r.id)));
  for(const t of targets){const r=after.catalog.find(r=>r.id===t.id);assert.equal(r.revision,t.expected_revision+1);assert.deepEqual(r.body,t.body);}assert.equal(after.history.length,2);
  await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);assert.deepEqual(await snapshot(),after);
 }finally{await db.close();}
});

test('recursion and prefix sums each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in('recursion','binary-search')");
  for(const id of ['recursion','prefix-sums']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('sorting replacement and contextual terminology corrections retain private drafts and other live documents',async()=>{
 const{ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');const{db}=await foundationDatabase();try{
 for(const id of ['sorting','binary-search','greedy']){
  const initial=JSON.parse(fs.readFileSync(id==='sorting'?'audit/package02-lessons/sorting.json':`audit/package02-rewrite/${id}.json`)).body;
  const d=JSON.parse(fs.readFileSync(`audit/package02-revisions/${id==='sorting'?'sorting-recursive':id+'-terminology'}.json`));assert.equal(bodyHash(initial),d.expected_body_sha256);
  await db.query('update tutorial_catalog set body=$2,revision=$3 where id=$1',[id,initial,d.expected_revision]);
 }
 await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,3,5 from tutorial_catalog where id='binary-search'");
 for(const id of ['sorting','binary-search','greedy']){
  const d=JSON.parse(fs.readFileSync(`audit/package02-revisions/${id==='sorting'?'sorting-recursive':id+'-terminology'}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0],g=await localOwnerGuard(db,[id]);
  const t={...d,expected_body_md5:old.body_md5,reviewed_body_sha256:bodyHash(d.body),proposed_body_sha256:bodyHash(d.body)},sql=ownerReviewedLessonsSql({targets:[t]},g),before=(await db.query('select * from tutorial_catalog order by id')).rows,drafts=(await db.query('select * from tutorial_drafts')).rows;
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected revised content failure';")),/Injected revised content/);assert.deepEqual((await db.query('select * from tutorial_catalog order by id')).rows,before);
  await db.exec(sql);assert.deepEqual((await db.query('select * from tutorial_drafts')).rows,drafts);const after=(await db.query('select * from tutorial_catalog order by id')).rows;assert.deepEqual(after.filter(t=>t.id!==id),before.filter(t=>t.id!==id));assert.deepEqual(after.find(t=>t.id===id).body,d.body);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }
 }finally{await db.close();}
});

test('difference and two pointers each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in('difference-array','binary-search')");
  for(const id of ['difference-array','two-pointers']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('2D prefix and positive-window lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in('prefix-sums-2d','binary-search')");
  for(const id of ['prefix-sums-2d','sliding-window']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Stack/queue and set/map lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in('stack-queue','binary-search')");
  for(const id of ['stack-queue','set-map']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Bit operations and gcd lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in('bit-operations','binary-search')");
  for(const id of ['bit-operations','gcd']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Modular power and sieve lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body,1,revision from tutorial_catalog where id in('fast-power','binary-search')");
  for(const id of ['fast-power','sieve']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Graph components and shortest-path BFS lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('graph-basics','binary-search')");
  for(const id of ['graph-basics','bfs']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Explicit DFS and grid regions lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('dfs','binary-search')");
  for(const id of ['dfs','flood-fill']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Answer search and compression lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('binary-search-answer','binary-search')");
  for(const id of ['binary-search-answer','hash-compression']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Rooted tree and grid paths lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('tree-basics','binary-search')");
  for(const id of ['tree-basics','grid-dp']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];assert.equal(old.revision,d.expected_revision);assert.equal(bodyHash(old.body),d.expected_body_sha256);
   const target={...d,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Knapsack and DSU lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('knapsack','binary-search')");
  for(const id of ['knapsack','dsu']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('LIS and Kruskal lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('lis','binary-search')");
  for(const id of ['lis','kruskal']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Interval DP and priority queue lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('interval-dp','binary-search')");
  for(const id of ['interval-dp','priority-queue']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Dijkstra and topological sort lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('dijkstra','binary-search')");
  for(const id of ['dijkstra','topological-sort']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Bellman-Ford and Floyd-Warshall lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('bellman-ford','binary-search')");
  for(const id of ['bellman-ford','floyd-warshall']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Fenwick and segment tree lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('fenwick-tree','binary-search')");
  for(const id of ['fenwick-tree','segment-tree']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Sparse table and lazy segment tree lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('sparse-table','binary-search')");
  for(const id of ['sparse-table','lazy-segment-tree']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Bitmask and tree DP lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('bitmask-dp','binary-search')");
  for(const id of ['bitmask-dp','tree-dp']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('KMP and string hashing lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('kmp','binary-search')");
  for(const id of ['kmp','string-hashing']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Components and bipartite coloring lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('connected-components','binary-search')");
  for(const id of ['connected-components','bipartite']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('Lower and upper boundary lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('lower-bound','binary-search')");
  for(const id of ['lower-bound','upper-bound']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});

test('LCA and monotonic stack lessons each publish as an individually guarded native document',async()=>{
 const {ownerReviewedLessonsSql}=await import('../tools/package02_reviewed_publication.mjs'),{bodyHash}=await import('../tools/package02_tutorial_proposals.mjs');
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision) select id,'00000000-0000-0000-0000-000000000002',body||jsonb_build_object('summary',(body->>'summary')||' private preserved'),1,revision from tutorial_catalog where id in('monotonic-stack','binary-search')");
  for(const id of ['lca','monotonic-stack']){
   const d=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)),old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];await db.query('update tutorial_catalog set revision=$2 where id=$1',[id,d.expected_revision]);old.revision=d.expected_revision;const prepared={...d,expected_body_sha256:bodyHash(old.body)};
   const target={...prepared,expected_body_md5:old.body_md5,proposed_body_sha256:bodyHash(d.body),reviewed_body_sha256:bodyHash(d.body)},g=await localOwnerGuard(db,[id]),sql=ownerReviewedLessonsSql({targets:[target]},g);
   const snapshot=async()=>({catalog:(await db.query('select * from tutorial_catalog order by id')).rows,drafts:(await db.query('select * from tutorial_drafts order by tutorial_id')).rows,history:(await db.query('select * from tutorial_changes order by change_id')).rows,progress:(await db.query('select * from progress')).rows,learning:(await db.query('select * from learning_records')).rows});
   const before=await snapshot();await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"raise exception 'Injected individual publication failure';")),/Injected individual/);assert.deepEqual(await snapshot(),before);
   await db.exec(sql);const after=await snapshot();for(const k of ['drafts','progress','learning'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.catalog.filter(t=>t.id!==id),before.catalog.filter(t=>t.id!==id));assert.deepEqual(after.catalog.find(t=>t.id===id).body,d.body);assert.equal(after.history.length,before.history.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});
