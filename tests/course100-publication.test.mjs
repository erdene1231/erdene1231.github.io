import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
import{setupPublicationSql}from'../tools/course100_publication.mjs';import{bodyHash}from'../tools/package02_tutorial_proposals.mjs';
const bodies=JSON.parse(fs.readFileSync('audit/course100-v2/setup-tutorials.json'));
test('three-lesson publication is guarded, atomic, preserves existing content and rejects replay',async()=>{
 const{db}=await foundationDatabase();try{
 await db.exec('create role service_role');for(const f of JSON.parse(fs.readFileSync('audit/course100-v2/validator-baseline.json'))){await db.exec(f.definition);await db.exec(`revoke all on function public.${f.signature} from public,anon,authenticated;grant execute on function public.${f.signature} to service_role`);}await db.exec(fs.readFileSync('supabase/041-native-tutorial-quiz-assets.sql','utf8'));
 const before=(await db.query('select *from tutorial_catalog order by id')).rows;
 const g={...await localOwnerGuard(db),...(await db.query("select count(*)::int catalog_count,md5(jsonb_agg(to_jsonb(t)order by id)::text)catalog_fingerprint from tutorial_catalog t")).rows[0],...(await db.query("select md5(coalesce(jsonb_agg(to_jsonb(d)order by tutorial_id,editor_id)::text,'[]'))all_drafts_fingerprint from tutorial_drafts d")).rows[0],reviewed_hashes:Object.fromEntries(bodies.map(b=>[b.id,bodyHash(b)])),protected_sql:"select md5('protected-fixture')",protected_fingerprint:(await db.query("select md5('protected-fixture')h")).rows[0].h};
 const sql=setupPublicationSql(bodies,g);assert.throws(()=>setupPublicationSql([...bodies,bodies[0]],g),/scope/);
 await assert.rejects(db.exec(setupPublicationSql(bodies,{...g,catalog_fingerprint:'0'.repeat(32)})),/Catalog drift/);
 await assert.rejects(db.exec(sql.replace('-- Atomic preservation boundary, including all previous private and public content.',"RAISE EXCEPTION 'Injected failure';")),/Injected failure/);assert.deepEqual((await db.query('select *from tutorial_catalog order by id')).rows,before);
 await db.exec(sql);assert.deepEqual((await db.query("select *from tutorial_catalog where id not like 'cpp-%' order by id")).rows,before);for(const b of bodies)assert.deepEqual((await db.query('select body from tutorial_catalog where id=$1',[b.id])).rows[0].body,b);
 await assert.rejects(db.exec(sql),/identity used/);
 }finally{await db.close();}
});
