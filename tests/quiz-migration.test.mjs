import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {foundationDatabase} from './package03-introduction-fixture.mjs';
import {createQuiz} from '../tutorial-quiz.js';
import {validateTutorial} from '../tutorial-model.js';
test('041 quiz/image validation preserves ACLs and old data; exact bounded native documents validate',async()=>{
 const {db}=await foundationDatabase();
 try{
  await db.exec('create role service_role;');
  const baseline=JSON.parse(fs.readFileSync('audit/course100-v2/validator-baseline.json'));
  for(const f of baseline){await db.exec(f.definition);await db.exec(`revoke all on function public.${f.signature} from public,anon,authenticated;grant execute on function public.${f.signature} to service_role;`);}
  const before=(await db.query('select *from tutorial_catalog order by id')).rows;
  const sql=fs.readFileSync('supabase/041-native-tutorial-quiz-assets.sql','utf8');await db.exec(sql);
  const plan=JSON.parse(fs.readFileSync('study-plan.json')),setup=JSON.parse(fs.readFileSync('audit/course100-v2/setup-tutorials.json'));
  for(const t of [...plan.days.map(d=>d.document),...setup]){validateTutorial(t);await db.query('select public.validate_tutorial_body($1,$2)',[t.id,t]);}
  for(const row of before)await db.query('select public.validate_tutorial_body($1,$2)',[row.id,row.body]);
  assert.deepEqual((await db.query('select *from tutorial_catalog order by id')).rows,before);
  const q=createQuiz('fixture');for(const b of[{...q,answerId:'none'},{...q,quizId:23},{...q,options:null},{...q,options:[q.options[0],q.options[0]]},{type:'image',assetPath:'https://bad.invalid/x.webp',alt:'x',align:'center',width:100},{type:'image',alt:'x',align:'center',width:100}])await assert.rejects(db.query('select public.validate_tutorial_extended_block($1)',[b]));
  await assert.rejects(db.exec(sql),/baseline drift|already applied/);
 }finally{await db.close();}
});
