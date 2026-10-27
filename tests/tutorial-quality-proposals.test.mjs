import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import{proposedTutorialRows,bodyHash}from'../tools/part04_tutorial_proposals.mjs';import{validateTutorial}from'../tutorial-model.js';import{mathProseWarnings}from'../math-prose.js';
test('tutorial proposals are revision/hash guarded, non-mutating, math clean and preserve identities/relations/samples',()=>{
 const rows=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,before=JSON.stringify(rows),proposal=JSON.parse(fs.readFileSync('audit/PART04-TUTORIAL-QUALITY-PATCH01.json')),out=proposedTutorialRows(rows);assert.equal(JSON.stringify(rows),before);assert.equal(out.length,56);
 for(const p of proposal.patches){const old=rows.find(r=>r.body.id===p.id),row=out.find(r=>r.body.id===p.id);validateTutorial(row.body);assert.equal(mathProseWarnings(row.body).length,0,p.id);assert.equal(row.revision,old.revision);
  if(p.cpp_review?.batch==='02')for(const op of p.operations)if(op.expected.type==='code'){
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
