import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {canonicalKey,problemIndex,resolvePractice,tutorialMastery,dayCompletion,CHECKS,buildStatistics,dateKey,monday,weekStatistics,bodyHash,validateRelations,withArchivedProblems} from '../learning-model.js';
import {validateProblem,parseCatalog} from '../problem-store.js';
import {validateTutorial} from '../tutorial-model.js';
import {proposalProblems} from '../tools/package02_tutorial_proposals.mjs';
import {filterProblems} from '../catalog.js';
const read=name=>JSON.parse(fs.readFileSync(new URL('../'+name,import.meta.url)));
const catalog=read('problems.json'),problems=catalog.problems,topics=read('tutorials.json').tutorials,curr=read('curriculum.json'),plan=read('study-plan.json');
test('all 702 problems have numeric ratings; original IDs/numbers and official CF ratings are preserved',()=>{
 parseCatalog(catalog);assert.equal(problems.length,702);for(const p of problems){validateProblem(p);assert(Number.isInteger(p.rating)&&p.rating>=800&&p.rating<=4000,p.id);}
 for(const old of read('tests/baseline-ids.json')){const p=problems.find(p=>p.id===old.id);assert(p,old.id);assert.equal(p.number,old.number);if(old.officialRating)assert.equal(p.rating,old.officialRating);}
 assert.equal(new Set(problems.map(canonicalKey)).size,problems.length);assert.equal(problemIndex(problems).get('cses|1071').id,'task-87');
});
test('56 seed lessons plus the scoped SCC, Paths, Flows, Matrices, Probability, Game theory, Square root, Geometry, Bridges, HLD, Centroid, Digit DP DP optimizations and Aho–Corasick catalog additions resolve prerequisites and practice',()=>{
 const addition=read('audit/package03-lessons/scc.json').body,allTopics=topics.concat(addition,read('audit/package03-lessons/paths-circuits.json').body,read('audit/package03-lessons/flows-cuts.json').body,read('audit/package03-lessons/matrices.json').body,read('audit/package03-lessons/probability.json').body,read('audit/package03-lessons/game-theory.json').body,read('audit/package03-lessons/sqrt-algorithms.json').body,read('audit/package03-lessons/geometry.json').body,read('audit/package03-lessons/sweep-line.json').body,read('audit/package03-lessons/bridges-articulation.json').body,read('audit/package03-lessons/heavy-light-decomposition.json').body,read('audit/package03-lessons/centroid-decomposition.json').body,read('audit/package03-lessons/digit-dp.json').body,read('audit/package03-lessons/dp-optimizations.json').body,read('audit/package03-lessons/aho-corasick.json').body,read('audit/package03-lessons/suffix-array.json').body,read('audit/package03-lessons/interactive-communication.json').body),known=new Set(topics.map(t=>t.id)),position=new Map(curr.order.map((id,i)=>[id,i]));assert.equal(known.size,56);
 for(const t of allTopics)validateTutorial(t);
 for(const[id,rel]of Object.entries(curr.lessons)){const scopedTopics=['scc','paths-circuits','flows-cuts','matrices','probability','game-theory','sqrt-algorithms','geometry','sweep-line','bridges-articulation','heavy-light-decomposition','centroid-decomposition','digit-dp','dp-optimizations','aho-corasick','suffix-array','interactive-communication'].includes(id)?allTopics:topics,scopedKnown=new Set(scopedTopics.map(t=>t.id));assert(scopedKnown.has(id));for(const p of rel.prerequisites)assert(position.get(p)<position.get(id),id+' → '+p);for(const v of rel.variants)assert(scopedKnown.has(v.tutorialId));validateRelations(rel,id,scopedTopics,['scc','paths-circuits','flows-cuts','matrices','probability','game-theory','sqrt-algorithms','geometry','sweep-line','bridges-articulation','heavy-light-decomposition','centroid-decomposition','digit-dp','dp-optimizations','aho-corasick','suffix-array','interactive-communication'].includes(id)?proposalProblems():problems);}
 for(const row of curr.backlog){assert.equal(row.status,'not_published');assert(!allTopics.some(t=>t.id===row.id));}
});
test('all 100 days refer to real tasks and published tutorials',()=>{
 const idx=problemIndex(problems),ids=new Set(topics.map(t=>t.id));assert.equal(plan.days.length,100);
 for(const d of plan.days){assert(d.required.length>=1&&d.goal&&d.observations.length&&d.checklist.length);assert.equal(new Set(d.required).size,d.required.length);for(const k of [...d.required,...d.challenge])assert(idx.has(k),k);for(const id of d.tutorials)assert(ids.has(id));for(const k of d.priority)assert(d.required.includes(k));}
});
test('opening/reading does not complete a day; solves, understanding and daily checks are required',()=>{
 const day=plan.days[0],idx=problemIndex(problems),progress={};assert(!dayCompletion(day,idx,{},progress).complete);
 for(const k of day.required)progress[idx.get(k).id]={status:'solved'};assert(!dayCompletion(day,idx,{},progress).complete);
 const records=Object.fromEntries(day.tutorials.map(id=>[id,{readSections:[0],checks:CHECKS}]));assert(dayCompletion(day,idx,records,progress,[0,1,2]).complete);
 assert(!dayCompletion(day,idx,records,progress,[0,1]).complete);
});
test('missing priority tasks cannot produce mastery',()=>{
 const practice=[{priority:true,problem:problems[0]},{priority:true}];assert(!tutorialMastery('x',{checks:CHECKS},practice,{[problems[0].id]:{status:'solved'}}).mastered);
});
test('legacy unknown dates are not invented and tags count unique problem membership',()=>{
 const p=problems.slice(0,2),progress=Object.fromEntries(p.map(p=>[p.id,{status:'solved'}])),dates={[p[1].id]:{first_solved_at:'2026-10-24T17:00:00Z'}};
 const s=buildStatistics(p,progress,dates,'2026-10-25');assert.equal(s.unknownDate,1);assert.equal(s.activity.get('2026-10-25'),1);assert.equal(s.solved.length,2);
 const duplicatedTags={...p[0],tags:['dp','dp']};assert.equal(buildStatistics([duplicatedTags],progress).tags.get('dp'),1);
});
test('Ulaanbaatar midnight, week boundaries and actual dated attempts are explicit',()=>{
 assert.equal(dateKey('2026-10-24T15:59:59Z'),'2026-10-24');assert.equal(dateKey('2026-10-24T16:00:00Z'),'2026-10-25');assert.equal(monday('2026-10-25'),'2026-10-19');assert.equal(monday('2026-10-26'),'2026-10-26');
 const p=problems[0],q=problems[1],progress={[p.id]:{status:'trying'},[q.id]:{status:'solved'}},dates={[p.id]:{first_attempted_at:'2026-10-20T00:00:00Z'}},s=buildStatistics([p,q],progress,dates,'2026-10-25'),week=weekStatistics(s,dates,'2026-10-19');assert.equal(week.attempted.length,1);assert.equal(week.solved.length,0);assert.equal(week.highest,null);
});
test('editable relationships reject unknown topics, duplicates and invalid optional reasons',()=>{
 const good=curr.lessons['binary-search'];assert.throws(()=>validateRelations({...good,next:'not-published'},'binary-search',topics,problems));assert.throws(()=>validateRelations({...good,practice:[...good.practice,good.practice[0]]},'binary-search',topics,problems));assert.throws(()=>validateRelations({...good,practice:[{key:'cses|1620',stage:'Standard',priority:true,reason:'x'.repeat(1001)}]},'binary-search',topics,problems));
});
test('fingerprints match exact original editions; custom admin edits do not match',async()=>{
 const baselines=read('tests/edition-baselines.json'),editions=read('tutorial-editions.json').editions;
 for(const[id,e]of Object.entries(editions)){assert(e.baseHashes.includes(await bodyHash(baselines[id])));assert(!e.baseHashes.includes(await bodyHash({...baselines[id],title:'Custom administrator title'})));}
});
test('numeric filters exclude unrated values and maintain correct rating bounds',()=>{
 const unrated={...problems[0],id:'unrated',rating:null,ratingKind:'unrated'},result=filterProblems([...problems,unrated],{},{minRating:2000,maxRating:2200,sort:'rating-asc'});assert(result.length);assert(result.every(p=>p.rating>=2000&&p.rating<=2200));assert(!result.some(p=>p.id==='unrated'));assert.equal(filterProblems(problems,{},{minRating:2200,maxRating:2000}).length,0);
});

test('archived problem status stays in all-time counts without inventing metadata',()=>{const p=problems[0],progress={[p.id]:{status:'solved'},'old-archived-id':{status:'solved'}};const combined=withArchivedProblems([p],progress),stats=buildStatistics(combined,progress,{'old-archived-id':{first_solved_at:'2026-10-20T00:00:00Z'}},'2026-10-25');assert.equal(stats.solved.length,2);assert.equal(stats.unrated,1);assert.equal(stats.activity.get('2026-10-20'),1);assert.equal(combined[1].tags.length,0);assert.equal(combined[1].rating,null);});
