import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';import {mathProseWarnings} from '../math-prose.js';import {bodyHash} from '../tools/package02_tutorial_proposals.mjs';import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';import {ownerReviewedLessonsSql} from '../tools/package02_reviewed_publication.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/segment-tree.json'));
test('full chapter9 retains source subtopics/states, exact compiled fragments, recursive main tree and old practice',()=>{
 validateTutorial(d.body);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.deepEqual(mathProseWarnings(d.body),[]);assert.deepEqual(d.body.sections.map(s=>s.key),['static','fenwick','segment','additional','practice']);assert.deepEqual(d.body.learningRelations.practice.map(p=>p.key),['397','398','402','403','409','406']);
 const names=['static','prefix2d','fenwick','recursive','iterative','minimum','compression','difference'];
 for(const doc of[d.body,d.body.translations.en]){
  const all=doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17'));let prev=-1;
  for(const name of names){const src=fs.readFileSync(`audit/package03-work/range-${name}.cpp`,'utf8');const i=all.findIndex(b=>b.text===src);assert(i>prev,name);assert.equal(all.slice(prev+1,i).map(b=>b.text.trim()).join('\n').replace(/\s+/g,''),src.replace(/\s+/g,''),name);prev=i;}
  assert(!/the book|the source|Номын|Номд /i.test(JSON.stringify(doc)));
  const arrays=doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='diagram'&&b.kind==='array'));for(const values of[[1,3,8,4,6,1,3,4],[1,3,4,8,6,1,4,2],[1,4,8,16,22,23,27,29],[1,4,4,16,6,7,4,29],[3,3,1,1,1,5,2,2],[3,0,-2,0,0,4,-3,0],[3,5,-2,0,0,-1,-3,0]])assert(arrays.some(a=>JSON.stringify(a.rows[0])===JSON.stringify(values.map(v=>`$${v}$`))),values.join(','));
  const graphs=doc.sections[2].blocks.filter(b=>b.type==='diagram'&&b.kind==='tree');assert.equal(graphs.length,4);assert.equal(graphs[0].nodes.find(n=>n.id==='1').label,'39');assert.equal(graphs[3].nodes.find(n=>n.id==='1').label,'1');assert.equal(graphs[0].nodes.length,15);
  const matrix=doc.sections[0].blocks.find(b=>b.gridPresentation);assert.equal(matrix.gridPresentation.colors.length,12);assert.equal(matrix.rows[1][1],'$D$');assert.equal(matrix.rows[4][5],'$A$');
  assert(doc.sections[0].blocks.some(b=>b.type==='table'&&b.rows.length===21));
  for(const b of doc.sections.flatMap(s=>s.blocks))for(const text of [b.text,...(b.content||[]).map(c=>c.text)])if(typeof text==='string')assert(!/[\x00-\x08\x0b-\x1f]/.test(text),'no escaped TeX control corruption');
 }
});
async function snapshot(db){const o={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])o[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return o;}
test('chapter9 publication with037 preserves private drafts/progress/focused lessons and rejects failure/replay',async()=>{
 const{db}=await foundationDatabase();try{
  await db.exec('create role service_role;revoke all on function public.validate_tutorial_body(text,jsonb) from public;grant execute on function public.validate_tutorial_body(text,jsonb) to service_role;');await db.exec(fs.readFileSync('supabase/037-tutorial-grid-regions.sql','utf8'));
  const intro=JSON.parse(fs.readFileSync('audit/package03-prose-cleanup/introduction.json')).body;await db.query("insert into tutorial_catalog(id,body,revision,published)values('introduction',$1,2,true)",[intro]);const row=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='segment-tree'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values('segment-tree','00000000-0000-0000-0000-000000000002',$1,4,$2)",[row.body,row.revision]);
  const before=await snapshot(db),target={...d,expected_revision:row.revision,expected_body_md5:row.body_md5},guard={...await localOwnerGuard(db,['segment-tree']),catalog_count:57},sql=ownerReviewedLessonsSql({targets:[target]},guard);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected chapter9 failure';")),/Injected chapter9/);assert.deepEqual(await snapshot(db),before);await db.exec(sql);const after=await snapshot(db);for(const t of['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(r=>r.id!=='segment-tree'),before.tutorial_catalog.filter(r=>r.id!=='segment-tree'));assert.deepEqual(after.tutorial_catalog.find(r=>r.id==='segment-tree').body,d.body);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
