import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import{proposedTutorialRows,bodyHash}from'../tools/package02_tutorial_proposals.mjs';import{validateTutorial}from'../tutorial-model.js';import{mathProseWarnings}from'../math-prose.js';
test('tutorial proposals are revision/hash guarded, non-mutating, math clean and preserve identities/relations/samples',()=>{
 const rows=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,before=JSON.stringify(rows),proposal=JSON.parse(fs.readFileSync('audit/PACKAGE02-TUTORIAL-PROPOSALS.json')),out=proposedTutorialRows(rows);assert.equal(JSON.stringify(rows),before);assert.equal(out.length,56);
 for(const p of proposal.patches){const old=rows.find(r=>r.body.id===p.id),row=out.find(r=>r.body.id===p.id);validateTutorial(row.body);assert.equal(mathProseWarnings(row.body).length,0,p.id);assert.equal(row.revision,old.revision);
  for(const op of p.operations)if(op.expected?.detailKey)assert.equal(op.value.detailKey,op.expected.detailKey,p.id+' block identity must survive content conversion');
  if(p.cpp_review)for(const op of p.operations)if(op.expected.type==='code'){
   const literals=code=>code.match(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'/g)||[];
   assert.deepEqual(literals(op.value.text),literals(op.expected.text),p.id+' identifier changes must preserve C++ string/character literals');
  }
  for(const key of ['id','prerequisiteIds','learningRelations','related','priority'])assert.deepEqual(row.body[key],old.body[key]);
  const samples=d=>[d,...Object.values(d.translations||{})].flatMap(v=>v.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&['Input','Output'].includes(b.language)).map(b=>b.text)));assert.deepEqual(samples(row.body),samples(old.body));
  const codes=d=>d.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17').map(b=>b.text));assert.deepEqual(codes(row.body),codes(row.body.translations.en));
 }
 const joke=out.find(r=>r.body.id==='mongolia');assert.equal(bodyHash(joke.body),bodyHash(rows.find(r=>r.body.id==='mongolia').body));
 const stale=structuredClone(rows);stale.find(r=>r.body.id==='dsu').revision++;assert.throws(()=>proposedTutorialRows(stale),/Stale/);
 const changed=structuredClone(rows);changed.find(r=>r.body.id==='dsu').body.title+=' changed';assert.throws(()=>proposedTutorialRows(changed),/Stale/);
});
test('fresh inventory metadata survives proposal application including unpublished revision2test lesson',()=>{const rows=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials;const inventory=JSON.parse(fs.readFileSync('audit/PACKAGE02-BASELINE-INVENTORY.json'));for(const row of rows){const live=inventory.tutorials.find(r=>r.id===row.id);assert.equal(bodyHash(row.body),live.body_sha256);row.revision=live.revision;row.published=live.published;}const before=structuredClone(rows),out=proposedTutorialRows(rows);assert.deepEqual(rows,before);const joke=out.find(r=>r.id==='mongolia');assert.equal(joke.revision,2);assert.equal(joke.published,false);assert.deepEqual(joke,before.find(r=>r.id==='mongolia'));for(const r of out){assert.equal(r.revision,before.find(v=>v.id===r.id).revision);assert.equal(r.published,before.find(v=>v.id===r.id).published);}});
test('three foundational semantic proposals validate native bilingual schema/math and keep samples/identity',()=>{const rows=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,out=proposedTutorialRows(rows);for(const id of['binary-search','greedy','dynamic-programming']){const before=rows.find(r=>r.id===id),after=out.find(r=>r.id===id);validateTutorial(after.body);assert.equal(mathProseWarnings(after.body).length,0,id);assert.equal(after.body.id,id);assert.equal(after.revision,before.revision);for(const lang of['mn','en']){const a=lang==='mn'?before.body:before.body.translations.en,b=lang==='mn'?after.body:after.body.translations.en;assert.equal(b.sections[6].blocks[0].type,'ordered');for(const language of['Input','Output'])assert.deepEqual(b.sections[12].blocks.filter(x=>x.language===language),a.sections[12].blocks.filter(x=>x.language===language));}}});
test('implementation fragments precede and exactly reconstruct the final full program in both languages',()=>{const out=proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials);for(const id of['binary-search','greedy','dynamic-programming'])for(const lang of['mn','en']){const body=out.find(r=>r.id===id).body,d=lang==='mn'?body:body.translations.en;const blocks=d.sections[5].blocks,fragments=blocks.filter(b=>b.type==='code'&&b.detailKey?.startsWith('p02-fragment-'));assert.equal(fragments.length,4);for(const b of fragments){const at=blocks.indexOf(b);assert.equal(blocks[at-1].type,'p');assert.ok(blocks[at-1].text.length>30);}const full=d.sections[12].blocks.find(b=>b.language==='C++17').text;assert.equal(fragments.map(b=>b.text).join(''),full);assert.ok(!blocks.some(b=>b.type==='code'&&b.text===full));}});

test('tutorial priority proposals are individual, guarded and exclude the test lesson',()=>{const p=JSON.parse(fs.readFileSync('audit/PACKAGE02-SEMANTIC-PATCH01.json'));assert.equal(p.patches.length,3);const before=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,out=proposedTutorialRows(before);for(const patch of p.patches){assert.notEqual(patch.id,'mongolia');const doc=out.find(r=>r.id===patch.id).body;assert.equal(doc.priorityLevel,'high');assert.ok(doc.priorityReason.length>60);assert.deepEqual(doc.prerequisiteIds,before.find(r=>r.id===patch.id).body.prerequisiteIds);}assert.deepEqual(out.find(r=>r.id==='mongolia'),before.find(r=>r.id==='mongolia'));});

test('all 55 curriculum priority proposals preserve lesson bodies and metadata outside the two reviewed fields',()=>{
 const before=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials;
 const out=proposedTutorialRows(before),patch=JSON.parse(fs.readFileSync('audit/PACKAGE02-PRIORITY-PATCH01.json'));
 assert.equal(patch.patches.length,52);
 assert.equal(new Set(patch.patches.map(p=>p.id)).size,52);
 for(const proposal of patch.patches){
  assert.deepEqual(proposal.operations,[]);
  const original=before.find(r=>r.body.id===proposal.id),result=out.find(r=>r.body.id===proposal.id);
  const priorBody=structuredClone(result.body);
  for(const key of ['priorityLevel','priorityReason']){
   if(Object.hasOwn(original.body,key))priorBody[key]=original.body[key];else delete priorBody[key];
  }
  assert.equal(bodyHash(priorBody),proposal.expected_body_sha256,proposal.id+' only priority fields changed from guarded input');
  const metadata=row=>Object.fromEntries(Object.entries(row).filter(([key])=>key!=='body'));
  assert.deepEqual(metadata(result),metadata(original));

 }
 for(const r of out.filter(r=>r.body.id!=='mongolia')){validateTutorial(r.body);assert.ok(['low','medium','high'].includes(r.body.priorityLevel));assert.ok(r.body.priorityReason.length>60);}
 assert.deepEqual(out.find(r=>r.body.id==='mongolia'),before.find(r=>r.body.id==='mongolia'));
 const drift=structuredClone(before);drift.find(r=>r.body.id==='bellman-ford').body.title+=' changed';assert.throws(()=>proposedTutorialRows(drift),/Stale tutorial proposal: bellman-ford/);
});
