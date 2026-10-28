import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {mathProseWarnings} from '../math-prose.js';
import {publicationBody} from '../tutorial-publication.js';
import {bodyHash,proposalProblems} from '../tools/package02_tutorial_proposals.mjs';
import {priorityLevel} from '../priority.js';
test('complexity rewrite retains stable metadata, prior practice and native rich editing schema',()=>{
 const baseline=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,candidate=JSON.parse(fs.readFileSync('audit/package02-lessons/complexity.json')),doc=candidate.body,before=baseline.find(r=>r.id==='complexity');
 assert.equal(candidate.expected_body_sha256,bodyHash(before.body));assert.equal(candidate.expected_revision,before.revision);
 for(const k of ['id','aliases','order','related','prerequisiteIds','level','levelKey','category'])assert.deepEqual(doc[k],before.body[k],k);
 validateTutorial(doc);assert.deepEqual(mathProseWarnings(doc),[]);
 const topics=baseline.map(r=>r.id==='complexity'?doc:r.body),problems=proposalProblems();assert.deepEqual(publicationBody(doc,topics,problems),doc);
 assert.equal(doc.priorityLevel,'high');assert.ok(doc.priorityReason.length>60);
 const rel=doc.learningRelations;assert.equal(rel.practice.length,6);assert.deepEqual(rel.practice.slice(0,5).map(({reason,...p})=>p),before.body.learningRelations.practice.map(({reason,...p})=>p));
 assert.deepEqual(rel.practice.at(-1),{key:'841',stage:'Olympiad extension',priority:false,reason:''});
 const plan=JSON.parse(fs.readFileSync('audit/PACKAGE02-COMPLEXITY-PRIORITY-PROMOTIONS.json'));assert.equal(plan.patches.length,2);for(const p of rel.practice.filter(p=>p.priority)){assert.ok(p.reason.length>50);const problem=problems.find(x=>String(x.number)===p.key),patch=plan.patches.find(x=>x.number===problem.number);assert.equal(bodyHash(problem),patch.expected_body_sha256);assert.equal(priorityLevel({...problem,...patch.changes}),'high');}
 const order=['need','direct','observation','method','walkthrough','proof','cost','implementation','boundaries','mistakes','connections','recognition','practice','importance','mastery'];
 for(const language of [doc,doc.translations.en]){
  assert.deepEqual(language.sections.map(s=>s.key),order);
  const blocks=language.sections[7].blocks,code=blocks.filter(b=>b.language==='C++17');assert.equal(code.length,5);assert.equal(code.slice(0,4).map(b=>b.text).join(''),code[4].text);
  for(const fragment of code.slice(0,4))assert.equal(blocks[blocks.indexOf(fragment)-1].type,'rich');
  assert.ok(!code[4].text.includes('\t'));assert.equal(language.sections[12].blocks.filter(b=>b.type==='heading').length,6);
 }
});
