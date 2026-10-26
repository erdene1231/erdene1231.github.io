import test from 'node:test';
import assert from 'node:assert/strict';
import {tutorialImageUrl,clearMediaCache} from '../tutorial-media.js';

const path='test-lesson/00000000-0000-0000-0000-000000000001/11111111-1111-1111-1111-111111111111.webp';
const delivery='https://example.com/fixture.webp';
const clientFor=fn=>({storage:{from(bucket){assert.equal(bucket,'tutorial-media');return {createSignedUrl:fn};}}});

test('image reader validates paths before requesting short-lived signed delivery',async()=>{
 const calls=[];
 const client=clientFor(async(p,seconds)=>{calls.push([p,seconds]);return {data:{signedUrl:delivery}};});
 await assert.rejects(tutorialImageUrl(client,'../external.svg'));
 assert.equal(calls.length,0);
 assert.equal(await tutorialImageUrl(client,path),delivery);
 assert.equal(await tutorialImageUrl(client,path,'admin',true),delivery);
 assert.deepEqual(calls,[[path,600],[path,60]]);
});

test('late signed delivery from a previous account is rejected',async()=>{
 let resolve;
 const client=clientFor(()=>new Promise(done=>{resolve=done;}));
 const pending=tutorialImageUrl(client,path,'previous');
 clearMediaCache();
 resolve({data:{signedUrl:delivery}});
 await assert.rejects(pending,/Account changed/);
});

test('errors and unsafe delivery URLs cannot become image sources',async()=>{
 await assert.rejects(tutorialImageUrl(clientFor(async()=>({error:Error('Unavailable')})),path),/Unavailable/);
 for(const signedUrl of ['javascript:alert(1)','http://example.com/image.webp','https://user:password@example.com/image.webp',undefined]){
  await assert.rejects(tutorialImageUrl(clientFor(async()=>({data:{signedUrl}})),path));
 }
});
