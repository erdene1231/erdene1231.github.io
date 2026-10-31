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
test('server-returned activity dates replace intent only for the same actor and unchanged pending value',async()=>{
 environment();let current={id:'alice'},release;const server={readSections:[0],viewedAt:'2026-10-31T00:00:00Z',viewEventId:'event'};
 let saved=[];const client={from(){return{select(){return{eq:async(_,user)=>({data:saved.filter(r=>r.user_id===user)})};},upsert(rows){return{select(){return new Promise(resolve=>{release=()=>{saved=rows.map(r=>({...r,value:server}));resolve({data:saved,error:null});};});}};}};}};
 const store=createLearningStore({user:()=>current,client:()=>client});await store.accountChanged();assert(store.ready());store.set('tutorial','intro',{readSections:[0],_activityEvent:{id:'event'}});release();await settle();assert.deepEqual(store.get('tutorial','intro'),server);
 store.set('tutorial','intro',{readSections:[0],_activityEvent:{id:'next'}});current={id:'bob'};await store.accountChanged();release();await settle();assert.deepEqual(store.get('tutorial','intro'),{});
});
test('unresolved or failed account load cannot claim ready dated activity',async()=>{
 environment();let release;const client={from(){return{select(){return{eq:()=>new Promise(resolve=>{release=resolve;})};}};}};const store=createLearningStore({user:()=>({id:'alice'}),client:()=>client});const loading=store.accountChanged();assert.equal(store.ready(),false);release({error:Error('offline')});await loading;assert.equal(store.ready(),false);const retry=store.reload();release({data:[],error:null});await retry;assert.equal(store.ready(),true);
});
test('a same-user edit during activity readback stays dirty and preserves its newer fields',async()=>{
 environment();let release,saved=[];const client={from(){return{select(){return{eq:async()=>({data:saved})};},upsert(rows){return{select:()=>new Promise(resolve=>{release=()=>{saved=rows.map(r=>({...r,value:{...r.value,viewedAt:'2026-10-31T00:00:00Z',viewEventId:r.value._activityEvent.id}}));for(const r of saved)delete r.value._activityEvent;resolve({data:rows,error:null});};})};}};}};
 const store=createLearningStore({user:()=>({id:'alice'}),client:()=>client});await store.accountChanged();store.set('tutorial','intro',{checks:['purpose'],_activityEvent:{id:'same',preserve:['checks']}});store.set('tutorial','intro',{checks:['purpose','correctness'],unknown:'new',_activityEvent:{id:'same',preserve:['checks']}});assert.deepEqual(store.get('tutorial','intro')._activityEvent.preserve,[]);release();await settle();assert.deepEqual(store.get('tutorial','intro').checks,['purpose','correctness']);release();await settle();assert.equal(store.get('tutorial','intro').unknown,'new');assert(!store.get('tutorial','intro')._activityEvent);
});
