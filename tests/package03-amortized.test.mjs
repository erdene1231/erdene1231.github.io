import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';import {mathProseWarnings} from '../math-prose.js';import {bodyHash} from '../tools/package02_tutorial_proposals.mjs';import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';import {ownerReviewedLessonsSql} from '../tools/package02_reviewed_publication.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/two-pointers.json'));
test('full chapter8 keeps source traces, explained exact code and old practice identity',()=>{
 validateTutorial(d.body);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.deepEqual(d.body.sections.map(s=>s.key),['two-pointers','nearest-smaller','sliding-minimum','practice']);
 // Roman I belongs to the official task title Subarray Sums I, not a bare variable.
 assert(mathProseWarnings(d.body).every(w=>w.variable==='I'&&/sections\[3\]\.blocks\[9\]/.test(w.path)));
 const names=['subarray','two-sum','three-sum','smaller','window'];
 for(const doc of[d.body,d.body.translations.en]){
  const all=doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17'));let previous=-1;
  for(const name of names){const source=fs.readFileSync(`audit/package03-work/amortized-${name}.cpp`,'utf8');const i=all.findIndex(b=>b.text===source);assert(i>previous,name);assert.equal(all.slice(previous+1,i).map(b=>b.text.trim()).join('\n').replace(/\s+/g,''),source.replace(/\s+/g,''),name);previous=i;}
  const figures=doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='diagram'));assert(figures.some(b=>b.rows[0].join(',')==='$1$,$3$,$2$,$5$,$1$,$1$,$2$,$3$'));assert(figures.some(b=>b.rows[0].join(',')==='$1$,$4$,$5$,$6$,$7$,$9$,$9$,$10$'));assert(figures.some(b=>b.rows[0].join(',')==='$1$,$3$,$4$,$2$,$5$,$3$,$4$,$2$'));assert(figures.some(b=>b.rows[0].join(',')==='$2$,$1$,$4$,$5$,$3$,$4$,$1$,$2$'));assert(!/the book|the source|Номын|Номд /i.test(JSON.stringify(doc)));
 }
 assert.deepEqual(d.body.learningRelations.practice.map(p=>p.key),['318','313','314','334','23','841','332']);
});
async function snapshot(db){const o={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])o[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return o;}
test('chapter8 publication with037validator is atomic, CAS guarded and preserves private drafts/progress/other lessons',async()=>{
 const{db}=await foundationDatabase();try{
  await db.exec('create role service_role;revoke all on function public.validate_tutorial_body(text,jsonb) from public;grant execute on function public.validate_tutorial_body(text,jsonb) to service_role;');await db.exec(fs.readFileSync('supabase/037-tutorial-grid-regions.sql','utf8'));
  const intro=JSON.parse(fs.readFileSync('audit/package03-prose-cleanup/introduction.json')).body;await db.query("insert into tutorial_catalog(id,body,revision,published)values('introduction',$1,2,true)",[intro]);const row=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='two-pointers'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values('two-pointers','00000000-0000-0000-0000-000000000002',$1,4,$2)",[row.body,row.revision]);
  const before=await snapshot(db),target={...d,expected_revision:row.revision,expected_body_md5:row.body_md5},guard={...await localOwnerGuard(db,['two-pointers']),catalog_count:57},sql=ownerReviewedLessonsSql({targets:[target]},guard);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected chapter8 failure';")),/Injected chapter8/);assert.deepEqual(await snapshot(db),before);await db.exec(sql);const after=await snapshot(db);for(const t of['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(r=>r.id!=='two-pointers'),before.tutorial_catalog.filter(r=>r.id!=='two-pointers'));assert.deepEqual(after.tutorial_catalog.find(r=>r.id==='two-pointers').body,d.body);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
