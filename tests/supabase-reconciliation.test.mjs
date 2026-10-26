import {test} from 'node:test';
import assert from 'node:assert/strict';
import {PGlite} from '@electric-sql/pglite';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
test('021 validates optional prerequisites and preserves existing data and ACL',async()=>{
 const db=new PGlite();
 try{
  await db.exec('create role anon;create role authenticated;create role service_role;');
  const baseline=JSON.parse(read('supabase/audit/production-2026-10-26.json'));
  for(const name of ['tutorial_require_text','validate_tutorial_body']){
   const f=baseline.functions.find(f=>f.name===name);await db.exec(f.definition);
   await db.exec(`revoke all on function public.${name}(${name==='tutorial_require_text'?'jsonb,integer':'text,jsonb'}) from public,anon,authenticated;`);
  }
  const lesson=JSON.parse(read('tutorials.json')).tutorials[0];
  const validate=body=>db.query('select public.validate_tutorial_body($1,$2)',[body.id,body]);
  // Demonstrate the missing production validation before applying 021 locally.
  await validate({...lesson,prerequisiteIds:'invalid'});
  await db.exec("create table public.untouched(body jsonb);insert into public.untouched values ('{\"marker\":1}');");
  const acl=async()=>(await db.query("select proacl::text from pg_proc where proname='validate_tutorial_body'")).rows[0].proacl;
  const before=await acl();
  await db.exec(read('supabase/021-tutorial-prerequisite-validation.sql'));
  assert.equal(await acl(),before);
  for(const value of ['invalid',null,Array(31).fill('valid-id'),['INVALID'],[42]]){
   await assert.rejects(validate({...lesson,prerequisiteIds:value}),e=>e.code==='22023');
  }
  for(const value of [[],['binary-search'],Array(30).fill('valid-id')])await validate({...lesson,prerequisiteIds:value});
  const noPrerequisites={...lesson};delete noPrerequisites.prerequisiteIds;await validate(noPrerequisites);
  for(const t of JSON.parse(read('tutorials.json')).tutorials)await validate(t);
  assert.deepEqual((await db.query('select body from public.untouched')).rows,[{body:{marker:1}}]);
 }finally{await db.close();}
});
