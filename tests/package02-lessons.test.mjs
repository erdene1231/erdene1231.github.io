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

test('search/sort rewrites preserve old references, justify only their core flags and round-trip native publication',()=>{
 const baseline=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,curriculum=JSON.parse(fs.readFileSync('curriculum.json')).lessons;
 const docs=['brute-force','sorting'].map(id=>JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)));
 const problems=proposalProblems(),topics=baseline.map(r=>docs.find(d=>d.id===r.id)?.body||r.body);
 for(const d of docs){const before=baseline.find(r=>r.id===d.id),b=d.body;assert.equal(d.expected_body_sha256,bodyHash(before.body));assert.equal(d.expected_revision,before.revision);
  validateTutorial(b);assert.deepEqual(mathProseWarnings(b),[]);assert.deepEqual(publicationBody(b,topics,problems),b);
  for(const key of ['id','aliases','order','level','levelKey','category','related','prerequisiteIds'])assert.deepEqual(b[key],before.body[key],key);
  const keyOf=p=>String(p.number);for(const old of curriculum[d.id].practice){const problem=problems.find(p=>p.source.toLowerCase()+'|'+p.ref.toLowerCase()===old.key);assert.ok(problem,old.key);assert.ok(b.learningRelations.practice.some(p=>p.key===keyOf(problem)),d.id+' retained '+old.key);}
  assert.deepEqual(b.learningRelations.practice.filter(p=>p.priority).map(p=>p.key),[d.id==='brute-force'?'85':'312']);
  assert.ok(b.learningRelations.practice.some(p=>p.key==='892'&&!p.priority&&p.stage==='Olympiad extension'));
  for(const doc of [b,b.translations.en]){assert.equal(doc.sections.length,15);const blocks=doc.sections[7].blocks,pieces=blocks.filter(p=>p.language==='C++17');assert.equal(pieces.length,5);assert.equal(pieces.slice(0,4).map(p=>p.text).join(''),pieces[4].text);for(const p of pieces.slice(0,4))assert.equal(blocks[blocks.indexOf(p)-1].type,'rich');assert.equal(doc.sections[12].blocks.filter(p=>p.type==='heading').length,6);}
 }
});

test('recursion/prefix lessons preserve metadata and previous references; core and extensions stay distinct',()=>{
 const baseline=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,problems=proposalProblems(),curriculum=JSON.parse(fs.readFileSync('curriculum.json')).lessons;
 const docs=['recursion','prefix-sums'].map(id=>JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`))),topics=baseline.map(r=>docs.find(d=>d.id===r.id)?.body||r.body);
 for(const d of docs){const before=baseline.find(r=>r.id===d.id),b=d.body;assert.equal(d.expected_body_sha256,bodyHash(before.body));assert.equal(d.expected_revision,before.revision);validateTutorial(b);assert.deepEqual(mathProseWarnings(b),[]);assert.deepEqual(publicationBody(b,topics,problems),b);
 for(const key of ['id','aliases','order','level','levelKey','category','related','prerequisiteIds'])assert.deepEqual(b[key],before.body[key],key);
 for(const old of curriculum[d.id].practice){const task=problems.find(p=>p.source.toLowerCase()+'|'+p.ref.toLowerCase()===old.key);assert.ok(task,old.key);assert.ok(b.learningRelations.practice.some(p=>p.key===String(task.number)));}
 assert.deepEqual(b.learningRelations.practice.filter(p=>p.priority).map(p=>p.key),[d.id==='recursion'?'22':'395']);assert.ok(b.learningRelations.practice.some(p=>p.key==='915'&&!p.priority));
 for(const lang of [b,b.translations.en]){assert.equal(lang.sections.length,15);const blocks=lang.sections[7].blocks,codes=blocks.filter(p=>p.language==='C++17');assert.equal(codes.length,5);assert.equal(codes.slice(0,4).map(p=>p.text).join(''),codes[4].text);for(const code of codes.slice(0,4))assert.equal(blocks[blocks.indexOf(code)-1].type,'rich');assert.equal(lang.sections[12].blocks.filter(p=>p.type==='heading').length,6);}
 }
});

test('sorting recursive revision preserves identity/relations and teaches strict library comparators; terminology edits preserve meaning and code',()=>{
 const previous=JSON.parse(fs.readFileSync('audit/package02-lessons/sorting.json')).body,d=JSON.parse(fs.readFileSync('audit/package02-revisions/sorting-recursive.json')),b=d.body;
 assert.equal(d.expected_revision,4);assert.equal(d.expected_body_sha256,bodyHash(previous));
 for(const k of ['id','aliases','order','level','levelKey','category','related','prerequisiteIds','learningRelations'])assert.deepEqual(b[k],previous[k],k);
 const baseline=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,topics=baseline.map(r=>r.id==='sorting'?b:r.body);validateTutorial(b);assert.deepEqual(mathProseWarnings(b),[]);assert.deepEqual(publicationBody(b,topics,proposalProblems()),b);
 for(const lang of [b,b.translations.en]){assert.equal(lang.sections.length,15);const code=lang.sections[7].blocks.filter(b=>b.language==='C++17').map(b=>b.text);assert.equal(code.length,10);assert.equal(code.slice(0,4).join(''),code[4]);assert.equal(code[7]+code[8],code[9]);assert.match(code[1],/merge_sort\(values, buffer, left, middle\)/);assert.match(code[1],/merge_sort\(values, buffer, middle, right\)/);assert.ok(code[1].indexOf('merge_parts')>code[1].indexOf('merge_sort(values, buffer, middle, right)'));}
 for(const id of ['binary-search','greedy']){const d=JSON.parse(fs.readFileSync(`audit/package02-revisions/${id}-terminology.json`)),old=JSON.parse(fs.readFileSync(`audit/package02-rewrite/${id}.json`)).body;assert.equal(d.expected_body_sha256,bodyHash(old));assert.deepEqual(d.body.translations,old.translations);assert.deepEqual(d.body.learningRelations,old.learningRelations);const patched=structuredClone(old);for(const change of d.changes){const path=JSON.parse(change.path);let parent=patched;for(const k of path.slice(0,-1))parent=parent[k];assert.equal(parent[path.at(-1)],change.before);parent[path.at(-1)]=change.after;}assert.deepEqual(patched,d.body);validateTutorial(d.body);assert.deepEqual(mathProseWarnings(d.body),[]);}
});
