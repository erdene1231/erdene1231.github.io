import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial,view} from '../tutorial-model.js';
import {validateExtendedBlock,validateInline,safeLink} from '../tutorial-blocks.js';
import {editableVersion,isLegacyEditableBlock} from '../tutorial-editor-compat.js';

const lessons=JSON.parse(fs.readFileSync(new URL('../tutorials.json',import.meta.url),'utf8')).tutorials;
const sample=()=>structuredClone(lessons[0]);
const withBlock=block=>({...sample(),sections:[{title:'Reader compatibility fixture',blocks:[block]}]});
const mediaPath='test-lesson/00000000-0000-0000-0000-000000000001/11111111-1111-1111-1111-111111111111.webp';

test('all 55 existing documents validate without changing IDs, content, relationships or metadata',()=>{
 assert.equal(lessons.length,55);
 for(const original of lessons){
  const body=structuredClone(original),before=JSON.stringify(body);
  assert.equal(validateTutorial(body),body);
  assert.equal(JSON.stringify(body),before,original.id);
  assert.equal(view(body,'mn'),body);
  assert.equal(view(body,'en'),body.translations.en);
 }
 const body=sample();body.adminExtension={notes:['retain exactly'],version:17};
 body.sections[0].blocks[0].unrecognizedMetadata={future:true};
 const before=JSON.stringify(body);validateTutorial(body);assert.equal(JSON.stringify(body),before);
});

test('022-compatible typed blocks round-trip through the model without rewriting values',()=>{
 const blocks=[
  {type:'rich',content:[{text:'<img src=x onerror=alert(1)> $n$',marks:['bold','italic','underline','strike','code'],href:'#tutorial/binary-search'}]},
  {type:'heading',level:1,text:'Heading'},
  {type:'quote',content:[{text:'A quoted observation'}]},
  {type:'callout',tone:'proof',title:'Invariant',text:'The invariant holds.'},
  {type:'checklist',items:[{text:'Check the base case',checked:false}]},
  {type:'divider'},
  {type:'image',path:mediaPath,alt:'Array before updating',caption:'',width:80,align:'center'},
  {type:'diagram',kind:'array',rows:[['$0$','$1$']],highlights:['0:1']},
  {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A'},{id:'b',label:'B',x:80,y:60}],edges:[['a','b']]},
  {type:'problem',problemKey:'cses|1071'},
  {type:'tutorial',tutorialId:'binary-search',label:'Continue reading'}
 ];
 for(const block of blocks){
  assert.equal(validateExtendedBlock(block),true,block.type);
  const body=withBlock(block),before=JSON.stringify(body);validateTutorial(body);
  assert.equal(JSON.stringify(body),before,block.type);
 }
});

test('prerequisite validation remains strict after extending the reader model',()=>{
 for(const value of [null,'binary-search',[42],['INVALID'],Array(31).fill('binary-search')]){
  assert.throws(()=>validateTutorial({...sample(),prerequisiteIds:value}));
 }
 validateTutorial({...sample(),prerequisiteIds:[]});
 validateTutorial({...sample(),prerequisiteIds:Array(30).fill('binary-search')});
});

test('reader MN fallback does not provide an editable alias for a missing English version',()=>{
 const body=sample();delete body.translations;const before=JSON.stringify(body);
 validateTutorial(body);assert.equal(view(body,'en'),body);
 assert.equal(editableVersion(body,'mn'),body);
 assert.throws(()=>editableVersion(body,'en'));
 assert.equal(JSON.stringify(body),before);
 const bilingual=sample();assert.equal(editableVersion(bilingual,'en'),bilingual.translations.en);
 for(const invalid of [false,0,'',[]])assert.throws(()=>validateTutorial({...body,translations:{en:invalid}}));
});

test('legacy editor recognizes only shapes it can safely edit',()=>{
 for(const type of ['p','note','code','math','list','ordered','table','links'])assert.equal(isLegacyEditableBlock({type}),true,type);
 for(const block of [null,undefined,[],{}, {type:'rich'},{type:'image'},{type:'diagram'},{type:'heading'},{type:'future-format'}])
  assert.equal(isLegacyEditableBlock(block),false);
});

test('malformed blocks and SQL-incompatible optional fields are rejected',()=>{
 for(const block of [null,[],{}, {type:'future-format'},
  {type:'rich',content:[{text:'x',marks:Array(21).fill('bold')}]},
  {type:'rich',content:[{text:'x',marks:['onclick']}]},
  {type:'heading',level:2.5,text:'Invalid level'},
  {type:'callout',tone:'note',title:42,text:'Text'},
  {type:'callout',tone:'note',title:null,text:'Text'},
  {type:'quote',content:null,text:'Must not fall back to text'},
  {type:'callout',tone:'note',content:false,text:'Must not fall back to text'},
  {type:'image',path:mediaPath,alt:'Array',width:80,align:'center',caption:42},
  {type:'image',path:mediaPath,alt:'Array',width:80,align:'center',caption:null},
  {type:'image',path:'../external.svg',alt:'Unsafe path',width:100,align:'center'},
  {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A'}],edges:[['a','missing']]},
  {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A',x:999}],edges:[]},
  {type:'diagram',kind:'array',rows:[['1']],highlights:['']},
  {type:'checklist',items:[{text:'x',checked:'false'}]}
 ])assert.throws(()=>validateTutorial(withBlock(block)));
 validateInline([{text:'x',marks:Array(20).fill('bold')}]);
});

test('inline links accept explicit safe URLs and reject browser normalization tricks',()=>{
 assert.equal(safeLink('#tutorial/binary-search'),'#tutorial/binary-search');
 assert.equal(safeLink('https://example.com/path'),'https://example.com/path');
 for(const href of ['javascript:alert(1)','data:text/html,x','//example.com/path',
  'https://user:password@example.com/path','https:example.com',' https://example.com',
  'https://example.com/white space','https://example.com/\npath','https://example.com\\path']){
  assert.equal(safeLink(href),null,href);
  assert.throws(()=>validateInline([{text:'Link',href}]),href);
 }
});
