-- Recovery 025-tutorial-reference-integrity.sql -> 026-tutorial-reference-integrity.sql; production 021 prerequisite validation is distinct.
-- Validate embedded MN/EN links and canonical practice keys on publication.
-- Dependencies: 022-025. No content/progress rows are rewritten.
begin;
create or replace function public.tutorial_problem_key(p_body jsonb) returns text
language sql immutable set search_path='' as $$
 select coalesce(
  'cses|'||(regexp_match(p_body->>'url','^https://cses[.]fi/problemset/task/([0-9]+)/?([?#].*)?$'))[1],
  lower(btrim(p_body->>'source'))||'|'||lower(btrim(p_body->>'ref')));
$$;

create or replace function public.tutorial_reference_targets(p_body jsonb)
returns table(kind text,target text,part numeric)
language sql immutable set search_path='' as $$
 with versions(body) as (
  select p_body union all select p_body#>'{translations,en}'
  where jsonb_typeof(p_body#>'{translations,en}')='object'
 ), blocks(body) as (
  select b from versions v
  cross join lateral jsonb_array_elements(coalesce(v.body->'sections','[]'::jsonb)) s
  cross join lateral jsonb_array_elements(coalesce(s->'blocks','[]'::jsonb)) b
 ), inline_links(parts) as (
  select regexp_match(item->>'href','^#tutorial/([a-z0-9-]+)(/part/([0-9]+))?$')
  from blocks cross join lateral jsonb_array_elements(coalesce(body->'content','[]'::jsonb)) item
 )
 select 'tutorial',value#>>'{}',null::numeric from jsonb_array_elements(coalesce(p_body->'prerequisiteIds','[]'::jsonb))
 union all select 'tutorial',value#>>'{}',null from jsonb_array_elements(coalesce(p_body->'related','[]'::jsonb))
 union all select 'tutorial',value->>'tutorialId',null from jsonb_array_elements(coalesce(p_body#>'{learningRelations,variants}','[]'::jsonb))
 union all select 'tutorial',p_body#>>'{learningRelations,next}',null where p_body#>>'{learningRelations,next}' is not null
 union all select 'problem',value->>'key',null from jsonb_array_elements(coalesce(p_body#>'{learningRelations,practice}','[]'::jsonb))
 union all select 'tutorial',body->>'tutorialId',null from blocks where body->>'type'='tutorial'
 union all select 'problem',body->>'problemKey',null from blocks where body->>'type'='problem'
 union all select 'tutorial',parts[1],parts[3]::numeric from inline_links where parts is not null;
$$;

create or replace function public.check_tutorial_reference_integrity() returns trigger
language plpgsql security definer set search_path='' as $$
declare ref record;destination jsonb;removed_id text;
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if tg_op='DELETE' then removed_id:=old.id;
 elsif not new.published then removed_id:=new.id;
 end if;
 if removed_id is not null then
  if exists(select 1 from public.tutorial_catalog t
   cross join lateral public.tutorial_reference_targets(t.body) r
   where t.published and t.id<>removed_id and r.kind='tutorial' and r.target=removed_id)
  then raise exception 'A published tutorial still links to this lesson.' using errcode='22023';end if;
  if tg_op='DELETE' then return old;else return new;end if;
 end if;
 if exists(select 1 from public.tutorial_catalog t
  cross join lateral public.tutorial_reference_targets(t.body) r
  where t.published and t.id<>new.id and r.kind='tutorial' and r.target=new.id
   and r.part>=jsonb_array_length(new.body->'sections'))
 then raise exception 'A published tutorial links to a section being removed.' using errcode='22023';end if;
 for ref in select * from public.tutorial_reference_targets(new.body) loop
  if ref.kind='problem' then
   if not exists(select 1 from public.problem_catalog p where not p.archived
     and public.tutorial_problem_key(p.body)=ref.target)
   then raise exception 'Unknown embedded/practice problem: %',ref.target using errcode='22023';end if;
  else
   if ref.target=new.id then destination:=new.body;
   else select body into destination from public.tutorial_catalog where id=ref.target and published;end if;
   if destination is null then raise exception 'Unknown published tutorial reference: %',ref.target using errcode='22023';end if;
   if ref.part is not null and (ref.part<0 or ref.part>=jsonb_array_length(destination->'sections'))
   then raise exception 'Unknown tutorial section: %/part/%',ref.target,ref.part using errcode='22023';end if;
  end if;
 end loop;
 return new;
end;
$$;
revoke all on function public.tutorial_problem_key(jsonb),public.tutorial_reference_targets(jsonb),
 public.check_tutorial_reference_integrity() from public,anon,authenticated;
drop trigger if exists tutorial_reference_integrity on public.tutorial_catalog;
create trigger tutorial_reference_integrity before insert or update or delete on public.tutorial_catalog
 for each row execute function public.check_tutorial_reference_integrity();
commit;
-- Verify: select to_regprocedure('public.tutorial_reference_targets(jsonb)');
