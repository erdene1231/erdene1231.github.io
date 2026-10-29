-- Optional presentation validation only. Existing function privileges are retained.
-- No table data, roles, grants, RLS or Storage changes.
do $guard$ begin
 if md5(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure)) <> 'f214981e444e2f89f3fc4a79e841e890' or (select proacl::text from pg_proc where oid='public.validate_tutorial_body(text,jsonb)'::regprocedure) is distinct from '{postgres=X/postgres,service_role=X/postgres}' then raise exception '037 validator baseline drift or migration already applied.';end if;
end $guard$;
CREATE OR REPLACE FUNCTION public.validate_tutorial_body(p_id text, p_body jsonb)
 RETURNS void
 LANGUAGE plpgsql
 IMMUTABLE
 SET search_path TO ''
AS $function$
declare lang text; v jsonb; s jsonb; b jsonb; item jsonb; cell jsonb; row_value jsonb; typ text; cols integer; ord numeric; grid jsonb; entry jsonb; nr integer; nc integer; gr integer; gc integer; rs integer; cs integer; rr integer; cc integer; num numeric; grid_field text; coord text; painted text[]; occupied text[];
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
    -- Optional cell presentation, leaving original strings and legacy grids unchanged.
    if (typ='table' or (typ='diagram' and b->>'kind' in ('array','dp'))) and b ? 'gridPresentation' then
     grid:=b->'gridPresentation';
     if jsonb_typeof(grid) is distinct from 'object' or exists(select 1 from jsonb_object_keys(grid) x where x not in ('colors','merges')) then raise exception 'Invalid grid presentation.' using errcode='22023';end if;
     if jsonb_typeof(b->'rows') is distinct from 'array' then raise exception 'Invalid grid rows.' using errcode='22023';end if;
     nr:=jsonb_array_length(b->'rows');
     if nr<1 or nr>(case when typ='table' then 100 else 20 end) or jsonb_typeof(b->'rows'->0) is distinct from 'array' then raise exception 'Invalid grid dimensions.' using errcode='22023';end if;
     nc:=jsonb_array_length(b->'rows'->0);
     if nc<1 or nc>(case when typ='table' then 8 else 30 end) then raise exception 'Invalid grid columns.' using errcode='22023';end if;
     for row_value in select value from jsonb_array_elements(b->'rows') loop
      if jsonb_typeof(row_value) is distinct from 'array' then raise exception 'Invalid grid row.' using errcode='22023';end if;
      if jsonb_array_length(row_value)<>nc then raise exception 'Grid must be rectangular.' using errcode='22023';end if;
     end loop;
     foreach grid_field in array array['colors','merges'] loop
      if grid ? grid_field then
       if jsonb_typeof(grid->grid_field) is distinct from 'array' then raise exception 'Invalid grid list.' using errcode='22023';end if;
       if jsonb_array_length(grid->grid_field)>nr*nc then raise exception 'Too many grid entries.' using errcode='22023';end if;
      end if;
     end loop;
     painted:=array[]::text[];occupied:=array[]::text[];
     for entry in select value from jsonb_array_elements(coalesce(grid->'colors','[]'::jsonb)) loop
      if jsonb_typeof(entry) is distinct from 'object' then raise exception 'Invalid grid color.' using errcode='22023';end if;
      if exists(select 1 from jsonb_object_keys(entry) x where x not in ('row','col','color')) or jsonb_typeof(entry->'color') is distinct from 'string' or entry->>'color' !~ '^#[0-9a-fA-F]{6}$' then raise exception 'Invalid grid color.' using errcode='22023';end if;
      foreach grid_field in array array['row','col'] loop
       if jsonb_typeof(entry->grid_field) is distinct from 'number' then raise exception 'Invalid grid coordinate.' using errcode='22023';end if;
       num:=(entry->>grid_field)::numeric;
       if num<>trunc(num) or num<0 or num>=(case when grid_field='row' then nr else nc end) then raise exception 'Grid coordinate out of bounds.' using errcode='22023';end if;
      end loop;
      coord:=(entry->>'row')::numeric::integer||':'||(entry->>'col')::numeric::integer;
      if coord=any(painted) then raise exception 'Duplicate grid color.' using errcode='22023';end if;
      painted:=array_append(painted,coord);
     end loop;
     for entry in select value from jsonb_array_elements(coalesce(grid->'merges','[]'::jsonb)) loop
      if jsonb_typeof(entry) is distinct from 'object' then raise exception 'Invalid grid region.' using errcode='22023';end if;
      if exists(select 1 from jsonb_object_keys(entry) x where x not in ('row','col','rowSpan','colSpan')) then raise exception 'Invalid grid region keys.' using errcode='22023';end if;
      foreach grid_field in array array['row','col','rowSpan','colSpan'] loop
       if jsonb_typeof(entry->grid_field) is distinct from 'number' then raise exception 'Invalid grid region coordinate.' using errcode='22023';end if;
       num:=(entry->>grid_field)::numeric;
       if num<>trunc(num) or num<(case when grid_field in ('rowSpan','colSpan') then 1 else 0 end) or num>(case when grid_field in ('row','rowSpan') then nr else nc end) then raise exception 'Grid region out of bounds.' using errcode='22023';end if;
      end loop;
      gr:=(entry->>'row')::numeric::integer;gc:=(entry->>'col')::numeric::integer;rs:=(entry->>'rowSpan')::numeric::integer;cs:=(entry->>'colSpan')::numeric::integer;
      if rs*cs<2 or gr+rs>nr or gc+cs>nc then raise exception 'Invalid grid region bounds.' using errcode='22023';end if;
      for rr in gr..gr+rs-1 loop for cc in gc..gc+cs-1 loop
       coord:=rr||':'||cc;
       if coord=any(occupied) then raise exception 'Overlapping grid regions.' using errcode='22023';end if;
       occupied:=array_append(occupied,coord);
      end loop;end loop;
     end loop;
    end if;
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
