import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import{validateTutorial}from'../tutorial-model.js';import{publicationBody}from'../tutorial-publication.js';import{mathProseWarnings}from'../math-prose.js';import{proposalProblems,bodyHash}from'../tools/package02_tutorial_proposals.mjs';
const d=JSON.parse(fs.readFileSync('audit/package03-lessons/complexity.json'));
test('complexity preserves four source subtopics, book examples and complete synchronized algorithm explanations',()=>{
 const topics=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials.map(r=>r.id==='complexity'?d.body:r.body);validateTutorial(d.body);assert.deepEqual(mathProseWarnings(d.body),[]);assert.deepEqual(publicationBody(d.body,topics,proposalProblems()),d.body);assert.equal(bodyHash(d.body),d.reviewed_body_sha256);assert.equal(d.body.id,'complexity');assert.equal(d.body.priorityLevel,'high');assert.deepEqual(d.body.learningRelations.practice.map(p=>p.key),['298','299','301','319','312','841']);
 const counting=JSON.parse(fs.readFileSync('audit/package03-work/complexity-counting-examples.json'));
 for(const doc of[d.body,d.body.translations.en]){
  assert.deepEqual(doc.sections.map(s=>s.key),['calculation-rules','complexity-classes','estimating-efficiency','maximum-subarray-sum','practice']);
  const rules=doc.sections[0].blocks;for(const c of[...counting.loops,...counting.recursion])assert(rules.some(b=>b.language==='C++17'&&b.text.trim()===c.code.trim()));
  const blocks=doc.sections[3].blocks,codes=blocks.filter(b=>b.language==='C++17').map(b=>b.text);assert.equal(codes.length,6);assert.equal(codes.slice(0,-1).map(c=>c.trimEnd()).join('\n\n')+'\n',codes.at(-1));assert.equal(codes.at(-1),fs.readFileSync('audit/package03-work/complexity.cpp','utf8'));
  const a=blocks.find(b=>b.kind==='array');assert.deepEqual(a.rows,[['$-1$','$2$','$4$','$-3$','$5$','$2$','$-5$','$2$']]);assert.deepEqual(a.highlights,['0:1','0:2','0:3','0:4','0:5']);assert.equal(doc.sections[4].blocks.filter(b=>b.type==='problem').length,6);
  assert(!/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(JSON.stringify(doc).replaceAll('\\n','')));assert(doc.sections[4].blocks.some(b=>b.type==='links'&&b.items.some(l=>l.url==='https://creativecommons.org/licenses/by-nc-sa/4.0/')));
 }
});
