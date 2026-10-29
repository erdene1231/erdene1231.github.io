import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
import {introductionPublicationSql} from '../tools/package03_introduction_publication.mjs';
import {validateTutorial} from '../tutorial-model.js';import{publicationBody}from'../tutorial-publication.js';import{bodyHash,proposalProblems}from'../tools/package02_tutorial_proposals.mjs';import{mathProseWarnings}from'../math-prose.js';
const candidate=JSON.parse(fs.readFileSync('audit/package03-lessons/introduction.json'));
test('chapter 1 keeps its six source subtopics, mathematical examples, code and practice in native bilingual content',()=>{
 const body=candidate.body;validateTutorial(body);assert.equal(bodyHash(body),candidate.reviewed_body_sha256);assert.deepEqual(mathProseWarnings(body),[]);assert.deepEqual(publicationBody(body,[body,{id:'complexity'}],proposalProblems()),body);
 assert.deepEqual(body.sections.map(s=>s.key),['programming-languages','input-output','numbers','shortening-code','mathematics','contests-resources','practice']);
 for(const doc of[body,body.translations.en]){
  const text=JSON.stringify(doc);for(const value of['123 456 monkey','123456789','987654321','SQ_BAD','SQ_BOOK','32','16','1111011','133','Programming Challenges','Yandex.Algorithm'])assert(text.includes(value),value);
  const math=doc.sections[4].blocks;assert.equal(math.find(b=>b.type==='table').rows.length,4);assert(math.some(b=>b.tex?.includes('sqrt5')));assert(math.some(b=>b.tex?.includes('H_6')));assert.equal(doc.sections[6].blocks.filter(b=>b.type==='problem').length,6);
  for(const name of['io','mod','square','sequences','digits']){
   const full=fs.readFileSync('audit/package03-work/introduction-'+name+'.cpp','utf8');assert(doc.sections.some(s=>s.blocks.some(b=>b.language==='C++17'&&b.text===full)));
  }
 }
 assert.deepEqual(JSON.parse(fs.readFileSync('curriculum.json')).order.slice(0,2),['introduction','complexity']);assert.equal(body.learningRelations.next,'complexity');
});
async function guard(db){const g=await localOwnerGuard(db);return{...g,...(await db.query(`select (select count(*)::int from tutorial_catalog) catalog_count,(select md5(jsonb_agg(to_jsonb(t) order by id)::text)from tutorial_catalog t)catalog_fingerprint,(select md5(coalesce(jsonb_agg(to_jsonb(d)order by tutorial_id,editor_id)::text,'[]'))from tutorial_drafts d)all_drafts_fingerprint`)).rows[0]};}
async function snapshot(db){const x={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records','problem_catalog'])x[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return x;}
test('new introduction publication is atomic, rejects replay/drift, and preserves existing lessons, drafts and progress',async()=>{
 const{db}=await foundationDatabase();try{
  await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)select 'complexity','00000000-0000-0000-0000-000000000002',body,10,revision from tutorial_catalog where id='complexity'");
  const before=await snapshot(db),g=await guard(db),sql=introductionPublicationSql(candidate,g);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: catalog and initial history exist together.',"RAISE EXCEPTION 'Injected insertion failure';")),/Injected insertion/);assert.deepEqual(await snapshot(db),before);
  const stale=introductionPublicationSql(candidate,{...g,catalog_fingerprint:'0'.repeat(32)});await assert.rejects(db.exec(stale),/Catalog drift/);assert.deepEqual(await snapshot(db),before);
  await db.exec(sql);const after=await snapshot(db);for(const t of ['tutorial_drafts','progress','learning_records','problem_catalog'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(t=>t.id!=='introduction'),before.tutorial_catalog);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);assert.deepEqual(after.tutorial_catalog.find(t=>t.id==='introduction').body,candidate.body);
  await assert.rejects(db.exec(sql),/identity already used/);
 }finally{await db.close();}
});
test('new introduction cannot resurrect a tombstone or bypass publication validation',async()=>{
 const{db}=await foundationDatabase();try{
  await db.query("insert into tutorial_deleted_ids values('introduction')");await assert.rejects(db.exec(introductionPublicationSql(candidate,await guard(db))),/identity already used/);await db.query("delete from tutorial_deleted_ids where id='introduction'");
  const bad=structuredClone(candidate);bad.body.sections[6].blocks.push({type:'problem',problemKey:'99999999'});bad.reviewed_body_sha256=bad.proposed_body_sha256=bodyHash(bad.body);await assert.rejects(db.exec(introductionPublicationSql(bad,await guard(db))),/Unknown embedded problem/);assert.equal((await db.query("select count(*)::int n from tutorial_catalog where id='introduction'")).rows[0].n,0);
 }finally{await db.close();}
});
