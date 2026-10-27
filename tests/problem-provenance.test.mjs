import test from 'node:test';import assert from 'node:assert/strict';
import {validateProblem,parseProblemImport} from '../problem-store.js';
const p={title:'Fixture',source:'Codeforces',ref:'580/C',url:'https://codeforces.com/contest/580/problem/C',rating:1500,ratingKind:'official',priorityLevel:'high',tags:['dfs and similar'],hints:[],hintsEn:[],ratingSource:'https://codeforces.com/api/problemset.problems',ratingVerifiedAt:'2026-10-27',sourceTags:['dfs and similar','graphs','trees','*special']};
test('official rating and source-tag provenance survives import/JSON roundtrip without conflating editorial tags',()=>{
 const out=parseProblemImport(JSON.parse(JSON.stringify([p])))[0];assert.equal(out.ratingSource,p.ratingSource);assert.equal(out.ratingVerifiedAt,p.ratingVerifiedAt);assert.deepEqual(out.sourceTags,p.sourceTags);assert.deepEqual(out.tags,p.tags);assert.notEqual(out.sourceTags,p.sourceTags);
 for(const patch of [{ratingSource:'javascript:alert(1)'},{ratingSource:null},{ratingVerifiedAt:7},{sourceTags:'graphs'},{sourceTags:[null]},{sourceTags:['x'.repeat(51)]}])assert.throws(()=>validateProblem({...p,...patch}));
});
