import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {foundationDatabase} from './package03-introduction-fixture.mjs';
import {validateGridPresentation} from '../tutorial-grid.js';
test('037 accepts optional grid presentation, rejects malformed regions in both languages and retains validator ACL',async()=>{
 const {db,baseline}=await foundationDatabase();
 try{
  await db.exec('create role service_role; revoke all on function public.validate_tutorial_body(text,jsonb) from public; grant execute on function public.validate_tutorial_body(text,jsonb) to service_role;');
  const before=(await db.query("select md5(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure)) hash,proacl::text acl from pg_proc where oid='public.validate_tutorial_body(text,jsonb)'::regprocedure")).rows[0];
  assert.equal(before.hash,'f214981e444e2f89f3fc4a79e841e890');
  const sql=fs.readFileSync('supabase/037-tutorial-grid-regions.sql','utf8');await db.exec(sql);
  assert.equal((await db.query("select proacl::text acl from pg_proc where oid='public.validate_tutorial_body(text,jsonb)'::regprocedure")).rows[0].acl,before.acl);
  const body=structuredClone(baseline.find(r=>r.body.id==='dynamic-programming').body);
  const block={type:'diagram',kind:'dp',rows:[['A','A','B'],['C','D','B']],highlights:[],gridPresentation:{colors:[{row:0,col:0,color:'#112233'}],merges:[{row:0,col:0,rowSpan:1,colSpan:2},{row:0,col:2,rowSpan:2,colSpan:1}]}};
  for(const row of baseline) await db.query('select public.validate_tutorial_body($1,$2)',[row.body.id,row.body]);
  for(const lang of['mn','en']){
   const put=b=>{const c=structuredClone(body);(lang==='mn'?c:c.translations.en).sections[0].blocks.push(b);return c;};
   await db.query('select public.validate_tutorial_body($1,$2)',[body.id,put(block)]);
   const invalid=[null,[],{bad:1},{colors:null},{merges:null},{colors:[{row:0,col:0,color:'red'}]},{colors:[{row:0,col:0,color:'#000000'},{row:0,col:0,color:'#ffffff'}]},{colors:[{row:0.1,col:0,color:'#000000'}]},{colors:[{row:1e40,col:0,color:'#000000'}]},{merges:[{row:0,col:0,rowSpan:1,colSpan:1}]},{merges:[{row:0,col:0,rowSpan:2,colSpan:4}]},{merges:[{row:0,col:0,rowSpan:1,colSpan:2},{row:0,col:1,rowSpan:2,colSpan:1}]}];
   for(const gridPresentation of invalid){const b={...block,gridPresentation};assert.throws(()=>validateGridPresentation(b));await assert.rejects(db.query('select public.validate_tutorial_body($1,$2)',[body.id,put(b)]));}
   await db.query('select public.validate_tutorial_body($1,$2)',[body.id,put({type:'table',headers:['X','Y'],rows:[['a','b'],['c','d']],gridPresentation:{merges:[{row:0,col:0,rowSpan:2,colSpan:1}]}})]);
  }
  await assert.rejects(db.exec(sql),/baseline drift|already applied/);
 }finally{await db.close();}
});
