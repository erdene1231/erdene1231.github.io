import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {mathProseWarnings} from '../math-prose.js';
import {bodyHash} from '../tools/package02_tutorial_proposals.mjs';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
import {ownerReviewedLessonsSql} from '../tools/package02_reviewed_publication.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/greedy.json'));
const codes=doc=>doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17'));
test('full Greedy chapter is bilingual native content with exact explained code and source examples',()=>{
 validateTutorial(d.body);assert.deepEqual(mathProseWarnings(d.body),[]);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.deepEqual(d.body.sections.map(s=>s.key),['coins','scheduling','deadlines','minimizing-sums','compression','practice']);assert.deepEqual(d.body.learningRelations.practice.map(p=>p.key),['301','317','314','330','338','712','320','107','329','331']);assert.equal(d.body.learningRelations.next,'dynamic-programming');
 for(const doc of[d.body,d.body.translations.en]){
  for(const[name,si]of[['coins',0],['events',1],['deadlines',2],['sums',3],['huffman',4]]){
   const source=fs.readFileSync(`audit/package03-work/greedy-${name}.cpp`,'utf8');const parts=doc.sections[si].blocks.filter(b=>b.type==='code'&&b.language==='C++17');assert.equal(parts.at(-1).text,source);assert(parts.length>=4);assert.equal(parts.slice(0,-1).map(b=>b.text.trim()).join('\n').replace(/\s+/g,''),source.replace(/\s+/g,''));
  }
  const prose=JSON.stringify(doc);for(const token of['520','99','200','111','1011','AABACDACA','15','18','46','12','Huffman'])assert(prose.includes(token),token);assert(!/Номын|Номд |the book|the source|CC BY-NC-SA|2018 edition/i.test(prose));assert.equal(doc.sections[4].blocks.filter(b=>b.type==='diagram').length,4);
 }
});
async function snapshot(db){const out={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])out[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return out;}
test('Greedy replacement is atomic, stale/replay guarded and preserves all other rows/private edits/progress',async()=>{
 const{db}=await foundationDatabase();try{
  const intro=JSON.parse(fs.readFileSync('audit/package03-prose-cleanup/introduction.json')).body;await db.query("insert into tutorial_catalog(id,body,revision,published)values('introduction',$1,2,true)",[intro]);const row=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='greedy'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values('greedy','00000000-0000-0000-0000-000000000002',$1,4,$2)",[row.body,row.revision]);
  const before=await snapshot(db);const target={...d,expected_revision:row.revision,expected_body_md5:row.body_md5};const guard={...await localOwnerGuard(db,['greedy']),catalog_count:57};const sql=ownerReviewedLessonsSql({targets:[target]},guard);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected greedy failure';")),/Injected greedy/);assert.deepEqual(await snapshot(db),before);
  await db.exec(sql);const after=await snapshot(db);for(const t of['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(r=>r.id!=='greedy'),before.tutorial_catalog.filter(r=>r.id!=='greedy'));assert.deepEqual(after.tutorial_catalog.find(r=>r.id==='greedy').body,d.body);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
