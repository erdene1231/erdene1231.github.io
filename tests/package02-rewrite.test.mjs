import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {mathProseWarnings} from '../math-prose.js';
import {publicationBody} from '../tutorial-publication.js';
import {proposalProblems,bodyHash} from '../tools/package02_tutorial_proposals.mjs';
const prior=JSON.parse(fs.readFileSync('audit/PACKAGE02-FOUNDATION-PUBLISH-BATCH01.json')).targets;
const candidates=['binary-search','greedy','dynamic-programming'].map(id=>JSON.parse(fs.readFileSync(`audit/package02-rewrite/${id}.json`)));
const order=['need','direct','observation','method','walkthrough','proof','cost','implementation','boundaries','mistakes','connections','recognition','practice','importance','mastery'];
test('freshly authored foundations preserve revision guards and relationship identities in native publication schema',()=>{
 const topics=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials.map(r=>candidates.find(d=>d.id===r.id)?.body||r.body);
 for(const candidate of candidates){
  const old=prior.find(r=>r.id===candidate.id),body=candidate.body;
  assert.equal(candidate.expected_revision,6);
  assert.equal(candidate.expected_body_sha256,bodyHash(old.body));
  validateTutorial(body);assert.deepEqual(mathProseWarnings(body),[]);
  for(const key of ['id','aliases','prerequisiteIds','related','priority','priorityLevel'])assert.deepEqual(body[key],old.body[key],key);
  const identities=relations=>({...relations,variants:relations.variants.map(({description,descriptionEn,...v})=>v),practice:relations.practice.map(({reason,...p})=>p)});
  assert.deepEqual(identities(body.learningRelations),identities(old.body.learningRelations));
  assert.deepEqual(publicationBody(structuredClone(body),topics,proposalProblems()),body);
  assert.equal(body.automaticDemo,false);
  for(const doc of [body,body.translations.en]){
   assert.deepEqual(doc.sections.map(s=>s.key),order);
   const blocks=doc.sections[7].blocks,code=blocks.filter(b=>b.type==='code'&&b.language==='C++17');
   assert.equal(code.length,5);assert.equal(code.slice(0,-1).map(b=>b.text).join(''),code.at(-1).text);
   for(const fragment of code.slice(0,-1))assert.equal(blocks[blocks.indexOf(fragment)-1].type,'rich');
   assert.ok(!code.at(-1).text.includes('\t'));
   assert.equal(doc.sections.flatMap(s=>s.blocks).filter(b=>b.type==='code'&&b.language==='C++17').length,5);
   assert.ok(doc.sections[12].blocks.length>10);assert.ok(doc.sections[14].blocks.some(b=>b.type==='list'&&b.items.length>=4));
  }
 }
});
