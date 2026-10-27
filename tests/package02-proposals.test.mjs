import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import{proposedTutorialRows,bodyHash}from'../tools/package02_tutorial_proposals.mjs';import{validateTutorial}from'../tutorial-model.js';import{mathProseWarnings}from'../math-prose.js';
test('tutorial proposals are revision/hash guarded, non-mutating, math clean and preserve identities/relations/samples',()=>{
 const rows=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,before=JSON.stringify(rows),proposal=JSON.parse(fs.readFileSync('audit/PACKAGE02-TUTORIAL-PROPOSALS.json')),out=proposedTutorialRows(rows);assert.equal(JSON.stringify(rows),before);assert.equal(out.length,56);
 for(const p of proposal.patches){const old=rows.find(r=>r.body.id===p.id),row=out.find(r=>r.body.id===p.id);validateTutorial(row.body);assert.equal(mathProseWarnings(row.body).length,0,p.id);assert.equal(row.revision,old.revision);
  for(const op of p.operations)if(op.expected?.detailKey)assert.equal(op.value.detailKey,op.expected.detailKey,p.id+' block identity must survive content conversion');
  if(p.cpp_review)for(const op of p.operations)if(op.expected.type==='code'){
   const literals=code=>code.match(/"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'/g)||[];
   assert.deepEqual(literals(op.value.text),literals(op.expected.text),p.id+' identifier changes must preserve C++ string/character literals');
  }
  for(const key of ['id','prerequisiteIds','learningRelations','related','priorityLevel','priority'])assert.deepEqual(row.body[key],old.body[key]);
  const samples=d=>[d,...Object.values(d.translations||{})].flatMap(v=>v.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&['Input','Output'].includes(b.language)).map(b=>b.text)));assert.deepEqual(samples(row.body),samples(old.body));
  const codes=d=>d.sections.flatMap(s=>s.blocks.filter(b=>b.type==='code'&&b.language==='C++17').map(b=>b.text));assert.deepEqual(codes(row.body),codes(row.body.translations.en));
 }
 const joke=out.find(r=>r.body.id==='mongolia');assert.equal(bodyHash(joke.body),bodyHash(rows.find(r=>r.body.id==='mongolia').body));
 const stale=structuredClone(rows);stale.find(r=>r.body.id==='dsu').revision++;assert.throws(()=>proposedTutorialRows(stale),/Stale/);
 const changed=structuredClone(rows);changed.find(r=>r.body.id==='dsu').body.title+=' changed';assert.throws(()=>proposedTutorialRows(changed),/Stale/);
});
test('fresh inventory metadata survives proposal application including unpublished revision2test lesson',()=>{const rows=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials;const inventory=JSON.parse(fs.readFileSync('audit/PACKAGE02-BASELINE-INVENTORY.json'));for(const row of rows){const live=inventory.tutorials.find(r=>r.id===row.id);assert.equal(bodyHash(row.body),live.body_sha256);row.revision=live.revision;row.published=live.published;}const before=structuredClone(rows),out=proposedTutorialRows(rows);assert.deepEqual(rows,before);const joke=out.find(r=>r.id==='mongolia');assert.equal(joke.revision,2);assert.equal(joke.published,false);assert.deepEqual(joke,before.find(r=>r.id==='mongolia'));for(const r of out){assert.equal(r.revision,before.find(v=>v.id===r.id).revision);assert.equal(r.published,before.find(v=>v.id===r.id).published);}});
