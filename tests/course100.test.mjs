import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {dayCompletion,problemIndex,CHECKS} from '../learning-model.js';
const read=name=>JSON.parse(fs.readFileSync(name));
const plan=read('study-plan.json'),refs=read('audit/course100-v2/reference-inventory.json'),topics=read('audit/course100-v2/tutorial-inventory.json').concat(read('audit/course100-v2/setup-tutorials.json'));
test('100 fresh days use native bilingual documents, bounded practice, real IDs and backward review links',()=>{
 assert.equal(plan.id,'olympiad-100-v1');assert.equal(plan.version,2);assert.deepEqual(plan.days.map(d=>d.day),Array.from({length:100},(_,i)=>i+1));
 const idx=problemIndex(refs),ids=new Set(topics.map(t=>t.id));let quizzes=0;
 for(const d of plan.days){validateTutorial(d.document);assert.equal(d.completionMode,'daily-practice');assert(d.required.length<=2);assert(d.required.length||d.localExercise);for(const k of [...d.required,...d.challenge])assert(idx.has(k),d.day+' '+k);for(const id of d.tutorials)assert(ids.has(id));for(const r of d.reviewDays)assert(r<d.day&&r>0);
  const mn=d.document.sections.flatMap(s=>s.blocks),en=d.document.translations.en.sections.flatMap(s=>s.blocks);const m=mn.filter(b=>b.type==='quiz'),e=en.filter(b=>b.type==='quiz');assert(m.length>0);assert.deepEqual(m.map(b=>[b.quizId,b.answerId,b.options.map(o=>o.id)]),e.map(b=>[b.quizId,b.answerId,b.options.map(o=>o.id)]));quizzes+=m.length;
  for(const b of mn.filter(b=>b.type==='rich'))for(const run of b.content)if(run.href?.startsWith('#tutorial/')){const match=run.href.match(/^#tutorial\/([^/]+)\/part\/(\d+)$/);assert(match);assert(ids.has(match[1]));}
 }
 assert.equal(quizzes,122);
});
test('new daily reading criterion is separate from full lesson mastery; legacy mode is unchanged',()=>{
 const day=plan.days[2],idx=problemIndex(refs),progress=Object.fromEntries(day.required.map(k=>[idx.get(k).id,{status:'solved'}]));
 const masteryOnly=Object.fromEntries(day.tutorials.map(id=>[id,{checks:CHECKS,readSections:[]}]))
 assert(!dayCompletion(day,idx,masteryOnly,progress,[0,1,2]).complete);
 const reading=Object.fromEntries(day.tutorials.map(id=>[id,{readSections:day.tutorialSections[id]}]));assert(dayCompletion(day,idx,reading,progress,[0,1,2]).complete);assert(!dayCompletion(day,idx,reading,{},[0,1,2]).complete);assert(!dayCompletion(day,idx,reading,progress,[0,1]).complete);
 const legacy={...day,completionMode:undefined};assert(!dayCompletion(legacy,idx,reading,progress,[0,1,2]).complete);assert(dayCompletion(legacy,idx,masteryOnly,progress,[0,1,2]).complete);
});
