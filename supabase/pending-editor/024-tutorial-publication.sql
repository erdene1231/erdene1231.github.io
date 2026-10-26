-- Recovery 023-tutorial-publication.sql -> 024-tutorial-publication.sql; production 021 prerequisite validation is distinct.
-- Purpose: explicit publish/unpublish, references and lazy public reader APIs.
-- Dependencies: 022, 023, 004/007 catalog. Existing rows stay published.
begin;
create or replace function public.check_tutorial_publication() returns trigger
language plpgsql security definer set search_path='' as $$
declare item jsonb;rel jsonb;row_value jsonb;k text;cycle_found boolean;
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if not new.published then return new;end if;
 perform public.validate_tutorial_body(new.id,new.body);
 for item in select value from jsonb_array_elements(coalesce(new.body->'prerequisiteIds','[]'::jsonb)) loop
  if item#>>'{}'=new.id or not exists(select 1 from public.tutorial_catalog where id=item#>>'{}' and published) then raise exception 'Missing published prerequisite: %',item#>>'{}' using errcode='22023';end if;
 end loop;
 with recursive paths(id,path,cycle) as (
  select value#>>'{}',array[new.id,value#>>'{}'],(value#>>'{}')=new.id from jsonb_array_elements(coalesce(new.body->'prerequisiteIds','[]'::jsonb))
  union all select x.value#>>'{}',p.path||(x.value#>>'{}'),(x.value#>>'{}')=any(p.path)
  from paths p join public.tutorial_catalog t on t.id=p.id cross join lateral jsonb_array_elements(coalesce(t.body->'prerequisiteIds','[]'::jsonb)) x(value) where not p.cycle
 ) select exists(select 1 from paths where cycle) into cycle_found;
 if cycle_found then raise exception 'Prerequisite cycle.' using errcode='22023';end if;
 rel:=new.body->'learningRelations';
 if rel is not null then
  if jsonb_typeof(rel) is distinct from 'object' or jsonb_typeof(rel->'practice') is distinct from 'array' or jsonb_typeof(rel->'variants') is distinct from 'array' then raise exception 'Invalid tutorial relationships.' using errcode='22023';end if;
  if jsonb_array_length(rel->'practice') not between 1 and 30 or jsonb_array_length(rel->'variants')>20 then raise exception 'Expected 1-30 practice tasks, at most 20 variants.' using errcode='22023';end if;
  if not exists(select 1 from jsonb_array_elements(rel->'practice') x where x->'priority'='true'::jsonb) then raise exception 'Select at least one priority task.' using errcode='22023';end if;
  if (select count(*)<>count(distinct value->>'key') from jsonb_array_elements(rel->'practice')) then raise exception 'Duplicate practice task.' using errcode='22023';end if;
  for row_value in select value from jsonb_array_elements(rel->'practice') loop
   k:=row_value->>'key';
   if not exists(select 1 from public.problem_catalog where not archived and coalesce('cses|'||(regexp_match(body->>'url','^https://cses[.]fi/problemset/task/([0-9]+)/?([?#].*)?$'))[1],lower(btrim(body->>'source'))||'|'||lower(btrim(body->>'ref')))=k) then raise exception 'Unknown practice task: %',k using errcode='22023';end if;
   if coalesce(row_value->>'stage','') not in ('Warm-up','Standard','Observation','Application','Challenge','Olympiad extension') or jsonb_typeof(row_value->'priority') is distinct from 'boolean' then raise exception 'Invalid practice stage/priority.' using errcode='22023';end if;
   if row_value->'priority'='true'::jsonb then perform public.tutorial_require_text(row_value->'reason',1000);end if;
   if row_value ? 'objective' and (jsonb_typeof(row_value->'objective')<>'string' or length(row_value->>'objective')>1500) then raise exception 'Invalid learning objective.' using errcode='22023';end if;
  end loop;
  for row_value in select value from jsonb_array_elements(rel->'variants') loop
   if coalesce(row_value->>'tutorialId','') !~ '^[a-z0-9-]{1,80}$' or row_value->>'tutorialId'=new.id then raise exception 'Invalid variant ID.' using errcode='22023';end if;
   perform public.tutorial_require_text(row_value->'description',1000);
   if row_value ? 'descriptionEn' and (jsonb_typeof(row_value->'descriptionEn')<>'string' or length(row_value->>'descriptionEn')>1000) then raise exception 'Invalid variant description.' using errcode='22023';end if;
  end loop;
  if rel->>'next' is not null and ((rel->>'next') !~ '^[a-z0-9-]{1,80}$' or rel->>'next'=new.id) then raise exception 'Invalid next tutorial.' using errcode='22023';end if;
 end if;
 return new;
end;
$$;
revoke all on function public.check_tutorial_publication() from public,anon,authenticated;
drop trigger if exists tutorial_publication_check on public.tutorial_catalog;
create trigger tutorial_publication_check before insert or update on public.tutorial_catalog for each row execute function public.check_tutorial_publication();
create or replace function public.admin_publish_tutorial_draft(p_id text,p_body jsonb,p_base_revision integer,p_draft_revision integer,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare d public.tutorial_drafts%rowtype;t public.tutorial_catalog%rowtype;old_body jsonb;next_revision integer;remaining jsonb;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 select * into d from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid() for update;
 select * into t from public.tutorial_catalog where id=p_id for update;
 if d.tutorial_id is null or d.revision is distinct from p_draft_revision or d.base_revision is distinct from p_base_revision or coalesce(t.revision,0)<>p_base_revision then raise exception 'REVISION_CONFLICT: draft or publication changed.' using errcode='40001';end if;
 perform public.validate_tutorial_body(p_id,p_body);old_body:=coalesce(t.body,'{}'::jsonb);next_revision:=coalesce(t.revision,0)+1;
 insert into public.tutorial_catalog(id,body,revision,published,published_at,updated_by) values(p_id,p_body,next_revision,true,now(),auth.uid())
 on conflict(id) do update set body=excluded.body,revision=excluded.revision,published=true,published_at=now(),updated_at=now(),updated_by=auth.uid();
 insert into public.tutorial_changes(tutorial_id,actor_id,revision,previous_body,new_body) values(p_id,auth.uid(),next_revision,old_body,p_body);
 if d.body=p_body then delete from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid();
 else update public.tutorial_drafts set base_revision=next_revision,revision=revision+1,updated_at=now() where tutorial_id=p_id and editor_id=auth.uid() returning to_jsonb(tutorial_drafts)-'editor_id' into remaining;end if;
 return jsonb_build_object('body',p_body,'revision',next_revision,'published',true,'updated_at',now(),'draft',remaining);
end;
$$;
create or replace function public.admin_set_tutorial_publication(p_id text,p_revision integer,p_published boolean,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare t public.tutorial_catalog%rowtype;remaining jsonb;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 if p_published is null then raise exception 'Publication state required.' using errcode='22023';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);select * into t from public.tutorial_catalog where id=p_id for update;
 if t.id is null or t.revision is distinct from p_revision then raise exception 'REVISION_CONFLICT: publication changed.' using errcode='40001';end if;
 if not p_published and exists(select 1 from public.tutorial_catalog other where other.published and other.id<>p_id and coalesce(other.body->'prerequisiteIds','[]'::jsonb) ? p_id) then raise exception 'A published tutorial still requires this prerequisite.' using errcode='22023';end if;
 update public.tutorial_catalog set published=p_published,revision=revision+1,updated_at=now(),updated_by=auth.uid(),published_at=case when p_published then now() else published_at end where id=p_id;
 insert into public.tutorial_changes(tutorial_id,actor_id,revision,previous_body,new_body) values(p_id,auth.uid(),t.revision+1,t.body,t.body);
 update public.tutorial_drafts set base_revision=t.revision+1,revision=revision+1,updated_at=now() where tutorial_id=p_id and editor_id=auth.uid() and base_revision=t.revision returning to_jsonb(tutorial_drafts)-'editor_id' into remaining;
 return jsonb_build_object('body',t.body,'revision',t.revision+1,'published',p_published,'updated_at',now(),'draft',remaining);
end;
$$;
create or replace function public.get_tutorial_index() returns jsonb
language sql stable security definer set search_path='' as $$
 select jsonb_build_object('tutorials',coalesce((select jsonb_agg(jsonb_build_object('body',jsonb_build_object(
 'id',id,'title',body->'title','summary',body->'summary','category',body->'category','levelKey',body->'levelKey','level',body->'level','order',body->'order','aliases',body->'aliases','prerequisites',body->'prerequisites','prerequisiteIds',coalesce(body->'prerequisiteIds','[]'::jsonb),'related',body->'related','learningRelations',body->'learningRelations',
 'sectionCount',jsonb_array_length(body->'sections'),'readingMinutes',greatest(5,ceil(length((body->'sections')::text)/1800.0)),
 'translations',case when jsonb_typeof(body#>'{translations,en}')='object' then jsonb_build_object('en',(body#>'{translations,en}')-'sections') else '{}'::jsonb end),
 'revision',revision,'updatedAt',updated_at) order by (body->>'order')::integer) from public.tutorial_catalog where published),'[]'::jsonb),
 'knownIds',coalesce((select jsonb_agg(id) from public.tutorial_catalog),'[]'::jsonb),'unpublishedIds',coalesce((select jsonb_agg(id) from public.tutorial_catalog where not published),'[]'::jsonb));
$$;
create or replace function public.get_published_tutorial(p_id text) returns jsonb
language sql stable security definer set search_path='' as $$
 select jsonb_build_object('body',body,'revision',revision,'updatedAt',updated_at) from public.tutorial_catalog where id=p_id and published;
$$;
create or replace function public.get_tutorials() returns jsonb
language sql stable security definer set search_path='' as $$
 select coalesce(jsonb_agg(jsonb_build_object('body',body,'revision',revision) order by (body->>'order')::integer),'[]'::jsonb) from public.tutorial_catalog where published;
$$;
revoke all on function public.admin_publish_tutorial_draft(text,jsonb,integer,integer,uuid),public.admin_set_tutorial_publication(text,integer,boolean,uuid) from public,anon;
grant execute on function public.admin_publish_tutorial_draft(text,jsonb,integer,integer,uuid),public.admin_set_tutorial_publication(text,integer,boolean,uuid) to authenticated;
revoke all on function public.get_tutorial_index(),public.get_published_tutorial(text),public.get_tutorials() from public;
grant execute on function public.get_tutorial_index(),public.get_published_tutorial(text),public.get_tutorials() to anon,authenticated;
commit;
-- Verify: select to_regprocedure('public.get_published_tutorial(text)');
