import fs from'node:fs';import {PGlite}from'@electric-sql/pglite';
export async function editorialDatabase({installPriority=true}={}){
 const db=new PGlite();await db.exec(`create role anon;create role authenticated;create schema auth;create function auth.uid() returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;grant usage on schema auth to anon,authenticated;
 create table admin_accounts(user_id uuid primary key);create function public.is_admin() returns boolean language sql stable security definer set search_path='' as $$select auth.uid() is not null and exists(select 1 from public.admin_accounts where user_id=auth.uid())$$;
 create table problem_sources(name text primary key);create unique index source_lower on problem_sources(lower(name));create sequence problem_number_seq start 100;
 create table problem_catalog(problem_id text primary key,number bigint unique,body jsonb,revision integer default 1,archived boolean default false,updated_at timestamptz default now());
 create table problem_changes(change_id bigserial,problem_id text,actor_id uuid,action text,previous_body jsonb,next_body jsonb);
 create table tutorial_catalog(id text primary key,body jsonb,published boolean);create table tutorial_media_references(scope text,scope_id text,object_path text,primary key(scope,scope_id,object_path));
 create schema storage;create table storage.objects(bucket_id text,name text,created_at timestamptz default now());
 create table progress(user_id uuid,problem_id text,status text);insert into progress values('00000000-0000-0000-0000-000000000002','stable','solved');`);
 const snapshot=JSON.parse(fs.readFileSync('supabase/audit/production-before-032.json'));
 for(const name of ['normalize_problem_source','valid_task_url','admin_add_source','validate_learning_problem','admin_save_problem','admin_import_problems','admin_import_learning_problems','get_catalog','get_admin_catalog','tutorial_require_text','tutorial_optional_text','safe_tutorial_link','validate_tutorial_inline','validate_tutorial_extended_block','validate_tutorial_body','validate_tutorial_publication','tutorial_image_paths','can_read_tutorial_media'])await db.exec(snapshot.functions.find(f=>f.name===name).definition);
 if(installPriority)await db.exec(fs.readFileSync('supabase/032-three-tier-priority.sql','utf8'));
 return db;
}
