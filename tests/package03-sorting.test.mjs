import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import{validateTutorial}from'../tutorial-model.js';import{publicationBody}from'../tutorial-publication.js';import{mathProseWarnings}from'../math-prose.js';import{bodyHash,proposalProblems}from'../tools/package02_tutorial_proposals.mjs';import{foundationDatabase,localOwnerGuard}from'./package03-introduction-fixture.mjs';import{ownerReviewedLessonsSql}from'../tools/package02_reviewed_publication.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/sorting.json'));
test('Sorting preserves complete chapter3 subtopics, source examples, original exercises and exact explained implementations',()=>{
 validateTutorial(d.body);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.deepEqual(mathProseWarnings(d.body),[]);const topics=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials.map(t=>t.body);assert.deepEqual(publicationBody(d.body,topics,proposalProblems()),d.body);
 assert.deepEqual(d.body.sections.map(s=>s.key),['sorting-theory','sorting-cpp','binary-search','practice']);assert.deepEqual(d.body.learningRelations.practice.map(p=>p.key),['312','320','313','314','330','317','892']);assert.deepEqual(d.body.prerequisiteIds,['complexity']);assert.equal(d.body.learningRelations.next,'set-map');
 for(const doc of[d.body,d.body.translations.en]){
  for(const file of['sorting-chapter3','sorting-std','sorting-search','sorting-monotone']){const full=fs.readFileSync(`audit/package03-work/${file}.cpp`,'utf8');const section=doc.sections.find(s=>s.blocks.some(b=>b.language==='C++17'&&b.text===full));assert(section,file);const before=section.blocks.slice(0,section.blocks.findIndex(b=>b.text===full));assert(before.filter(b=>b.type==='code').length>=3);}
  const fragments=doc.sections[0].blocks.filter(b=>b.language==='C++17').map(b=>b.text);
  const prefix=fragments.find(t=>t.startsWith('void merge_sort')&&!t.includes('int i = l'));
  const middle=fragments.find(t=>t.startsWith('    int i = l'));
  const tail=fragments.find(t=>t.startsWith('    while (i <= mid)'));
  const fullMerge=fs.readFileSync('audit/package03-work/sorting-chapter3.cpp','utf8').split('void merge_sort')[1].split('\n\nvoid count_sort')[0];
  assert.equal(prefix.trimEnd()+'\n\n'+middle.trimEnd()+'\n'+tail.trimEnd(),'void merge_sort'+fullMerge);
  const arrays=doc.sections[0].blocks.filter(b=>b.kind==='array').map(b=>b.rows[0]);for(const a of[[1,3,8,2,9,2,5,6],[1,2,2,3,5,6,8,9],[1,3,6,2,8,2,5,9],[1,2,2,6,3,5,9,8]])assert(arrays.some(b=>JSON.stringify(b)===JSON.stringify(a.map(x=>`$${x}$`))))
  assert(doc.sections[0].blocks.some(b=>b.kind==='tree'&&b.edges.length===6));assert(doc.sections[2].blocks.some(b=>b.type==='table'&&b.rows.length===1));assert.equal(doc.sections[3].blocks.filter(b=>b.type==='problem').length,7);
 }
 const cur=JSON.parse(fs.readFileSync('curriculum.json'));assert.deepEqual(cur.order.slice(0,4),['introduction','complexity','sorting','set-map']);
});
async function snapshot(db){const out={};for(const table of['tutorial_catalog','tutorial_drafts','tutorial_changes','progress','learning_records'])out[table]=(await db.query(`select * from ${table} order by to_jsonb(${table})::text`)).rows;return out;}
test('current57-row catalog Sorting replacement is atomic, guarded and preserves Introduction and private edits',async()=>{
 const{db}=await foundationDatabase();try{
  const intro=JSON.parse(fs.readFileSync('audit/package03-lessons/introduction.json')).body;await db.query("insert into tutorial_catalog(id,body,revision,published)values('introduction',$1,1,true)",[intro]);const old=(await db.query("select *,md5(body::text) body_md5 from tutorial_catalog where id='sorting'")).rows[0];await db.query("insert into tutorial_drafts(tutorial_id,editor_id,body,revision,base_revision)values('sorting','00000000-0000-0000-0000-000000000002',$1,9,$2)",[old.body,old.revision]);
  const before=await snapshot(db),target={...d,expected_revision:old.revision,expected_body_md5:old.body_md5};const guard={...await localOwnerGuard(db,['sorting']),catalog_count:57};const sql=ownerReviewedLessonsSql({targets:[target]},guard);
  await assert.rejects(db.exec(sql.replace('-- Atomic boundary: one target and its history are complete.',"RAISE EXCEPTION 'Injected sorting failure';")),/Injected sorting/);assert.deepEqual(await snapshot(db),before);
  await db.exec(sql);const after=await snapshot(db);for(const table of ['tutorial_drafts','progress','learning_records'])assert.deepEqual(after[table],before[table]);assert.deepEqual(after.tutorial_catalog.filter(t=>t.id!=='sorting'),before.tutorial_catalog.filter(t=>t.id!=='sorting'));assert.deepEqual(after.tutorial_catalog.find(t=>t.id==='sorting').body,d.body);assert.equal(after.tutorial_changes.length,before.tutorial_changes.length+1);await assert.rejects(db.exec(sql),/CAS\/body\/status drift/);
 }finally{await db.close();}
});
