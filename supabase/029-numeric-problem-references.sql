-- Numeric problem references; legacy source/ref links remain readable. No content/progress DML.
begin;
DO $baseline$ BEGIN
IF md5(replace(pg_get_functiondef('public.validate_tutorial_extended_block(jsonb)'::regprocedure),E'\r\n',E'\n'))<>'1971735e00e2bb5ba985713a297069f2' THEN RAISE EXCEPTION '029 baseline changed or already applied; re-audit instead of replaying';END IF;
IF md5(replace(pg_get_functiondef('public.validate_tutorial_publication(text,jsonb)'::regprocedure),E'\r\n',E'\n'))<>'9f866c7b3439bd45d062ce46efbb7e0b' THEN RAISE EXCEPTION '029 baseline changed or already applied; re-audit instead of replaying';END IF;
END;$baseline$;
CREATE OR REPLACE FUNCTION public.validate_tutorial_extended_block(b jsonb)
 RETURNS void
 LANGUAGE plpgsql
 IMMUTABLE
 SET search_path TO ''
AS $function$
declare typ text:=b->>'type';item jsonb;row_value jsonb;cell jsonb;n numeric;ids text[]:='{}';edge jsonb;id text;
begin
 if typ='rich' then perform public.validate_tutorial_inline(b->'content');
 elsif typ='heading' then
  perform public.tutorial_require_text(b->'text',200);
  if jsonb_typeof(b->'level') is distinct from 'number' or (b->>'level')::numeric not between 1 and 4 or (b->>'level')::numeric<>trunc((b->>'level')::numeric) then raise exception 'Expected H1-H4.' using errcode='22023';end if;
 elsif typ='divider' then return;
 elsif typ in ('callout','quote') then
  if b ? 'content' then perform public.validate_tutorial_inline(b->'content');else perform public.tutorial_require_text(b->'text',40000);end if;
  if b ? 'title' and (jsonb_typeof(b->'title')<>'string' or length(b->>'title')>200) then raise exception 'Invalid callout title.' using errcode='22023';end if;
  if typ='callout' and coalesce(b->>'tone','') not in ('note','important','warning','example','proof','observation','complexity','mistake') then raise exception 'Invalid callout tone.' using errcode='22023';end if;
 elsif typ='checklist' then
  if jsonb_typeof(b->'items') is distinct from 'array' then raise exception 'Invalid checklist.' using errcode='22023';end if;
  if jsonb_array_length(b->'items') not between 1 and 100 then raise exception 'Invalid checklist size.' using errcode='22023';end if;
  for item in select value from jsonb_array_elements(b->'items') loop
   perform public.tutorial_require_text(item->'text',8000);if jsonb_typeof(item->'checked') is distinct from 'boolean' then raise exception 'Invalid checklist state.' using errcode='22023';end if;
  end loop;
 elsif typ='image' then
  perform public.tutorial_require_text(b->'alt',500);
  if coalesce(b->>'path','') !~ '^[a-z0-9-]{1,80}/[0-9a-f-]{36}/[0-9a-f-]{36}\.webp$' or coalesce(b->>'align','') not in ('left','center','right') then raise exception 'Invalid image reference.' using errcode='22023';end if;
  if jsonb_typeof(b->'width') is distinct from 'number' or (b->>'width')::numeric not between 20 and 100 or (b->>'width')::numeric<>trunc((b->>'width')::numeric) then raise exception 'Image width must be 20-100 percent.' using errcode='22023';end if;
 elsif typ='problem' then
  if coalesce(b->>'problemKey','') !~ '^([1-9][0-9]{0,15}|[a-zA-Z0-9 ._-]+\|[a-zA-Z0-9_/-]+)$' then raise exception 'Invalid embedded problem.' using errcode='22023';end if;
 elsif typ='tutorial' then
  if coalesce(b->>'tutorialId','') !~ '^[a-z0-9-]{1,80}$' then raise exception 'Invalid embedded tutorial.' using errcode='22023';end if;
 elsif typ='diagram' then
  if coalesce(b->>'kind','') not in ('array','dp','graph','tree') then raise exception 'Invalid diagram type.' using errcode='22023';end if;
  if b->>'kind' in ('array','dp') then
   if jsonb_typeof(b->'rows') is distinct from 'array' then raise exception 'Invalid diagram rows.' using errcode='22023';end if;
   if jsonb_array_length(b->'rows') not between 1 and 20 then raise exception 'Invalid diagram row count.' using errcode='22023';end if;
   for row_value in select value from jsonb_array_elements(b->'rows') loop
    if jsonb_typeof(row_value) is distinct from 'array' then raise exception 'Invalid diagram row.' using errcode='22023';end if;
    if jsonb_array_length(row_value) not between 1 and 30 then raise exception 'Invalid diagram cells.' using errcode='22023';end if;
    for cell in select value from jsonb_array_elements(row_value) loop perform public.tutorial_require_text(cell,500);end loop;
   end loop;
  else
   if jsonb_typeof(b->'nodes') is distinct from 'array' or jsonb_typeof(b->'edges') is distinct from 'array' then raise exception 'Invalid graph diagram.' using errcode='22023';end if;
   if jsonb_array_length(b->'nodes') not between 1 and 30 or jsonb_array_length(b->'edges')>100 then raise exception 'Graph diagram too large.' using errcode='22023';end if;
   for item in select value from jsonb_array_elements(b->'nodes') loop
    perform public.tutorial_require_text(item->'id',50);perform public.tutorial_require_text(item->'label',500);id:=item->>'id';if id=any(ids) then raise exception 'Duplicate diagram node.' using errcode='22023';end if;ids:=array_append(ids,id);
    foreach id in array array['x','y'] loop
     if item ? id then
      if jsonb_typeof(item->id) is distinct from 'number' then raise exception 'Invalid diagram coordinate.' using errcode='22023';end if;n:=(item->>id)::numeric;if n not between 5 and 95 then raise exception 'Diagram coordinates must be 5-95.' using errcode='22023';end if;
     end if;
    end loop;
   end loop;
   for edge in select value from jsonb_array_elements(b->'edges') loop
    if jsonb_typeof(edge) is distinct from 'array' then raise exception 'Invalid diagram edge.' using errcode='22023';end if;
    if jsonb_array_length(edge)<>2 or not ((edge->>0)=any(ids)) or not ((edge->>1)=any(ids)) then raise exception 'Unknown diagram node.' using errcode='22023';end if;
   end loop;
  end if;
  if b ? 'highlights' then
   if jsonb_typeof(b->'highlights') is distinct from 'array' or jsonb_array_length(b->'highlights')>100 then raise exception 'Invalid highlights.' using errcode='22023';end if;
   for item in select value from jsonb_array_elements(b->'highlights') loop perform public.tutorial_require_text(item,50);end loop;
  end if;
 else raise exception 'Unsupported tutorial block type.' using errcode='22023';
 end if;
 if b ? 'caption' and (jsonb_typeof(b->'caption')<>'string' or length(b->>'caption')>2000) then raise exception 'Invalid caption.' using errcode='22023';end if;
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
  if jsonb_array_length(rel->'practice') not between 1 and 30 or jsonb_array_length(rel->'variants')>20 then raise exception 'Expected 1-30 practice tasks, at most 20 variants.' using errcode='22023';end if;
  if not exists(select 1 from jsonb_array_elements(rel->'practice') x where x->'priority'='true'::jsonb) then raise exception 'Select at least one priority task.' using errcode='22023';end if;
  if (select count(*)<>count(distinct value->>'key') from jsonb_array_elements(rel->'practice')) then raise exception 'Duplicate practice task.' using errcode='22023';end if;
  for row_value in select value from jsonb_array_elements(rel->'practice') loop
   k:=row_value->>'key';
   if not exists(select 1 from public.problem_catalog where not archived and (number::text=k or coalesce('cses|'||(regexp_match(body->>'url','^https://cses[.]fi/problemset/task/([0-9]+)/?([?#].*)?$'))[1],lower(btrim(body->>'source'))||'|'||lower(btrim(body->>'ref')))=k)) then raise exception 'Unknown practice task: %',k using errcode='22023';end if;
   if coalesce(row_value->>'stage','') not in ('Warm-up','Standard','Observation','Application','Challenge','Olympiad extension') or jsonb_typeof(row_value->'priority') is distinct from 'boolean' then raise exception 'Invalid practice stage/priority.' using errcode='22023';end if;
   if row_value->'priority'='true'::jsonb then perform public.tutorial_require_text(row_value->'reason',1000);end if;
   if row_value ? 'objective' and (jsonb_typeof(row_value->'objective')<>'string' or length(row_value->>'objective')>1500) then raise exception 'Invalid learning objective.' using errcode='22023';end if;
  end loop;
  for row_value in select value from jsonb_array_elements(rel->'variants') loop
   if coalesce(row_value->>'tutorialId','') !~ '^[a-z0-9-]{1,80}$' or row_value->>'tutorialId'=p_id or not exists(select 1 from public.tutorial_catalog where id=row_value->>'tutorialId' and published) then raise exception 'Invalid variant ID.' using errcode='22023';end if;
   perform public.tutorial_require_text(row_value->'description',1000);
   if row_value ? 'descriptionEn' and (jsonb_typeof(row_value->'descriptionEn')<>'string' or length(row_value->>'descriptionEn')>1000) then raise exception 'Invalid variant description.' using errcode='22023';end if;
  end loop;
  if rel->>'next' is not null and ((rel->>'next') !~ '^[a-z0-9-]{1,80}$' or rel->>'next'=p_id or not exists(select 1 from public.tutorial_catalog where id=rel->>'next' and published)) then raise exception 'Invalid next tutorial.' using errcode='22023';end if;
 end if;
 return;
end;
$function$
;
commit;
