import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {mathProseWarnings} from '../math-prose.js';
import {bodyHash} from '../tools/package02_tutorial_proposals.mjs';
import {foundationDatabase,localOwnerGuard} from './package03-introduction-fixture.mjs';
import {ownerReviewedLessonsSql} from '../tools/package02_reviewed_publication.mjs';
const names=['introduction','complexity','sorting','set-map','brute-force'];
const docs=Object.fromEntries(names.map(id=>[id,JSON.parse(fs.readFileSync(`audit/package03-prose-cleanup/${id}.json`))]));
const text=b=>b.type==='rich'?b.content.map(r=>r.text).join(''):b.text||'';
const strings=d=>d.sections.flatMap(s=>s.blocks.filter(b=>b.type!=='code').map(text));
const code=d=>d.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'));
test('direct teaching corrections keep native documents, code and all lesson relationships',()=>{
 for(const id of names){const d=docs[id];validateTutorial(d.body);assert.deepEqual(mathProseWarnings(d.body),[]);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);
  for(const doc of[d.body,d.body.translations.en]){const prose=[...strings(doc),...doc.sections.flatMap(s=>s.blocks.map(b=>b.caption||''))];assert(!JSON.stringify(doc).includes('CC BY-NC-SA'));assert(!prose.some(t=>/Source: Antti|Эх сурвалж: Antti/.test(t)));for(const t of prose.filter(t=>!t.includes('CC BY-NC-SA')))assert(!/(?<!\p{L})(?:Номын|Номд |Ном |номын|номд |the book|the source|2018 оны эх сурвалж)/iu.test(t),`${id}: ${t}`);}
  if(id==='brute-force')continue;
  // The audit revision published before this correction is tracked in the established candidate.
  const old=JSON.parse(fs.readFileSync(`audit/package03-lessons/${id}.json`)).body;
  const metadata=body=>Object.fromEntries(Object.entries(body).filter(([k])=>!['sections','translations'].includes(k)));
  assert.deepEqual(metadata(d.body),metadata(old));assert.deepEqual(code(d.body),code(old));assert.deepEqual(code(d.body.translations.en),code(old.translations.en));
 }
});
test('Complete search preserves full chapter sequence, source examples and explained complete programs',()=>{
 const d=docs['brute-force'].body;assert.deepEqual(d.sections.map(s=>s.key),['subsets','permutations','backtracking','pruning','meet-in-the-middle','practice']);assert.deepEqual(d.learningRelations.practice.map(p=>p.key),['305','85','82','22','311','892']);
 for(const doc of[d,d.translations.en]){
  for(const name of['subsets','permutations','queens','grid','mitm'])assert(code(doc).some(b=>b.text===fs.readFileSync(`audit/package03-work/complete-search-${name}.cpp`,'utf8')),name);
  const prose=JSON.stringify(doc);for(const token of['11001','111712','14772512','234907967154122528','Horowitz','Sahni','483','244','119','221','69','15','10'])assert(prose.includes(token),token);
  for(const section of doc.sections.slice(0,5)){const blocks=section.blocks;const full=blocks.findLastIndex(b=>b.type==='code');assert(full>0);assert(blocks.slice(0,full).filter(b=>b.type==='code').length>=3);assert(blocks.slice(0,full).some(b=>['p','rich'].includes(b.type)));}
 }
});
async function snapshot(db){const out={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])out[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return out;}
test('five-lesson release uses two scoped atomic transactions; rollback, drafts, other rows and replay guards hold',async()=>{
 const {db}=await foundationDatabase();try{
  await db.query("insert into tutorial_catalog(id,body,revision,published)values('introduction',$1,1,true)",[docs.introduction.body]);
  for(const id of names){const row=(await db.query('select * from tutorial_catalog where id=$1',[id])).rows[0];await db.query('insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values($1,$2,$3,4,$4)',[id,'00000000-0000-0000-0000-000000000002',row.body,row.revision]);}
  for(const ids of[names.slice(0,3),names.slice(3)]){
   const before=await snapshot(db);const targets=[];for(const id of ids){const old=(await db.query('select *,md5(body::text) body_md5 from tutorial_catalog where id=$1',[id])).rows[0];targets.push({...docs[id],expected_revision:old.revision,expected_body_md5:old.body_md5});}
   const sql=ownerReviewedLessonsSql({targets},{...await localOwnerGuard(db,[...ids].sort()),catalog_count:57});
   await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected release failure';")),/Injected release failure/);assert.deepEqual(await snapshot(db),before);
   await db.exec(sql);const after=await snapshot(db);for(const t of['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[t],before[t]);assert.deepEqual(after.tutorial_catalog.filter(r=>!ids.includes(r.id)),before.tutorial_catalog.filter(r=>!ids.includes(r.id)));assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+ids.length);for(const id of ids)assert.deepEqual(after.tutorial_catalog.find(r=>r.id===id).body,docs[id].body);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
  }
 }finally{await db.close();}
});
