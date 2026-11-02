import test from 'node:test';
import assert from 'node:assert/strict';
import {validateQuiz,createQuiz} from '../tutorial-quiz.js';
import {validateExtendedBlock,validTutorialAsset} from '../tutorial-blocks.js';
test('Native quiz requires exactly one stable answer and bounded unique options',()=>{
 const q=createQuiz('example');assert(validateQuiz(q));assert(validateExtendedBlock(q));
 for(const patch of [{quizId:123},{options:[]},{options:[q.options[0]]},{answerId:'missing'},{options:[q.options[0],q.options[0]]},{question:''},{explanation:''}])assert.throws(()=>validateQuiz({...q,...patch}));
 const moved={...q,options:[...q.options].reverse()};assert(validateQuiz(moved));assert.equal(moved.options.find(o=>o.id===moved.answerId).text,q.options[0].text);
 assert.deepEqual(JSON.parse(JSON.stringify(q)),q);
});

test('publisher images are exact same-origin assets; arbitrary URLs/paths are rejected',()=>{for(const p of ['https://example.invalid/x.webp','../x.webp','tutorial-assets/cpp-environment/evil.svg','tutorial-assets/cpp-environment/cpp-extension.webp?x=1'])assert(!validTutorialAsset(p));assert(validTutorialAsset('tutorial-assets/cpp-environment/cpp-extension.webp'));});
