-- Reconciles the verified production baseline; do not replay 008 or seed data.
-- Only adds the missing optional prerequisiteIds validation. Existing rows are untouched.
-- Fail closed if this function changed after the audited baseline.
DO $baseline$
BEGIN
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure), E'\r\n', E'\n'))
    NOT IN ('4b03c9840e3e4e05b946250042137052', 'e2a74e4373b8106c0360a141d5468378') THEN
  RAISE EXCEPTION 'validate_tutorial_body differs from the audited baseline; re-audit before applying 021';
 END IF;
END;
$baseline$;

create or replace function public.validate_tutorial_body(p_id text,p_body jsonb) returns void
language plpgsql immutable set search_path='' as $fn$
declare lang text; v jsonb; s jsonb; b jsonb; item jsonb; cell jsonb; row_value jsonb; typ text; cols integer; ord numeric;
begin
 if p_id is null or p_id !~ '^[a-z0-9-]{1,80}$' or jsonb_typeof(p_body) is distinct from 'object' or p_body->>'id' is distinct from p_id or length(p_body::text)>300000 then
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
  if jsonb_typeof(v) is distinct from 'object' then raise exception 'Both languages are required.' using errcode='22023'; end if;
  perform public.tutorial_require_text(v->'title',200);
  perform public.tutorial_require_text(v->'summary',4000);
  perform public.tutorial_require_text(v->'prerequisites',2000);
  if jsonb_typeof(v->'sections') is distinct from 'array' then raise exception 'Invalid tutorial sections.' using errcode='22023'; end if;
  if jsonb_array_length(v->'sections') not between 1 and 30 then raise exception 'Expected 1-30 sections.' using errcode='22023'; end if;
  for s in select value from jsonb_array_elements(v->'sections') loop
   if jsonb_typeof(s) is distinct from 'object' then raise exception 'Invalid section.' using errcode='22023'; end if;
   perform public.tutorial_require_text(s->'title',200);
   if jsonb_typeof(s->'blocks') is distinct from 'array' then raise exception 'Invalid section content.' using errcode='22023'; end if;
   if jsonb_array_length(s->'blocks') not between 1 and 40 then raise exception 'Expected 1-40 content blocks.' using errcode='22023'; end if;
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
    else raise exception 'Unsupported tutorial block type.' using errcode='22023';
    end if;
   end loop;
  end loop;
 end loop;
end;
$fn$;
