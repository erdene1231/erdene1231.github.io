import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import{validateTutorial}from'../tutorial-model.js';import{mathProseWarnings}from'../math-prose.js';import{bodyHash,proposalProblems}from'../tools/package02_tutorial_proposals.mjs';import{publicationBody}from'../tutorial-publication.js';import{foundationDatabase,localOwnerGuard}from'./package03-introduction-fixture.mjs';import{ownerReviewedLessonsSql}from'../tools/package02_reviewed_publication.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/lca.json')),old=JSON.parse(fs.readFileSync('audit/package03-preserved/lca-before-chapter18.json'));
test('chapter18 source examples, LCA-first static aggregates and all six explained programs',()=>{
 validateTutorial(d.body);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.deepEqual(mathProseWarnings(d.body),[]);publicationBody(d.body,[d.body,...JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials.filter(r=>r.id!=='lca').map(r=>r.body)],proposalProblems());
 assert.deepEqual(d.body.sections.map(s=>s.key),['lca-first','ancestors','static-paths','subtrees-paths','euler-rmq','offline-merging','offline-lca','practice']);
 for(const k of Object.keys(old.body).filter(k=>!['title','summary','sections','translations'].includes(k)))assert.deepEqual(d.body[k],old.body[k],k);
 const parts=JSON.parse(fs.readFileSync('audit/package03-work/tree-query-code-parts.json'));
 for(const doc of[d.body,d.body.translations.en]){
  const all=doc.sections.flatMap(s=>s.blocks),codes=all.filter(b=>b.type==='code'),graphs=all.filter(b=>b.type==='diagram'&&b.kind==='graph');assert.equal(graphs.length,11);
  let prev=-1;for(const name of['basic','aggregate','dynamic','rmq','merge','offline']){const src=fs.readFileSync(`audit/package03-work/tree-query-${name}.cpp`,'utf8'),i=codes.findIndex(c=>c.text===src);assert(i>prev);assert.deepEqual(codes.slice(i-parts[name].length,i).map(c=>c.text),parts[name].map(p=>p.trim()));assert.equal(parts[name].join(''),src);prev=i;}
  assert.deepEqual(graphs[0].edges,[['1','2'],['1','3'],['1','4'],['2','5'],['2','6'],['6','8'],['4','7']]);assert.deepEqual(graphs[1].edges,[['1','4'],['1','5'],['1','2'],['4','3'],['4','7'],['7','8'],['2','6']]);
  assert.deepEqual(graphs[3].edgeStyles.map(e=>e.label),['4','-2','7','5','3','-1','6']);assert.deepEqual(graphs[4].nodes.map(n=>n.annotation),['10','2','5','7','4','3','6','8']);
  assert.deepEqual(graphs[5].nodes.map(n=>n.annotation),['2','3','5','3','1','4','4','3','1']);assert.deepEqual(graphs[6].nodes.map(n=>n.annotation),['4','5','3','5','2','3','5','3','1']);
  const tables=doc.sections[3].blocks.filter(b=>b.type==='table');assert.deepEqual(tables[0].rows.map(r=>r[1]),['1','2','6','3','4','7','8','9','5']);assert.deepEqual(tables[1].rows.map(r=>r[3]),['4','9','12','7','10','15','13','11','6']);
  const euler=doc.sections[4].blocks.find(b=>b.type==='table');assert.deepEqual(euler.rows.map(r=>r[1]),['1','2','5','2','6','8','6','2','1','3','1','4','7','4','1']);assert.deepEqual(euler.rows.map(r=>r[2]),['1','2','3','2','3','4','3','2','1','2','1','2','3','2','1']);
  assert(!/the book|the source says|Номын|Номд /i.test(JSON.stringify(doc)));assert.deepEqual(all.filter(b=>b.type==='problem').map(b=>b.problemKey),['425','426','427','428','430','424']);
 }
});
async function snap(db){const o={};for(const t of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])o[t]=(await db.query(`select * from ${t} order by to_jsonb(${t})::text`)).rows;return o;}
test('chapter18 exact existing-ID publication rejects drift/replay, rolls back failures and preserves unrelated data',async()=>{
 const{db}=await foundationDatabase();try{
  const row=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='lca'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values('lca','00000000-0000-0000-0000-000000000002',$1,9,$2)",[row.body,row.revision]);
  const target={...d,expected_revision:row.revision,expected_body_md5:row.body_md5},guard={...await localOwnerGuard(db,['lca']),catalog_count:56},sql=ownerReviewedLessonsSql({targets:[target]},guard),before=await snap(db);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected tree query failure';")),/Injected tree query failure/);assert.deepEqual(await snap(db),before);
  await assert.rejects(db.exec(ownerReviewedLessonsSql({targets:[target]},{...guard,draft_fingerprint:'0'.repeat(32)})),/Private draft changed/);assert.deepEqual(await snap(db),before);
  await db.exec(sql);const after=await snap(db);for(const k of['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[k],before[k]);assert.deepEqual(after.tutorial_catalog.filter(r=>r.id!=='lca'),before.tutorial_catalog.filter(r=>r.id!=='lca'));assert.deepEqual(after.tutorial_catalog.find(r=>r.id==='lca').body,d.body);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
