-- Native single-answer practice quizzes and three licensed same-origin illustrations.
-- Extends the existing validator only; no content DML, roles, grants or policies.
begin;
DO $guard$ BEGIN
 IF md5(pg_get_functiondef('public.validate_tutorial_extended_block(jsonb)'::regprocedure))<> '4f4a2b6a409329faef8925286de3bc15' OR (select proacl::text from pg_proc where oid='public.validate_tutorial_extended_block(jsonb)'::regprocedure) is distinct from '{postgres=X/postgres,service_role=X/postgres}' OR (select prosecdef from pg_proc where oid='public.validate_tutorial_extended_block(jsonb)'::regprocedure) THEN
  RAISE EXCEPTION '041 validator baseline drift/already applied; inspect instead of replaying';
 END IF;
END $guard$;
CREATE OR REPLACE FUNCTION public.validate_tutorial_extended_block(b jsonb)
 RETURNS void
 LANGUAGE plpgsql
 IMMUTABLE
 SET search_path TO ''
AS $function$
declare typ text:=b->>'type';item jsonb;row_value jsonb;cell jsonb;n numeric;ids text[]:='{}';edge jsonb;id text;
begin
 if typ='quiz' then
  perform public.tutorial_require_text(b->'quizId',80);
  if b->>'quizId' !~ '^[a-zA-Z0-9_-]{1,80}$' then raise exception 'Invalid quiz ID.' using errcode='22023';end if;
  perform public.tutorial_require_text(b->'question',4000);
  perform public.tutorial_require_text(b->'explanation',8000);
  if jsonb_typeof(b->'options') is distinct from 'array' then raise exception 'Quiz options must be an array.' using errcode='22023';end if;
  if jsonb_array_length(b->'options') not between 2 and 6 then raise exception 'Quiz requires2-6 options.' using errcode='22023';end if;
  for item in select value from jsonb_array_elements(b->'options') loop
   if jsonb_typeof(item) is distinct from 'object' then raise exception 'Invalid quiz option.' using errcode='22023';end if;
   perform public.tutorial_require_text(item->'id',80);perform public.tutorial_require_text(item->'text',2000);
   id:=item->>'id';if id !~ '^[a-zA-Z0-9_-]{1,80}$' or id=any(ids) then raise exception 'Invalid or duplicate option ID.' using errcode='22023';end if;ids:=array_append(ids,id);
  end loop;
  perform public.tutorial_require_text(b->'answerId',80);
  if not((b->>'answerId')=any(ids)) then raise exception 'Quiz answer must name one option.' using errcode='22023';end if;
 elsif typ='rich' then perform public.validate_tutorial_inline(b->'content');
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
  if not coalesce(((coalesce(b->>'path','') ~ '^[a-z0-9-]{1,80}/[0-9a-f-]{36}/[0-9a-f-]{36}\.webp$' and not(b?'assetPath')) or
   (coalesce(b->>'path','')='' and jsonb_typeof(b->'assetPath')='string' and b->>'assetPath'=any(array['tutorial-assets/cpp-environment/cpp-extension.webp','tutorial-assets/cpp-environment/msys2-toolchain.webp','tutorial-assets/cpp-environment/devcpp-historical.webp']))),false)
   or coalesce(b->>'align','') not in ('left','center','right') then raise exception 'Invalid image reference.' using errcode='22023';end if;
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
$function$;
DO $verify$ BEGIN
 IF (select proacl::text from pg_proc where oid='public.validate_tutorial_extended_block(jsonb)'::regprocedure) is distinct from '{postgres=X/postgres,service_role=X/postgres}' OR (select prosecdef from pg_proc where oid='public.validate_tutorial_extended_block(jsonb)'::regprocedure) THEN RAISE EXCEPTION '041 validator access changed';END IF;
END $verify$;
commit;
