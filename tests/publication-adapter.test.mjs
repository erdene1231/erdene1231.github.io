import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';
import {publicationBody} from '../tutorial-publication.js';
const topics=JSON.parse(fs.readFileSync(new URL('../tutorials.json',import.meta.url))).tutorials;
test('publication strips private editor state without mutating the saved draft or inventing English',()=>{
 const body=structuredClone(topics[0]);delete body.translations;body.customMetadata={keep:true};body._draftRelationsText=JSON.stringify({variants:[],practice:[],next:null});const before=JSON.stringify(body);
 const result=publicationBody(body,topics,[]);assert.equal(result._draftRelationsText,undefined);assert.equal(result.learningRelations,undefined);assert.equal(result.translations,undefined);assert.deepEqual(result.customMetadata,{keep:true});assert.equal(JSON.stringify(body),before);
});
test('malformed relationships and invalid body fail before publication',()=>{
 for(const raw of ['{bad','null','{}',42])assert.throws(()=>publicationBody({...topics[0],_draftRelationsText:raw},topics,[]));
 assert.throws(()=>publicationBody({...topics[0],prerequisiteIds:[42]},topics,[]));
 assert.throws(()=>publicationBody({...topics[0],learningRelations:{variants:[],practice:[{key:'not-real',stage:'Warm-up',priority:false}],next:null}},topics,[]));
});
test('publication preserves supplemental relationship metadata while validating supported relationships',()=>{
 const body=structuredClone(topics[0]);
 body.learningRelations={variants:[],practice:[],next:null,related:['dynamic-programming'],prerequisites:['prefix-sums'],custom:{opaque:[1,2]}};
 const before=structuredClone(body),result=publicationBody(body,topics,[]);
 assert.deepEqual(result.learningRelations,body.learningRelations);
 assert.deepEqual(body,before);
 result.learningRelations.custom.opaque.push(3);
 assert.deepEqual(body,before);
 const edited={...body,_draftRelationsText:JSON.stringify({...body.learningRelations,variants:[{tutorialId:topics[1].id,description:'  valid  '}]})};
 const normalized=publicationBody(edited,topics,[]);
 assert.deepEqual(normalized.learningRelations.custom,{opaque:[1,2]});
 assert.equal(normalized.learningRelations.variants[0].description,'valid');
 assert.throws(()=>publicationBody({...body,learningRelations:{...body.learningRelations,next:'missing-tutorial'}},topics,[]));
});
