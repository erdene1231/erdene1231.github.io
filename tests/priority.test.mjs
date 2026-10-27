import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import {PGlite} from '@electric-sql/pglite';
import {priorityLevel,priorityRank,validatePriority,ratingClass} from '../priority.js';import {filterProblems} from '../catalog.js';import {validateProblem,parseProblemImport} from '../problem-store.js';import {validateTutorial} from '../tutorial-model.js';
const fixture={title:'Test',source:'Codeforces',ref:'1A',url:'https://codeforces.com/problemset/problem/1/A',rating:800,ratingKind:'official',tags:['math'],hints:[],hintsEn:[]};
test('three tiers sort/filter independently from rating and retain legacy imports',()=>{
 const ps=['low','high','medium'].map((priorityLevel,i)=>({...fixture,id:String(i),number:i+1,priorityLevel,rating:3000-i*1000}));
 assert.deepEqual(filterProblems(ps,{}, {sort:'priority'}).map(priorityLevel),['high','medium','low']);assert.equal(filterProblems(ps,{}, {priorityLevel:'low'})[0].id,'0');assert.equal(filterProblems(ps,{}, {priorityOnly:true}).length,1);assert.equal(priorityLevel({priority:true}),'high');assert.equal(priorityLevel({priority:false}),'medium');assert.equal(priorityRank(ps[0]),0);
 for(const v of ['extreme',true,null,2])assert.throws(()=>validatePriority({priorityLevel:v}));assert.throws(()=>validatePriority({priorityReason:null}));
 const out=parseProblemImport([{...fixture,priorityLevel:'high',priorityReason:'Essential observation'}])[0];assert.equal(out.priority,true);assert.equal(out.priorityLevel,'high');assert.equal(out.priorityReason,'Essential observation');assert.equal(validateProblem({...fixture,priority:true}).priority,true);
 assert.throws(()=>validateTutorial({id:'x',title:'X',levelKey:'beginner',order:1,sections:[],priorityLevel:'extreme'}));
});
test('rating boundaries and intermediate values follow requested bands without rewriting data',()=>{
 const pairs=[[800,'newbie'],[1100,'newbie'],[1199,'newbie'],[1200,'pupil'],[1300,'pupil'],[1400,'specialist'],[1500,'specialist'],[1600,'expert'],[1800,'expert'],[1900,'candidate-master'],[2000,'candidate-master'],[2100,'master'],[2300,'master'],[2400,'grandmaster'],[2900,'grandmaster'],[3000,'legendary'],[4000,'legendary']];
 for(const [rating,band]of pairs)assert.equal(ratingClass({rating}),`rating-${band}`);assert.equal(ratingClass({rating:null,ratingKind:'unrated'}),'rating-unrated');
});
test('032 preserves validators/CAS/content and persists tiers without stripping existing provenance',async()=>{
 const db=new PGlite();try{
 await db.exec(`create role anon;create role authenticated;create schema auth;create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;
 create function is_admin() returns boolean language sql stable as $$select coalesce(auth.uid()='00000000-0000-0000-0000-000000000001'::uuid,false)$$;
 create table problem_sources(name text primary key);create unique index source_lower on problem_sources(lower(name));create sequence problem_number_seq;
 create table problem_catalog(problem_id text primary key,number bigint unique,body jsonb,revision integer default1,archived boolean default false,updated_at timestamptz default now());
 create table problem_changes(problem_id text,actor_id uuid,action text,previous_body jsonb,next_body jsonb);
 create table tutorial_catalog(id text,body jsonb,published boolean);` .replace('default1','default 1'));
 const baseline=JSON.parse(fs.readFileSync('supabase/audit/production-before-032.json'));
 for(const name of ['normalize_problem_source','valid_task_url','admin_add_source','validate_learning_problem','admin_save_problem','tutorial_require_text','tutorial_optional_text','validate_tutorial_body'])await db.exec(baseline.functions.find(f=>f.name===name).definition);
 const old={...fixture,id:'stable',number:19,priority:true,ratingSource:'https://codeforces.com/api/problemset.problems',hintReview:{status:'keep'},priorityLevel:'high',priorityReason:'Original reasoning'};
 await db.query('insert into problem_catalog(problem_id,number,body) values($1,$2,$3)',['stable',19,old]);
 const before=(await db.query('select * from problem_catalog')).rows;
 await db.exec(fs.readFileSync('supabase/032-three-tier-priority.sql','utf8'));assert.deepEqual((await db.query('select * from problem_catalog')).rows,before);
 const validate=body=>db.query('select validate_learning_problem($1)',[body]);await assert.rejects(validate({...fixture,priority:true,priorityLevel:'extreme'}));await assert.rejects(validate({...fixture,priority:true,priorityReason:null}));
 const tutorial={id:'empty',title:'Empty',levelKey:'beginner',order:1,sections:[],priorityLevel:'low'};await db.query('select validate_tutorial_body($1,$2)',['empty',tutorial]);await assert.rejects(db.query('select validate_tutorial_body($1,$2)',['empty',{...tutorial,prerequisiteIds:['BAD ID']}]));
 const save=(body,num=19,rev=1)=>db.query('select admin_save_problem($1,$2,$3) as body',[body,num,rev]);
 await assert.rejects(save({...fixture,priority:true}));await db.query("select set_config('request.jwt.claim.sub','00000000-0000-0000-0000-000000000001',false)");
 const result=(await save({...fixture,priority:false})).rows[0].body;assert.equal(result.priorityLevel,'high');assert.equal(result.priority,true);assert.equal(result.priorityReason,'Original reasoning');assert.deepEqual(result.hintReview,{status:'keep'});assert.equal(result.ratingSource,old.ratingSource);await assert.rejects(save({...fixture,priority:true}),e=>e.code==='40001');
 const low=(await save({...fixture,priorityLevel:'low',priority:false,priorityReason:'Specialized practice'},19,2)).rows[0].body;assert.equal(low.priorityLevel,'low');assert.equal(low.priority,false);assert.equal(low.id,'stable');
 const sourced=(await save({...fixture,priority:true,priorityLevel:'high',ratingSource:'https://codeforces.com/api/problemset.problems',ratingVerifiedAt:'2026-10-27',sourceTags:['math']},null,null)).rows[0].body;assert.equal(sourced.ratingSource,'https://codeforces.com/api/problemset.problems');assert.equal(sourced.ratingVerifiedAt,'2026-10-27');assert.deepEqual(sourced.sourceTags,['math']);
 await assert.rejects(validate({...fixture,priority:true,ratingSource:'http://example.com'}));await assert.rejects(validate({...fixture,priority:true,sourceTags:'math'}));
 await assert.rejects(db.exec(fs.readFileSync('supabase/032-three-tier-priority.sql','utf8')),/re-audit/);await db.exec('rollback');
 }finally{await db.close();}
});
