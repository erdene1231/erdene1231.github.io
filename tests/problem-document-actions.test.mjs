import test from'node:test';import assert from'node:assert/strict';
import{problemMetadata,documentSavePayload,createProblemDocumentBases}from'../problem-document-actions.js';
test('independent native payload excludes the other document and keeps metadata unchanged',()=>{
 const original={id:'task-749',number:749,revision:3,title:'Keep',source:'AtCoder',ref:'typical90_a',url:'https://atcoder.jp/contests/typical90/tasks/typical90_a',statement:{id:'statement'},statementProvenance:{keep:true},editorial:{id:'editorial'},priorityLevel:'high'};
 const saved=documentSavePayload(original,'editorial',{id:'new'});assert.equal('statement'in saved,false);assert.equal('statementProvenance'in saved,false);assert.deepEqual(saved.editorial,{id:'new'});assert.equal(saved.revision,3);assert.deepEqual(original.statement,{id:'statement'});
 const statement=documentSavePayload(original,'statement',null);assert.equal(statement.statement,null);assert.equal('editorial'in statement,false);assert.equal('statementProvenance'in statement,false);assert.equal(problemMetadata(original).hasEditorial,true);
});
test('own saves advance compatible sibling CAS bases without rebasing external stale metadata/panels',()=>{
 const state=createProblemDocumentBases(),base={id:'task-749',number:749,revision:3,title:'Keep',hasStatement:true,hasEditorial:true};state.reset(base);state.saved('statement',{...base,revision:4});assert.equal(state.metadata().revision,4);assert.equal(state.document('editorial').revision,4);
 state.reload('editorial',{...base,revision:5,title:'External title'});assert.equal(state.metadata().revision,4);assert.equal(state.document('statement').revision,4);assert.equal(state.document('editorial').revision,5);
 state.saved('editorial',{...base,revision:6,title:'External title'});assert.equal(state.metadata().revision,4);assert.equal(state.metadata().title,'Keep');assert.equal(state.document('statement').revision,4);assert.equal(state.document('editorial').revision,6);
 state.reset(null);assert.equal(state.metadata(),null);assert.equal(state.document('statement'),null);
});
