-- Recovery 021-tutorial-content-blocks.sql -> 022-tutorial-content-blocks.sql; production 021 prerequisite validation is distinct.
-- Purpose: typed rich/media/diagram blocks; legacy 55 lessons remain valid.
-- Dependency: 008. No content rows or progress are rewritten.
begin;
-- Refuse a stale rollout: audit again if an admin changed the validator.
DO $baseline$
BEGIN
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure), E'\r\n', E'\n')) <> 'e2a74e4373b8106c0360a141d5468378' THEN
  RAISE EXCEPTION '022 requires the verified prerequisite-validator baseline; re-audit instead of replaying';
 END IF;
 IF to_regprocedure('public.validate_tutorial_extended_block(jsonb)') IS NOT NULL THEN
  RAISE EXCEPTION 'Editor blocks already exist; inspect migration contents before applying';
 END IF;
END;
$baseline$;

create or replace function public.safe_tutorial_link(p_url text) returns boolean
language sql immutable set search_path='' as $$
 select coalesce(p_url ~ '^https://[^/@[:space:]]+([/?#][^[:space:]]*)?$' or p_url ~ '^#(tutorial/[a-z0-9-]{1,80}(/part/[0-9]+)?|tutorials|library|plan(/[0-9]+)?|profile(/[a-zA-Z0-9_-]+)?)$',false) and length(p_url)<=1000;
$$;
create or replace function public.validate_tutorial_inline(p_content jsonb) returns void
language plpgsql immutable set search_path='' as $$
declare item jsonb;mark jsonb;total integer:=0;nonempty boolean:=false;
begin
 if jsonb_typeof(p_content) is distinct from 'array' then raise exception 'Invalid rich text.' using errcode='22023';end if;
 if jsonb_array_length(p_content) not between 1 and 1000 then raise exception 'Invalid rich text size.' using errcode='22023';end if;
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
 if not nonempty or total>40000 then raise exception 'Rich text is empty or too large.' using errcode='22023';end if;
end;
$$;
create or replace function public.validate_tutorial_extended_block(b jsonb) returns void
language plpgsql immutable set search_path='' as $$
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
  if coalesce(b->>'problemKey','') !~ '^[a-zA-Z0-9 ._-]+\|[a-zA-Z0-9_/-]+$' then raise exception 'Invalid embedded problem.' using errcode='22023';end if;
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
$$;
revoke all on function public.safe_tutorial_link(text),public.validate_tutorial_inline(jsonb),public.validate_tutorial_extended_block(jsonb) from public,anon,authenticated;
create or replace function public.validate_tutorial_body(p_id text,p_body jsonb) returns void
language plpgsql immutable set search_path='' as $fn$
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
 perform public.tutorial_require_text(p_body->'category',80);
 perform public.tutorial_require_text(p_body->'aliases',2000);
 if jsonb_typeof(p_body->'related') is distinct from 'array' then raise exception 'Invalid related topics.' using errcode='22023'; end if;
 if jsonb_array_length(p_body->'related')>30 then raise exception 'Too many related topics.' using errcode='22023'; end if;
 for item in select value from jsonb_array_elements(p_body->'related') loop
  if jsonb_typeof(item)<>'string' or (item#>>'{}') !~ '^[a-z0-9-]{1,80}$' then raise exception 'Invalid related topic ID.' using errcode='22023'; end if;
 end loop;
 foreach lang in array array['mn','en'] loop
  v:=case when lang='mn' then p_body else p_body#>'{translations,en}' end;
  if lang='en' and (v is null or v='null'::jsonb) then continue; end if;
  if jsonb_typeof(v) is distinct from 'object' then raise exception 'Both languages are required.' using errcode='22023'; end if;
  perform public.tutorial_require_text(v->'title',200);
  perform public.tutorial_require_text(v->'summary',4000);
  perform public.tutorial_require_text(v->'prerequisites',2000);
  if jsonb_typeof(v->'sections') is distinct from 'array' then raise exception 'Invalid tutorial sections.' using errcode='22023'; end if;
  if jsonb_array_length(v->'sections') not between 1 and 80 then raise exception 'Expected 1-80 sections.' using errcode='22023'; end if;
  for s in select value from jsonb_array_elements(v->'sections') loop
   if jsonb_typeof(s) is distinct from 'object' then raise exception 'Invalid section.' using errcode='22023'; end if;
   perform public.tutorial_require_text(s->'title',200);
   if jsonb_typeof(s->'blocks') is distinct from 'array' then raise exception 'Invalid section content.' using errcode='22023'; end if;
   if jsonb_array_length(s->'blocks') not between 1 and 100 then raise exception 'Expected 1-100 content blocks.' using errcode='22023'; end if;
   for b in select value from jsonb_array_elements(s->'blocks') loop
    if jsonb_typeof(b) is distinct from 'object' then raise exception 'Invalid content block.' using errcode='22023'; end if;
    typ:=b->>'type';
    if typ in ('p','note','code') then perform public.tutorial_require_text(b->'text',40000);
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
$fn$;
revoke all on function public.validate_tutorial_body(text,jsonb) from public,anon,authenticated;
-- Validate current live documents in the same transaction; rollback DDL on failure.
-- Reads current bodies rather than importing stale recovery JSON.
DO $compatibility$
DECLARE lesson record;
BEGIN
 FOR lesson IN SELECT id, body FROM public.tutorial_catalog LOOP
  PERFORM public.validate_tutorial_body(lesson.id, lesson.body);
 END LOOP;
END;
$compatibility$;
commit;
-- Verify: select to_regprocedure('public.validate_tutorial_extended_block(jsonb)');
