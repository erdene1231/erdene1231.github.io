import test from 'node:test';
import assert from 'node:assert/strict';
import {createLearningStore} from '../learning-store.js';
function environment(){const cache=new Map();globalThis.localStorage={getItem:k=>cache.get(k)||null,setItem:(k,v)=>cache.set(k,v)};globalThis.window={addEventListener(){}};return cache;}
const settle=async()=>{for(let i=0;i<12;i++)await Promise.resolve();};
test('pending saves and dates stay isolated across account changes',async()=>{
 environment();let current={id:'alice'},release;const writes=[];
 const client={from(){return {select(){return {eq:async()=>({data:[],error:null})};},upsert(rows){writes.push(rows);if(rows[0].user_id==='alice')return new Promise(resolve=>{release=()=>resolve({error:null});});return Promise.resolve({error:null});}};}};
 const store=createLearningStore({user:()=>current,client:()=>client});await store.accountChanged();store.recordTransition('task-1','new','solved');store.set('bookmark','task-1',{saved:true});assert(release);
 current={id:'bob'};await store.accountChanged();assert.deepEqual(store.get('bookmark','task-1'),{});assert.deepEqual(store.dates(),{});store.set('bookmark','task-2',{saved:true});release();await settle();assert.equal(store.get('bookmark','task-2').saved,true);assert.equal(writes[1][0].user_id,'bob');
});
test('failed online save stays queued locally and clears only after successful retry',async()=>{
 const cache=environment();let failed=true;const client={from(){return {select(){return {eq:async()=>({data:[],error:null})};},upsert:async()=>({error:failed?new Error('offline'):null})};}};
 const store=createLearningStore({user:()=>({id:'alice'}),client:()=>client});await store.accountChanged();store.set('tutorial','binary-search',{checks:['purpose']});await settle();assert.equal(JSON.parse(cache.get('erdene:learning:v1:alice')).dirty.length,1);failed=false;await store.flush();assert.equal(JSON.parse(cache.get('erdene:learning:v1:alice')).dirty.length,0);
});
