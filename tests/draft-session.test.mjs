import test from 'node:test';import assert from 'node:assert/strict';
import {createDraftSession} from '../tutorial-drafts.js';
const tick=()=>new Promise(r=>setTimeout(r,20));
function fixture(rpc){const values=new Map();let actor='a';const s=createDraftSession({storage:{getItem:k=>values.get(k),setItem:(k,v)=>values.set(k,v)},user:()=>({id:actor}),client:()=>({rpc}),delay:100000});s.open({actor:'a',id:'lesson',body:{id:'lesson'},baseRevision:5,draftRevision:0});return {s,values,actor:v=>actor=v};}
test('offline edits persist and retry uses expected revision, never publication RPC',async()=>{
 let fail=true,calls=[];const {s}=fixture(async(name,args)=>{calls.push([name,args]);return fail?{error:Error('offline')}:{data:{revision:1}};});
 s.changed({id:'lesson',title:''});await s.flush();assert.equal(s.dirty(),true);assert.equal(s.local('a','lesson').body.title,'');assert.equal(s.local('b','lesson'),null);
 fail=false;await s.flush();assert.equal(s.dirty(),false);assert.equal(calls[1][0],'admin_save_tutorial_draft');assert.equal(calls[1][1].p_base_revision,5);assert.equal(calls[1][1].p_draft_revision,0);s.invalidate();
});
test('changes during a save are drained with the returned revision',async()=>{
 let resolve,calls=[];const {s}=fixture((name,args)=>{calls.push(args);return calls.length===1?new Promise(r=>resolve=r):Promise.resolve({data:{revision:2}});});
 s.changed({id:'lesson',title:'one'});const first=s.flush();await Promise.resolve();s.changed({id:'lesson',title:'two'});resolve({data:{revision:1}});await first;await tick();assert.equal(calls.length,2);assert.equal(calls[1].p_draft_revision,1);assert.equal(calls[1].p_body.title,'two');assert.equal(s.dirty(),false);s.invalidate();
});
test('old account responses cannot mutate a new session and old edits remain recoverable',async()=>{
 let resolve;const {s,actor}=fixture(()=>new Promise(r=>resolve=r));s.changed({id:'lesson',title:'private A'});const old=s.flush();await Promise.resolve();s.invalidate();actor('b');s.open({actor:'b',id:'lesson',body:{id:'lesson'},baseRevision:5,draftRevision:0});resolve({data:{revision:99}});await old;assert.equal(s.snapshot().draftRevision,0);assert.equal(s.local('a','lesson').unsynced,true);assert.equal(s.local('b','lesson'),null);s.invalidate();
});
test('revision conflict retains local payload without retry loop or revision advancement',async()=>{
 let calls=0;const {s}=fixture(async()=>{calls++;return {error:Error('REVISION_CONFLICT')};});s.changed({id:'lesson',title:'local'});await s.flush();await tick();assert.equal(calls,1);assert.equal(s.snapshot().draftRevision,0);assert.equal(s.dirty(),true);assert.equal(s.local('a','lesson').body.title,'local');s.invalidate();
});

test('synchronous client failure allows a later retry',async()=>{
 let fail=true;const {s}=fixture(()=>{if(fail)throw Error('client unavailable');return {data:{revision:1}};});s.changed({id:'lesson'});await s.flush();fail=false;await s.flush();assert.equal(s.dirty(),false);s.invalidate();
});
