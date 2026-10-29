import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {mathProseWarnings} from '../math-prose.js';
import {bodyHash} from '../tools/package02_tutorial_proposals.mjs';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
import {ownerReviewedLessonsSql} from '../tools/package02_reviewed_publication.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/dynamic-programming.json'));
const codes=doc=>doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17'));
test('full chapter7 retains source states/examples, exact fragments and existing practice',()=>{
 validateTutorial(d.body);assert.deepEqual(mathProseWarnings(d.body),[]);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.deepEqual(d.body.sections.map(s=>s.key),['coins','lis','grid','knapsack','edit-distance','tilings','practice']);assert.deepEqual(d.body.learningRelations.practice.map(p=>p.key),['340','677','679','684','346','915','341','342','343','344','111']);
 const names=['min-coins','count-coins','lis','grid','knapsack','edit','tilings','tiling-formula'];const sources=names.map(n=>fs.readFileSync(`audit/package03-work/dp-${n}.cpp`,'utf8'));
 for(const doc of[d.body,d.body.translations.en]){
  const all=codes(doc);let previous=-1;for(const source of sources){const i=all.findIndex(b=>b.text===source);assert(i>previous);assert.equal(all.slice(previous+1,i).map(b=>b.text.trim()).join('\n').replace(/\s+/g,''),source.replace(/\s+/g,''));previous=i;}
  assert(!/Номын|Номд |the book|the source|CC BY-NC-SA/i.test(JSON.stringify(doc)));
  const diagrams=doc.sections.flatMap(s=>s.blocks.filter(b=>b.type==='diagram'));for(const fig of diagrams)if(fig.rows)assert(fig.rows.every(r=>r.length===fig.rows[0].length),'rectangular diagrams');
  const tile=doc.sections[5].blocks.find(b=>b.type==='diagram').rows;const seen=new Map();tile.forEach((row,r)=>row.forEach((v,c)=>{if(!seen.has(v))seen.set(v,[]);seen.get(v).push([r,c]);}));assert.equal(seen.size,14);for(const cells of seen.values()){assert.equal(cells.length,2);assert.equal(Math.abs(cells[0][0]-cells[1][0])+Math.abs(cells[0][1]-cells[1][1]),1);}
  const text=JSON.stringify(doc);for(const token of['781','67','LOVE','MOVIE','3,3,4'])assert(text.includes(token),token);
 }
});
async function snapshot(db){const out={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])out[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return out;}
test('Dynamic programming replacement is atomic, stale/replay guarded and preserves all other rows/private edits/progress',async()=>{
 const{db}=await foundationDatabase();try{
  const intro=JSON.parse(fs.readFileSync('audit/package03-prose-cleanup/introduction.json')).body;await db.query("insert into tutorial_catalog(id,body,revision,published)values('introduction',$1,2,true)",[intro]);const row=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='dynamic-programming'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values('dynamic-programming','00000000-0000-0000-0000-000000000002',$1,4,$2)",[row.body,row.revision]);
  const before=await snapshot(db);const target={...d,expected_revision:row.revision,expected_body_md5:row.body_md5};const guard={...await localOwnerGuard(db,['dynamic-programming']),catalog_count:57};const sql=ownerReviewedLessonsSql({targets:[target]},guard);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected DP failure';")),/Injected DP/);assert.deepEqual(await snapshot(db),before);
  await db.exec(sql);const after=await snapshot(db);for(const t of['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(r=>r.id!=='dynamic-programming'),before.tutorial_catalog.filter(r=>r.id!=='dynamic-programming'));assert.deepEqual(after.tutorial_catalog.find(r=>r.id==='dynamic-programming').body,d.body);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
