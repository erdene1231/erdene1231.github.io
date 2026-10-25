-- Dependency: 007. Validation/provenance and stable IDs for NEW CSES/AtCoder tasks.
-- Existing records, IDs and progress are never rewritten by this migration.
begin;
create or replace function public.validate_learning_problem(p_body jsonb) returns jsonb
language plpgsql set search_path='' as $$
declare rate integer;tag jsonb;hints jsonb;h jsonb;field text;
begin
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
$$;
revoke all on function public.validate_learning_problem(jsonb) from public,anon,authenticated;

create or replace function public.admin_save_problem(p_body jsonb,p_number bigint default null,p_revision integer default null) returns jsonb
language plpgsql security definer set search_path='' as $$
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
 if p_number is null then insert into public.problem_catalog(problem_id,number,body) values(task_id,n,payload);
 else update public.problem_catalog set body=payload,revision=revision+1,updated_at=now() where problem_id=task_id;end if;
 insert into public.problem_changes(problem_id,actor_id,action,previous_body,next_body) values(task_id,auth.uid(),case when p_number is null then 'create' else 'edit' end,current_row.body,payload);
 return payload||jsonb_build_object('revision',coalesce(current_row.revision,0)+1,'archived',coalesce(current_row.archived,false));
end;
$$;
revoke all on function public.admin_save_problem(jsonb,bigint,integer) from public,anon;
grant execute on function public.admin_save_problem(jsonb,bigint,integer) to authenticated;
commit;
-- Verify: select to_regprocedure('public.validate_learning_problem(jsonb)');
