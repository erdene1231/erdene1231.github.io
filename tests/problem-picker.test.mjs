import test from 'node:test';
import assert from 'node:assert/strict';
import {problemPickerRows} from '../tutorial-problem-picker.js';

test('problem picker searches stable IDs, source IDs, visible numbers and canonical references across the complete catalog',()=>{
 const problems=Array.from({length:748},(_,i)=>({id:'stable-'+i,number:i+1,title:'Problem '+i,source:'Judge',ref:String(1000+i)}));
 const last=problems.at(-1);last.sourceId='external-unique';
 assert.equal(problemPickerRows(problems).length,748);
 for(const query of ['STABLE-747','external-unique','judge|1747','Problem 747','  Judge 1747  '])assert(problemPickerRows(problems,query).some(row=>row.problem===last),query);
 for(const query of ['748','#748'])assert(problemPickerRows(problems,query).some(row=>row.problem===last));
 assert.equal(problemPickerRows(problems,'not present').length,0);
});

test('canonical CSES URL key, duplicate aliases and unavailable entries do not rewrite IDs or documents',()=>{
 const problems=[{id:'old-cses-id',title:'Old label',source:'CSES',ref:'Weird Algorithm',url:'https://cses.fi/problemset/task/1068/'},
  {id:'cses-1068',title:'New label',source:'CSES',ref:'1068',url:'https://cses.fi/problemset/task/1068'},
  {id:'retired',title:'Retired',source:'Judge',ref:'9999',archived:true}];
 const before=structuredClone(problems);
 assert.equal(problemPickerRows(problems).length,1);
 for(const query of ['old-cses-id','cses-1068','new label','cses|1068'])assert.equal(problemPickerRows(problems,query)[0].key,'cses|1068');
 assert.equal(problemPickerRows(problems,'retired').length,0);
 assert.deepEqual(problems,before);
});
