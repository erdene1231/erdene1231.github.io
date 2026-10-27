import test from'node:test';import assert from'node:assert/strict';
import {assertProblemContentReady,assertNewProblemRatingReady,assertProblemSelectionReady}from'../problem-content-policy.js';import{hintTexts,validateProblem}from'../problem-store.js';
const editorial={id:'editorial-fixture',title:'Original explanation',levelKey:'beginner',order:1,sections:[{title:'Reasoning',blocks:[{type:'rich',content:[{text:'An original proof.',marks:['bold']}]},{type:'math',tex:'x+y'},{type:'code',language:'C++17',text:'int x=0;'}]}]};
test('Low suppresses historical hints without changing data; Medium policy is preserved',()=>{
 const p={priorityLevel:'low',hints:['one','two','three'],hintsEn:['a','b','c']};const before=JSON.stringify(p);assert.deepEqual(hintTexts(p,'mn'),[]);assert.deepEqual(hintTexts(p,'en'),[]);assert.equal(JSON.stringify(p),before);assert.throws(()=>assertProblemContentReady(p));assert.doesNotThrow(()=>assertProblemContentReady({...p,hints:[],hintsEn:[]}));assert.deepEqual(hintTexts({...p,priorityLevel:'medium'},'en'),p.hintsEn);
});
test('High selection permits absent optional content and validates supplied rich documents',()=>{
 const p={priorityLevel:'high',hints:['one','two','three'],hintsEn:['a','b','c'],editorialUrl:'https://example.com/editorial'};assert.doesNotThrow(()=>assertProblemContentReady(p));assert.doesNotThrow(()=>assertProblemContentReady({...p,editorial}));assert.doesNotThrow(()=>assertProblemContentReady({...p,editorial,hints:[]}));assert.throws(()=>assertProblemContentReady({...p,editorial:{...editorial,sections:[]}}));assert.throws(()=>assertProblemContentReady({...p,editorial:{...editorial,sections:[{blocks:[{type:'html',text:'<script>bad</script>'}]}]}}));
});
test('all new entries are rated with provenance; existing unrated catalog reading remains supported',()=>{
 const p={source:'AtCoder',rating:1600,ratingKind:'estimated',ratingBasis:'Greedy feasibility plus binary search; rough comparison.',ratingConfidence:'rough',ratingEstimatedAt:'2026-10-27',ratingSource:'https://atcoder.jp/contests/typical90/tasks/typical90_a'};
 assert.doesNotThrow(()=>assertNewProblemRatingReady(p));
 for(const patch of [{rating:null},{ratingKind:'unrated'},{ratingBasis:''},{ratingSource:'http://example.com'},{ratingConfidence:''},{ratingEstimatedAt:'2026-02-30'},{rating:1650},{ratingKind:'official',ratingVerifiedAt:'2026-10-27'}])assert.throws(()=>assertNewProblemRatingReady({...p,...patch}));
 const legacy=validateProblem({title:'Existing',source:'AtCoder',ref:'legacy',url:'https://atcoder.jp/contests/dp/tasks/dp_a',rating:null,ratingKind:'unrated',priority:false,tags:['dp'],hints:[],hintsEn:[]});assert.equal(legacy.rating,null);
});

test('selection needs valid identity,tags,priority,rating and educational rationale,not proof or optional documents',()=>{
 const p={title:'Frog1',ref:'dp_a',url:'https://atcoder.jp/contests/dp/tasks/dp_a',source:'AtCoder',tags:['dp'],primaryTopic:'dp',learningObjective:'Reviewed recurrence',priorityLevel:'high',priorityReason:'Individual recurrence objective',reviewStatus:'reviewed',rating:1600,ratingKind:'estimated',ratingBasis:'Reviewed algorithm calibration',ratingConfidence:'rough',ratingEstimatedAt:'2026-10-27',ratingSource:'https://atcoder.jp/contests/dp/tasks/dp_a',statementEvidence:{url:'https://atcoder.jp/contests/dp/tasks/dp_a',sha256:'a'.repeat(64),reviewNote:'Exact task reviewed'},solutionEvidence:{url:'https://example.com/proof',sha256:'b'.repeat(64),reviewNote:'Independent solution reviewed'}};
 assert.doesNotThrow(()=>assertProblemSelectionReady({...p,reviewStatus:'curated',statementEvidence:undefined,solutionEvidence:undefined}));for(const change of[{tags:[]},{priorityReason:''},{learningObjective:''},{url:'javascript:bad'},{rating:null}])assert.throws(()=>assertProblemSelectionReady({...p,...change}));
});
