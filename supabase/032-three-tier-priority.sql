-- 032: three-tier problem/tutorial priority. Additive metadata; no catalog backfill or user-data changes.
-- Dependencies: actual audited schema after031. Preserve021 prerequisites,029 refs,031 optional content/reset.
-- Content ranking/backfill is a separate revision-guarded editorial action.
begin;
do $guard$
begin
 if md5(replace(pg_get_functiondef('public.validate_learning_problem(jsonb)'::regprocedure),E'\r\n',E'\n')) <> '24e3331a2ab999f8c05ec70d22414aa7' then raise exception '032: re-audit validate_learning_problem before applying'; end if;
 if md5(replace(pg_get_functiondef('public.admin_save_problem(jsonb,bigint,integer)'::regprocedure),E'\r\n',E'\n')) <> 'b1bc0a41e52ae72d486bac5a888e605d' then raise exception '032: re-audit admin_save_problem before applying'; end if;
 if md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure),E'\r\n',E'\n')) <> 'f214981e444e2f89f3fc4a79e841e890' then raise exception '032: re-audit validate_tutorial_body before applying'; end if;
end;
$guard$;
create or replace function public.validate_priority_metadata(p_body jsonb) returns void
language plpgsql immutable set search_path='' as $$
begin
 if p_body ? 'priorityLevel' and (jsonb_typeof(p_body->'priorityLevel') is distinct from 'string' or p_body->>'priorityLevel' not in ('low','medium','high')) then
  raise exception 'Priority must be low, medium or high.' using errcode='22023';
 end if;
 if p_body ? 'priorityReason' and (jsonb_typeof(p_body->'priorityReason') is distinct from 'string' or length(p_body->>'priorityReason')>1000) then
  raise exception 'Priority reason must be text up to 1000 characters.' using errcode='22023';
 end if;
end;
$$;
revoke all on function public.validate_priority_metadata(jsonb) from public,anon,authenticated;
CREATE OR REPLACE FUNCTION public.validate_learning_problem(p_body jsonb)
 RETURNS jsonb
 LANGUAGE plpgsql
 SET search_path TO ''
AS $function$
declare rate integer;tag jsonb;hints jsonb;h jsonb;field text;
begin
 perform public.validate_priority_metadata(p_body);
 if p_body is null or jsonb_typeof(p_body)<>'object' or pg_column_size(p_body)>65536 then raise exception 'Бодлогын өгөгдөл буруу эсвэл хэт том байна.'; end if;
 if nullif(btrim(p_body->>'title'),'') is null or length(p_body->>'title')>200 then raise exception 'Бодлогын нэр 1–200 тэмдэгт байна.'; end if;
 if jsonb_typeof(p_body->'source') is distinct from 'string' then raise exception 'Source нэр оруулна уу.'; end if;
 p_body:=jsonb_set(p_body,'{source}',to_jsonb(public.normalize_problem_source(p_body->>'source')));
 if lower(p_body->>'source')='codeforces' then p_body:=jsonb_set(p_body,'{source}','"Codeforces"'::jsonb); end if;
 if nullif(btrim(p_body->>'ref'),'') is null or length(p_body->>'ref')>80 then raise exception 'Эх бодлогын ID оруулна уу.'; end if;
 if not public.valid_task_url(p_body->>'url') then raise exception 'HTTPS бодлогын холбоос оруулна уу.'; end if;
 if coalesce(p_body->>'editorialUrl','')<>'' and not public.valid_task_url(p_body->>'editorialUrl') then raise exception 'Editorial HTTPS холбоос байх ёстой.'; end if;
 if p_body->>'ratingKind'='unrated' then
  if p_body->'rating' is distinct from 'null'::jsonb then raise exception 'Unrated rating null байна.'; end if;
 else
  if coalesce(p_body->>'rating','') !~ '^[0-9]{3,4}$' then raise exception 'Rating бүхэл тоо байна.'; end if;
  rate:=(p_body->>'rating')::integer;
  if rate not between 800 and 4000 then raise exception 'Rating 800–4000 хүрээнд байна.'; end if;
  if coalesce(p_body->>'ratingKind','') not in ('official','estimated') or (p_body->>'ratingKind'='official' and p_body->>'source'<>'Codeforces') then raise exception 'Rating-ийн төрөл буруу байна.'; end if;
 end if;
 if jsonb_typeof(p_body->'priority') is distinct from 'boolean' then raise exception 'Priority сонголт буруу байна.'; end if;
 if coalesce(p_body->>'level','Practice') not in ('Practice','Interactive') then raise exception 'Төрөл буруу байна.'; end if;
 if jsonb_typeof(p_body->'tags') is distinct from 'array' then raise exception 'Tags array шаардлагатай.'; end if;
 if jsonb_array_length(p_body->'tags') not between 1 and 20 then raise exception '1–20 tag оруулна уу.'; end if;
 for tag in select value from jsonb_array_elements(p_body->'tags') loop
  if jsonb_typeof(tag)<>'string' or (tag#>>'{}') !~ '^[a-zA-Z0-9 +/&()_-]{1,50}$' then raise exception 'English tag бүр 1–50 тэмдэгт байна.'; end if;
 end loop;
 for hints in select coalesce(p_body->'hints','[]'::jsonb) union all select coalesce(p_body->'hintsEn','[]'::jsonb) loop
  if jsonb_typeof(hints) is distinct from 'array' then raise exception 'Hints array шаардлагатай.'; end if;
  if jsonb_array_length(hints) not in (0,3) then raise exception 'Hint-гүй эсвэл хэл тус бүрд 3 hint байна.'; end if;
  for h in select value from jsonb_array_elements(hints) loop
   if jsonb_typeof(h)<>'string' or nullif(btrim(h#>>'{}'),'') is null or length(h#>>'{}')>3000 then raise exception 'Hint бүр 1–3000 тэмдэгт байна.'; end if;
  end loop;
 end loop;
 if jsonb_array_length(coalesce(p_body->'hints','[]'::jsonb))<>jsonb_array_length(coalesce(p_body->'hintsEn','[]'::jsonb)) then raise exception 'Хоёр хэлний hint-ийн тоо ижил байна.'; end if;
 if length(coalesce(p_body->>'lesson',''))>2000 then raise exception 'Тайлбар хэт урт байна.'; end if;
 foreach field in array array['sourceId','sourceCategory','verifiedAt','difficultyCategory','ratingBasis','ratingConfidence','ratingEstimatedAt'] loop
  if p_body ? field and (jsonb_typeof(p_body->field) is distinct from 'string' or length(p_body->>field)>500) then raise exception 'Metadata талбар буруу: %',field; end if;
 end loop;
 return p_body;
end;
$function$
;
CREATE OR REPLACE FUNCTION public.admin_save_problem(p_body jsonb, p_number bigint DEFAULT NULL::bigint, p_revision integer DEFAULT NULL::integer)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
declare current_row public.problem_catalog%rowtype;n bigint;task_id text;payload jsonb;pack text;rate integer;
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501'; end if;
 p_body:=public.validate_learning_problem(p_body);
 rate:=case when p_body->>'ratingKind'='unrated' then null else (p_body->>'rating')::integer end;
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 p_body:=jsonb_set(p_body,'{source}',to_jsonb(public.admin_add_source(p_body->>'source')));
 pack:=case when lower(p_body->>'source')='cses' then 'cses' when lower(p_body->>'source')='egoi' then 'egoi' when rate<=1100 then 'foundation' when rate<=1500 then 'core' when rate<=1800 then 'challenge' when rate<=2100 then 'stretch' else 'advanced' end;
 if p_number is null then
  n:=pg_catalog.nextval('public.problem_number_seq');
  task_id:=case when lower(p_body->>'source')='cses' and p_body->>'ref' ~ '^[0-9]+$' then 'cses-'||(p_body->>'ref') when lower(p_body->>'source')='atcoder' and p_body->>'ref' ~* '^dp_[a-z]$' then 'atcoder-'||lower(p_body->>'ref') else 'task-'||n::text end;
 else
  select * into current_row from public.problem_catalog where number=p_number for update;
  if current_row.problem_id is null then raise exception 'Бодлого олдсонгүй.'; end if;
  if current_row.revision is distinct from p_revision then raise exception 'REVISION_CONFLICT: дахин ачаалж засна уу.' using errcode='40001'; end if;
  n:=current_row.number;task_id:=current_row.problem_id;
 end if;
 payload:=jsonb_build_object('id',task_id,'number',n,'pack',pack,'title',btrim(p_body->>'title'),'source',p_body->>'source','ref',btrim(p_body->>'ref'),'url',p_body->>'url','rating',rate,'ratingKind',p_body->>'ratingKind','priority',(p_body->>'priority')::boolean,'level',coalesce(p_body->>'level','Practice'),'tags',p_body->'tags','hints',coalesce(p_body->'hints','[]'::jsonb),'hintsEn',coalesce(p_body->'hintsEn','[]'::jsonb),'lesson',coalesce(p_body->>'lesson',''));
 if coalesce(p_body->>'editorialUrl','')<>'' then payload:=payload||jsonb_build_object('editorialUrl',p_body->>'editorialUrl'); end if;
 payload:=payload||jsonb_strip_nulls(jsonb_build_object('sourceId',p_body->>'sourceId','sourceCategory',p_body->>'sourceCategory','verifiedAt',p_body->>'verifiedAt','difficultyCategory',p_body->>'difficultyCategory','ratingBasis',p_body->>'ratingBasis','ratingConfidence',p_body->>'ratingConfidence','ratingEstimatedAt',p_body->>'ratingEstimatedAt'));
 payload:=coalesce(current_row.body,'{}'::jsonb)||payload;
 payload:=payload||jsonb_build_object(
  'priorityLevel',coalesce(p_body->>'priorityLevel',current_row.body->>'priorityLevel',case when (p_body->>'priority')::boolean then 'high' else 'medium' end),
  'priorityReason',coalesce(p_body->>'priorityReason',current_row.body->>'priorityReason',''));
 payload:=jsonb_set(payload,'{priority}',to_jsonb(payload->>'priorityLevel'='high'));
 if p_number is null then insert into public.problem_catalog(problem_id,number,body) values(task_id,n,payload);
 else update public.problem_catalog set body=payload,revision=revision+1,updated_at=now() where problem_id=task_id;end if;
 insert into public.problem_changes(problem_id,actor_id,action,previous_body,next_body) values(task_id,auth.uid(),case when p_number is null then 'create' else 'edit' end,current_row.body,payload);
 return payload||jsonb_build_object('revision',coalesce(current_row.revision,0)+1,'archived',coalesce(current_row.archived,false));
end;
$function$
;
CREATE OR REPLACE FUNCTION public.validate_tutorial_body(p_id text, p_body jsonb)
 RETURNS void
 LANGUAGE plpgsql
 IMMUTABLE
 SET search_path TO ''
AS $function$
declare lang text; v jsonb; s jsonb; b jsonb; item jsonb; cell jsonb; row_value jsonb; typ text; cols integer; ord numeric;
begin
 perform public.validate_priority_metadata(p_body);
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
create index if not exists problem_catalog_priority_level_idx on public.problem_catalog ((body->>'priorityLevel')) where not archived;
create index if not exists tutorial_catalog_priority_level_idx on public.tutorial_catalog ((body->>'priorityLevel')) where published;
commit;
-- Verify: read function/index metadata; compare catalog hashes/counts and learner progress counts before/after.
-- Recovery: forward-fix the added metadata logic after audit; do not delete content or learner data.
