import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {PGlite} from '@electric-sql/pglite';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('022 extends the verified 021 validator without overwriting content, IDs, progress or grants',async()=>{
 const db=new PGlite();
 try{
  await db.exec(`create role anon;create role authenticated;create role service_role;
   create table tutorial_catalog(id text primary key,body jsonb,revision integer);
   create table progress(user_id text,problem_id text,status text,notes text);
   insert into progress values ('fixture-owner','stable-problem','solved','private fixture');`);
  const baseline=JSON.parse(read('supabase/audit/production-after-021.json'));
  for(const name of ['tutorial_require_text','validate_tutorial_body']){
   await db.exec(baseline.functions.find(f=>f.name===name).definition);
   await db.exec(`revoke all on function ${name}(${name==='tutorial_require_text'?'jsonb,integer':'text,jsonb'}) from public,anon,authenticated;`);
  }
  const lessons=JSON.parse(read('tutorials.json')).tutorials;
  for(const t of lessons)await db.query('insert into tutorial_catalog values ($1,$2,7)',[t.id,t]);
  const before=(await db.query('select * from tutorial_catalog order by id')).rows;
  const progress=(await db.query('select * from progress')).rows;
  const migration=read('supabase/022-tutorial-content-blocks.sql');
  await db.exec(migration);
  const validate=t=>db.query('select validate_tutorial_body($1,$2)',[t.id,t]);
  const sample=structuredClone(lessons[0]);
  for(const t of lessons)await validate(t);
  for(const prerequisites of [null,'not-an-array',[42],['INVALID'],Array(31).fill('valid-id')])
   await assert.rejects(validate({...sample,prerequisiteIds:prerequisites}),e=>e.code==='22023');
  await validate({...sample,prerequisiteIds:[]});
  const blocks=[
   {type:'rich',content:[{text:'<img src=x onerror=alert(1)> $n$',marks:['bold','code'],href:'#tutorial/binary-search'}]},
   {type:'heading',level:4,text:'Example'}, {type:'divider'},
   {type:'callout',tone:'proof',title:'Invariant',text:'An explanation'},
   {type:'quote',content:[{text:'Quoted text'}]},
   {type:'checklist',items:[{text:'Check the base case',checked:false}]},
   {type:'image',path:'test-lesson/00000000-0000-0000-0000-000000000001/11111111-1111-1111-1111-111111111111.webp',alt:'Array state',width:80,align:'center'},
   {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A'},{id:'b',label:'B'}],edges:[['a','b']]},
   {type:'diagram',kind:'dp',rows:[['0','1']]},
   {type:'problem',problemKey:'cses|1071'}, {type:'tutorial',tutorialId:'binary-search'}
  ];
  for(const block of blocks)await validate({...sample,sections:[{title:'Blocks',blocks:[block]}]});
  for(const block of [
   {type:'rich',content:[{text:'x',href:'javascript:alert(1)'}]},
   {type:'rich',content:[{text:'x',href:'https://user:password@example.com'}]},
   {type:'rich',content:[{text:'x',marks:['onclick']}]},
   {type:'heading',level:2.5,text:'x'},
   {type:'image',path:'../test.svg',alt:'x',width:80,align:'center'},
   {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A'}],edges:[['a','missing']]},
   {type:'diagram',kind:'graph',nodes:[{id:'a',label:'A',x:999}],edges:[]}
  ])await assert.rejects(validate({...sample,sections:[{title:'Invalid',blocks:[block]}]}),e=>e.code==='22023');
  const mnOnly=structuredClone(sample);delete mnOnly.translations;await validate(mnOnly);
  await assert.rejects(validate({...mnOnly,translations:{en:false}}),e=>e.code==='22023');
  for(const role of ['anon','authenticated']){
   await db.exec('set role '+role);
   await assert.rejects(validate(sample),e=>e.code==='42501');
   await assert.rejects(db.query('select validate_tutorial_extended_block($1)',[blocks[0]]),e=>e.code==='42501');
   await db.exec('reset role');
  }
  assert.deepEqual((await db.query('select * from tutorial_catalog order by id')).rows,before);
  assert.deepEqual((await db.query('select * from progress')).rows,progress);
  // Deliberately fail closed on a replay; never erase a concurrent validator edit.
  await assert.rejects(db.exec(migration),/re-audit instead of replaying/);
  await db.exec('rollback');
 }finally{await db.close();}
});
