import fs from'node:fs';
import{editorialDatabase}from'./problem-editorial-fixture.mjs';
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
export async function joiFixture(publicRows=read('audit/joi-ojuz/before-targets.json')){
 const db=await editorialDatabase({installPriority:false});
 // Existing local metadata fixture, never an online migration or content replay.
 await db.exec(fs.readFileSync('supabase/proposals/036-new-problem-metadata-import.sql','utf8'));
 await db.exec(`create table tutorial_changes(id integer,body jsonb);create table tutorial_drafts(tutorial_id text,editor_id text,body jsonb);create table learning_records(user_id text,body jsonb);create table profiles(id text,name text);
 insert into tutorial_catalog values('mongolia','{"keep":true}',false);insert into tutorial_changes values(1,'{"keep":true}');insert into profiles values('synthetic','Keep');insert into learning_records values('synthetic','{"readSections":[0],"checks":["purpose"],"undated":true}');`);
 for(let i=0;i<8;i++)await db.query('insert into tutorial_drafts values($1,$2,$3)',['synthetic-'+i,'synthetic-editor',{base:7,text:'Private synthetic draft '+i}]);
 const sources=[...new Set(publicRows.map(r=>r.body.source))];for(const source of sources)await db.query('insert into problem_sources values($1)',[source]);
 for(const r of publicRows)await db.query('insert into problem_catalog(problem_id,number,body,revision,archived,updated_at) values($1,$2,$3,$4,$5,$6)',[r.problem_id,r.number,r.body,r.revision,r.archived,r.updated_at]);
 if(publicRows.length<1000){
  const base=read('problems.json').problems.find(p=>p.id==='egoi-2023-inflation'),s=read('audit/atcoder-expansion/statement-patches.json').find(r=>r.id==='task-749'),e=read('audit/native-problem-editorials/batch01.json').find(r=>r.id==='task-749');
  const body={...base,id:'synthetic-native',number:2000,source:'Other',statement:s.statement,statementProvenance:s.statementProvenance,editorial:e.editorial};
  await db.query('insert into problem_catalog(problem_id,number,body,revision)values($1,$2,$3,4)',[body.id,body.number,body]);
 }
 await db.exec("select setval('problem_number_seq',3000,true);insert into problem_changes(problem_id,actor_id,action,previous_body,next_body) values('synthetic-history',null,'edit','{\"keep\":true}','{\"keep\":true}');");return db;
}
