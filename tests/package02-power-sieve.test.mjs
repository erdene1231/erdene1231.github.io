import test from'node:test';import assert from'node:assert/strict';import fs from'node:fs';import{validateTutorial}from'../tutorial-model.js';import{publicationBody}from'../tutorial-publication.js';import{mathProseWarnings}from'../math-prose.js';import{proposalProblems,bodyHash}from'../tools/package02_tutorial_proposals.mjs';
test('Modular exponentiation and smallest-factor sieve native lessons preserve stable identities and old practice, with exact explained compiled fragments',()=>{
 const baseline=JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials,docs=['fast-power','sieve'].map(id=>JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`))),topics=baseline.map(r=>docs.find(d=>d.id===r.id)?.body||r.body),problems=proposalProblems();
 for(const d of docs){const b=d.body,old=baseline.find(r=>r.id===d.id);assert.equal(bodyHash(old.body),d.expected_body_sha256);assert.equal(old.revision,d.expected_revision);for(const k of['id','aliases','order','level','levelKey','category','related','prerequisiteIds'])assert.deepEqual(b[k],old.body[k],k);validateTutorial(b);assert.deepEqual(mathProseWarnings(b),[]);assert.deepEqual(publicationBody(b,topics,problems),b);
 const oldPractice=JSON.parse(fs.readFileSync('curriculum.json')).lessons[d.id].practice;for(const p of oldPractice){const task=problems.find(t=>t.source.toLowerCase()+'|'+t.ref.toLowerCase()===p.key);assert.ok(task);assert.ok(b.learningRelations.practice.some(p=>p.key===String(task.number)));}
 assert.deepEqual(b.learningRelations.practice.filter(p=>p.priority).map(p=>p.key),[d.id==='fast-power'?'437':'439']);assert.ok(b.learningRelations.practice.some(p=>p.stage==='Olympiad extension'&&!p.priority));
 const expected=fs.readFileSync(`audit/package02-work/${d.id}.cpp`,'utf8');for(const lang of[b,b.translations.en]){assert.equal(lang.sections.length,15);const blocks=lang.sections[7].blocks,codes=blocks.filter(p=>p.language==='C++17');assert.equal(codes.length,5);assert.equal(codes.slice(0,4).map(c=>c.text).join(''),expected);assert.equal(codes[4].text,expected);for(const c of codes.slice(0,4))assert.equal(blocks[blocks.indexOf(c)-1].type,'rich');assert.equal(lang.sections[12].blocks.filter(b=>b.type==='heading').length,6);}
 }
});

test('power and sieve prose retains valid TeX instead of control escapes or bare command names',()=>{
 const slash=String.fromCharCode(92);
 for(const id of['fast-power','sieve']){const b=JSON.parse(fs.readFileSync(`audit/package02-lessons/${id}.json`)).body;for(const lang of[b,b.translations.en]){
 for(const section of lang.sections)for(const block of section.blocks)if(block.type!=='code'&&block.text)for(const ch of block.text)assert.ok(ch.charCodeAt(0)>=32);
 if(id==='fast-power'){assert.ok(lang.sections[4].blocks[0].text.includes(slash+'bmod17'));assert.ok(lang.sections[5].blocks[0].text.includes(slash+'equiv'));assert.ok(lang.sections[5].blocks[0].text.includes(slash+'pmod m'));}
 else{assert.ok(lang.sections[1].blocks[0].text.includes(slash+'sqrt{x}'));assert.ok(lang.sections[6].blocks[0].text.includes(slash+'sum_'));assert.ok(lang.sections[6].blocks[0].text.includes(slash+'log'+slash+'log N'));}
 }}
});
