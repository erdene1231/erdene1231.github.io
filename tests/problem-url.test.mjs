import test from 'node:test';import assert from 'node:assert/strict';
import {canonicalProblemUrl,problemUrlIdentity} from '../problem-url.js';
import {parseProblemImport,parseCatalog} from '../problem-store.js';
test('ordinary CF URL forms normalize idempotently including D1 and multi-letter indexes',()=>{
 for(const index of ['A','D1','AA','A12']){
  const expected=`https://codeforces.com/contest/2277/problem/${index}`;
  assert.equal(canonicalProblemUrl(`https://codeforces.com/problemset/problem/2277/${index}`),expected);
  assert.equal(canonicalProblemUrl(expected),expected);
  assert.equal(problemUrlIdentity(expected+'?locale=en#x'),problemUrlIdentity(`https://codeforces.com/problemset/problem/2277/${index}`));
 }
 for(const url of ['https://codeforces.com/gym/123/problem/A','https://codeforces.com/blog/entry/12','https://atcoder.jp/contests/abc/tasks/abc_a','https://example.com/problemset/problem/1/A','https://codeforces.com/contest/1/standings','https://codeforces.com.evil.test/problemset/problem/1/A'])assert.equal(canonicalProblemUrl(url),url);
});
test('catalog identity survives normalization and both forms collide in imports',()=>{
 const p={id:'stable',number:19,title:'Fixture',source:'Codeforces',ref:'2277/D1',url:'https://codeforces.com/problemset/problem/2277/D1',rating:1200,ratingKind:'official',tags:['math'],priority:false,hints:[],hintsEn:[],revision:7};
 const raw={problems:[p],knownIds:['stable']};const out=parseCatalog(raw);
 assert.deepEqual(out.problems[0],{...p,url:'https://codeforces.com/contest/2277/problem/D1'});assert.equal(raw.problems[0].url,p.url);
 assert.equal(parseProblemImport([p])[0].url,out.problems[0].url);
 assert.throws(()=>parseProblemImport([p,{...p,ref:'alias',url:out.problems[0].url}]),/давхардсан/);
});
