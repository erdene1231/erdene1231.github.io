-- Optional tutorial metadata/empty content, plus owner-only published-draft reset. No content installation DML.
begin;
DO $baseline$ BEGIN
 IF to_regprocedure('public.tutorial_optional_text(jsonb,integer)') IS NOT NULL OR to_regprocedure('public.admin_reset_tutorial_draft(text,integer,integer,uuid)') IS NOT NULL THEN RAISE EXCEPTION '031 already exists; re-audit instead of replaying';END IF;
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure),E'\r\n',E'\n'))<>'d17381308438362f364065137f8ad1a2' THEN RAISE EXCEPTION '031 baseline changed or already applied; re-audit';END IF;
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_inline(jsonb)'::regprocedure),E'\r\n',E'\n'))<>'fca77778ec2755c6b82694ca389bec89' THEN RAISE EXCEPTION '031 baseline changed or already applied; re-audit';END IF;
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_publication(text,jsonb)'::regprocedure),E'\r\n',E'\n'))<>'452336e2346caf0b7b0671a318050678' THEN RAISE EXCEPTION '031 baseline changed or already applied; re-audit';END IF;
 IF md5(replace(pg_get_functiondef('public.admin_publish_tutorial_draft(text,jsonb,integer,integer,uuid)'::regprocedure),E'\r\n',E'\n'))<>'81108a26f946a44fdb092377979d0ce6' THEN RAISE EXCEPTION '031 baseline changed or already applied; re-audit';END IF;
END;$baseline$;
create function public.tutorial_optional_text(p_value jsonb,p_max integer) returns void
language plpgsql immutable set search_path='' as $$begin
 if p_value is not null and (jsonb_typeof(p_value) is distinct from 'string' or length(p_value#>>'{}')>p_max) then raise exception 'Invalid optional text.' using errcode='22023';end if;
end;$$;
revoke all on function public.tutorial_optional_text(jsonb,integer) from public,anon,authenticated;
CREATE OR REPLACE FUNCTION public.validate_tutorial_body(p_id text, p_body jsonb)
 RETURNS void
 LANGUAGE plpgsql
 IMMUTABLE
 SET search_path TO ''
AS $function$
declare lang text; v jsonb; s jsonb; b jsonb; item jsonb; cell jsonb; row_value jsonb; typ text; cols integer; ord numeric;
begin
 if p_id is null or p_id !~ '^[a-z0-9-]{1,80}$' or jsonb_typeof(p_body) is distinct from 'object' or p_body->>'id' is distinct from p_id or length(p_body::text)>1000000 then
  raise exception 'Invalid tutorial ID or payload.' using errcode='22023';
 end if;
 if coalesce(p_body->>'levelKey','') not in ('beginner','intermediate','advanced') or jsonb_typeof(p_body->'order') is distinct from 'number' then
  raise exception 'Invalid tutorial level or order.' using errcode='22023';
 end if;
 ord:=(p_body->>'order')::numeric;
 if ord<>trunc(ord) or ord not between 1 and 1000 then raise exception 'Invalid tutorial order.' using errcode='22023'; end if;
 if p_body ? 'prerequisiteIds' then
  if jsonb_typeof(p_body->'prerequisiteIds') is distinct from 'array' then raise exception 'Invalid prerequisites.' using errcode='22023'; end if;
  if jsonb_array_length(p_body->'prerequisiteIds')>30 then raise exception 'Too many prerequisites.' using errcode='22023'; end if;
  for item in select value from jsonb_array_elements(p_body->'prerequisiteIds') loop
   if jsonb_typeof(item)<>'string' or (item#>>'{}') !~ '^[a-z0-9-]{1,80}$' then raise exception 'Invalid prerequisite ID.' using errcode='22023'; end if;
  end loop;
 end if;
 perform public.tutorial_optional_text(p_body->'category',80);
 perform public.tutorial_optional_text(p_body->'aliases',2000);
 if jsonb_typeof(coalesce(p_body->'related','[]'::jsonb)) is distinct from 'array' then raise exception 'Invalid related topics.' using errcode='22023'; end if;
 if jsonb_array_length(coalesce(p_body->'related','[]'::jsonb))>30 then raise exception 'Too many related topics.' using errcode='22023'; end if;
 for item in select value from jsonb_array_elements(coalesce(p_body->'related','[]'::jsonb)) loop
  if jsonb_typeof(item)<>'string' or (item#>>'{}') !~ '^[a-z0-9-]{1,80}$' then raise exception 'Invalid related topic ID.' using errcode='22023'; end if;
 end loop;
 foreach lang in array array['mn','en'] loop
  v:=case when lang='mn' then p_body else p_body#>'{translations,en}' end;
  if lang='en' and (v is null or v='null'::jsonb) then continue; end if;
  if jsonb_typeof(v) is distinct from 'object' then raise exception 'Both languages are required.' using errcode='22023'; end if;
  if lang='mn' then perform public.tutorial_require_text(v->'title',200);else perform public.tutorial_optional_text(v->'title',200);end if;
  perform public.tutorial_optional_text(v->'summary',4000);
  perform public.tutorial_optional_text(v->'prerequisites',2000);
  if jsonb_typeof(v->'sections') is distinct from 'array' then raise exception 'Invalid tutorial sections.' using errcode='22023'; end if;
  if jsonb_array_length(v->'sections') not between 0 and 80 then raise exception 'Expected 0-80 sections.' using errcode='22023'; end if;
  for s in select value from jsonb_array_elements(v->'sections') loop
   if jsonb_typeof(s) is distinct from 'object' then raise exception 'Invalid section.' using errcode='22023'; end if;
   perform public.tutorial_optional_text(s->'title',200);
   if jsonb_typeof(s->'blocks') is distinct from 'array' then raise exception 'Invalid section content.' using errcode='22023'; end if;
   if jsonb_array_length(s->'blocks') not between 0 and 100 then raise exception 'Expected 0-100 content blocks.' using errcode='22023'; end if;
   for b in select value from jsonb_array_elements(s->'blocks') loop
    if jsonb_typeof(b) is distinct from 'object' then raise exception 'Invalid content block.' using errcode='22023'; end if;
    typ:=b->>'type';
    if typ in ('p','note','code') then perform public.tutorial_optional_text(b->'text',40000);
    elsif typ='math' then perform public.tutorial_require_text(b->'tex',8000);
    elsif typ in ('list','ordered') then
     if jsonb_typeof(b->'items') is distinct from 'array' then raise exception 'Invalid list.' using errcode='22023'; end if;
     if jsonb_array_length(b->'items') not between 1 and 100 then raise exception 'Invalid list length.' using errcode='22023'; end if;
     for item in select value from jsonb_array_elements(b->'items') loop perform public.tutorial_require_text(item,8000); end loop;
    elsif typ='table' then
     if jsonb_typeof(b->'headers') is distinct from 'array' or jsonb_typeof(b->'rows') is distinct from 'array' then raise exception 'Invalid table.' using errcode='22023'; end if;
     cols:=jsonb_array_length(b->'headers');
     if cols not between 1 and 8 or jsonb_array_length(b->'rows') not between 1 and 100 then raise exception 'Invalid table dimensions.' using errcode='22023'; end if;
     for cell in select value from jsonb_array_elements(b->'headers') loop perform public.tutorial_require_text(cell,200); end loop;
     for row_value in select value from jsonb_array_elements(b->'rows') loop
      if jsonb_typeof(row_value) is distinct from 'array' then raise exception 'Invalid table row.' using errcode='22023'; end if;
      if jsonb_array_length(row_value)<>cols then raise exception 'Table column counts differ.' using errcode='22023'; end if;
      for cell in select value from jsonb_array_elements(row_value) loop perform public.tutorial_require_text(cell,8000); end loop;
     end loop;
    elsif typ='links' then
     if jsonb_typeof(b->'items') is distinct from 'array' then raise exception 'Invalid links.' using errcode='22023'; end if;
     if jsonb_array_length(b->'items') not between 1 and 30 then raise exception 'Invalid links length.' using errcode='22023'; end if;
     for item in select value from jsonb_array_elements(b->'items') loop
      perform public.tutorial_require_text(item->'label',300);perform public.tutorial_require_text(item->'url',1000);
      if item->>'url' !~ '^https://[^/@[:space:]]+([/?#][^[:space:]]*)?$' then raise exception 'HTTPS links are required.' using errcode='22023'; end if;
     end loop;
    else perform public.validate_tutorial_extended_block(b);
    end if;
   end loop;
  end loop;
 end loop;
end;
$function$
;
CREATE OR REPLACE FUNCTION public.validate_tutorial_inline(p_content jsonb)
 RETURNS void
 LANGUAGE plpgsql
 IMMUTABLE
 SET search_path TO ''
AS $function$
declare item jsonb;mark jsonb;total integer:=0;nonempty boolean:=false;
begin
 if jsonb_typeof(p_content) is distinct from 'array' then raise exception 'Invalid rich text.' using errcode='22023';end if;
 if jsonb_array_length(p_content) not between 0 and 1000 then raise exception 'Invalid rich text size.' using errcode='22023';end if;
 for item in select value from jsonb_array_elements(p_content) loop
  if jsonb_typeof(item->'text') is distinct from 'string' or length(item->>'text')>40000 then raise exception 'Invalid rich text item.' using errcode='22023';end if;
  total:=total+length(item->>'text');nonempty:=nonempty or length(btrim(item->>'text'))>0;
  if item ? 'marks' then
   if jsonb_typeof(item->'marks') is distinct from 'array' or jsonb_array_length(item->'marks')>20 then raise exception 'Invalid rich marks.' using errcode='22023';end if;
   for mark in select value from jsonb_array_elements(item->'marks') loop
    if jsonb_typeof(mark)<>'string' or (mark#>>'{}') not in ('bold','italic','underline','strike','code') then raise exception 'Unsupported rich mark.' using errcode='22023';end if;
   end loop;
  end if;
  if item ? 'href' and not public.safe_tutorial_link(item->>'href') then raise exception 'Unsafe inline link.' using errcode='22023';end if;
 end loop;
 if total>40000 then raise exception 'Rich text is empty or too large.' using errcode='22023';end if;
end;
$function$
;
CREATE OR REPLACE FUNCTION public.validate_tutorial_publication(p_id text, p_body jsonb)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
declare item jsonb;rel jsonb;row_value jsonb;k text;cycle_found boolean;
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if p_body ? '_draftRelationsText' then raise exception 'Private draft metadata cannot be published.' using errcode='22023';end if;
 perform public.validate_tutorial_body(p_id,p_body);
 for item in select value from jsonb_path_query(p_body,'$.**.problemKey') x(value) loop
  k:=item#>>'{}';
  if k ~ '^[0-9]+$' and not exists(select 1 from public.problem_catalog where not archived and number::text=k) then raise exception 'Unknown embedded problem number: %',k using errcode='22023';end if;
 end loop;
 for item in select value from jsonb_array_elements(coalesce(p_body->'prerequisiteIds','[]'::jsonb)) loop
  if item#>>'{}'=p_id or not exists(select 1 from public.tutorial_catalog where id=item#>>'{}' and published) then raise exception 'Missing published prerequisite: %',item#>>'{}' using errcode='22023';end if;
 end loop;
 with recursive paths(id,path,cycle) as (
  select value#>>'{}',array[p_id,value#>>'{}'],(value#>>'{}')=p_id from jsonb_array_elements(coalesce(p_body->'prerequisiteIds','[]'::jsonb))
  union all select x.value#>>'{}',p.path||(x.value#>>'{}'),(x.value#>>'{}')=any(p.path)
  from paths p join public.tutorial_catalog t on t.id=p.id cross join lateral jsonb_array_elements(coalesce(t.body->'prerequisiteIds','[]'::jsonb)) x(value) where not p.cycle
 ) select exists(select 1 from paths where cycle) into cycle_found;
 if cycle_found then raise exception 'Prerequisite cycle.' using errcode='22023';end if;
 rel:=p_body->'learningRelations';
 if rel is not null then
  if jsonb_typeof(rel) is distinct from 'object' or jsonb_typeof(rel->'practice') is distinct from 'array' or jsonb_typeof(rel->'variants') is distinct from 'array' then raise exception 'Invalid tutorial relationships.' using errcode='22023';end if;
  if jsonb_array_length(rel->'practice') not between 0 and 30 or jsonb_array_length(rel->'variants')>20 then raise exception 'Expected 0-30 practice tasks, at most 20 variants.' using errcode='22023';end if;
  if (select count(*)<>count(distinct value->>'key') from jsonb_array_elements(rel->'practice')) then raise exception 'Duplicate practice task.' using errcode='22023';end if;
  for row_value in select value from jsonb_array_elements(rel->'practice') loop
   k:=row_value->>'key';
   if not exists(select 1 from public.problem_catalog where not archived and (number::text=k or coalesce('cses|'||(regexp_match(body->>'url','^https://cses[.]fi/problemset/task/([0-9]+)/?([?#].*)?$'))[1],lower(btrim(body->>'source'))||'|'||lower(btrim(body->>'ref')))=k)) then raise exception 'Unknown practice task: %',k using errcode='22023';end if;
   if coalesce(row_value->>'stage','') not in ('Warm-up','Standard','Observation','Application','Challenge','Olympiad extension') or jsonb_typeof(row_value->'priority') is distinct from 'boolean' then raise exception 'Invalid practice stage/priority.' using errcode='22023';end if;
   if row_value->'priority'='true'::jsonb then perform public.tutorial_optional_text(row_value->'reason',1000);end if;
   if row_value ? 'objective' and (jsonb_typeof(row_value->'objective')<>'string' or length(row_value->>'objective')>1500) then raise exception 'Invalid learning objective.' using errcode='22023';end if;
  end loop;
  for row_value in select value from jsonb_array_elements(rel->'variants') loop
   if coalesce(row_value->>'tutorialId','') !~ '^[a-z0-9-]{1,80}$' or row_value->>'tutorialId'=p_id or not exists(select 1 from public.tutorial_catalog where id=row_value->>'tutorialId' and published) then raise exception 'Invalid variant ID.' using errcode='22023';end if;
   perform public.tutorial_optional_text(row_value->'description',1000);
   if row_value ? 'descriptionEn' and (jsonb_typeof(row_value->'descriptionEn')<>'string' or length(row_value->>'descriptionEn')>1000) then raise exception 'Invalid variant description.' using errcode='22023';end if;
  end loop;
  if rel->>'next' is not null and ((rel->>'next') !~ '^[a-z0-9-]{1,80}$' or rel->>'next'=p_id or not exists(select 1 from public.tutorial_catalog where id=rel->>'next' and published)) then raise exception 'Invalid next tutorial.' using errcode='22023';end if;
 end if;
 return;
end;
$function$
;
create function public.admin_reset_tutorial_draft(p_id text,p_current_revision integer,p_draft_revision integer,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare t public.tutorial_catalog%rowtype;d public.tutorial_drafts%rowtype;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 select * into t from public.tutorial_catalog where id=p_id for update;
 select * into d from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid() for update;
 if t.id is null or not t.published or t.revision is distinct from p_current_revision or coalesce(d.revision,0) is distinct from p_draft_revision then raise exception 'REVISION_CONFLICT: publication or private draft changed; review again.' using errcode='40001';end if;
 delete from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid();
 return jsonb_build_object('body',t.body,'revision',t.revision,'published',true,'updated_at',t.updated_at,'draft',null);
end;$$;
revoke all on function public.admin_reset_tutorial_draft(text,integer,integer,uuid) from public,anon,authenticated;
grant execute on function public.admin_reset_tutorial_draft(text,integer,integer,uuid) to authenticated;
commit;
