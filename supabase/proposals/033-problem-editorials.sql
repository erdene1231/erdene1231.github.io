-- PROPOSAL ONLY: no production application authorized. Requires reviewed032, fresh actual-schema audit and explicit approval.
-- Separate rich bodies keep get_catalog/get_admin_catalog small; no existing data backfill or fake tutorial rows.
begin;
do $guard$ begin
 if to_regprocedure('public.get_problem_editorial(text)') is not null or to_regclass('public.problem_editorials') is not null or to_regclass('public.problem_editorial_changes') is not null then raise exception '033 already exists: re-audit; do not replay';end if;
 if exists(select 1 from public.problem_catalog where body ? 'editorial') then raise exception 'Audit unexpected inline legacy editorials before applying';end if;
 if md5(replace(pg_get_functiondef('public.admin_save_problem(jsonb,bigint,integer)'::regprocedure),E'\r\n',E'\n'))<>'dacc200a2a3c0db0c9911c1cd16964ae' then raise exception '033 proposal baseline drift: re-audit admin_save_problem';end if;
 if md5(replace(pg_get_functiondef('public.can_read_tutorial_media(text)'::regprocedure),E'\r\n',E'\n'))<>'673def2324a65296757fe50a7cc6ecbd' then raise exception '033 proposal baseline drift: re-audit can_read_tutorial_media';end if;
 if md5(replace(pg_get_functiondef('public.tutorial_image_paths(jsonb)'::regprocedure),E'\r\n',E'\n'))<>'13229ff417ffa875b7d2ab159625c1e4' then raise exception '033 proposal baseline drift: re-audit tutorial_image_paths';end if;
 if md5(replace(pg_get_functiondef('public.validate_learning_problem(jsonb)'::regprocedure),E'\r\n',E'\n'))<>'670d939c72ef36a1bb9153d536415383' then raise exception '033 proposal baseline drift: re-audit validate_learning_problem';end if;
 if md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure),E'\r\n',E'\n'))<>'316fd2e8b20a336b4272421a9e048a62' then raise exception '033 proposal baseline drift: re-audit validate_tutorial_body';end if;
 if md5(replace(pg_get_functiondef('public.validate_tutorial_publication(text,jsonb)'::regprocedure),E'\r\n',E'\n'))<>'75ad9bcd99bfdb63a0fb533b5e9468f7' then raise exception '033 proposal baseline drift: re-audit validate_tutorial_publication';end if;
 if md5(replace(pg_get_functiondef('public.admin_import_learning_problems(jsonb,boolean)'::regprocedure),E'\r\n',E'\n'))<>'bce5f398f05f471a20cfc1ee2ed2d1c6' then raise exception '033 proposal baseline drift: re-audit admin_import_learning_problems';end if;
end;$guard$;
create table public.problem_editorials(
 problem_id text primary key references public.problem_catalog(problem_id),body jsonb not null,
 revision integer not null check(revision>0),updated_at timestamptz not null default now(),updated_by uuid not null
);
create table public.problem_editorial_changes(
 change_id bigserial primary key,problem_id text not null references public.problem_catalog(problem_id),
 actor_id uuid not null,problem_revision integer not null,previous_body jsonb,next_body jsonb,created_at timestamptz not null default now()
);
alter table public.problem_editorials enable row level security;
alter table public.problem_editorial_changes enable row level security;
revoke all on public.problem_editorials,public.problem_editorial_changes from public,anon,authenticated;
revoke all on sequence public.problem_editorial_changes_change_id_seq from public,anon,authenticated;

create function public.canonical_problem_url(p_url text) returns text language plpgsql immutable set search_path='' as $$
declare u text[];p text[];begin
 u:=regexp_match(p_url,'^(https://[^/]+)(/[^?#]*)([?#].*)?$');
 if u is null or lower(u[1]) not in ('https://codeforces.com','https://www.codeforces.com','https://codeforces.com:443','https://www.codeforces.com:443') then return p_url;end if;
 p:=regexp_match(u[2],'^/(?:problemset/problem/([0-9]+)/([A-Za-z][A-Za-z0-9]*)|contest/([0-9]+)/problem/([A-Za-z][A-Za-z0-9]*))/?$');
 if p is null then return p_url;end if;
 return 'https://codeforces.com/contest/'||coalesce(p[1],p[3])||'/problem/'||coalesce(p[2],p[4])||coalesce(u[3],'');
end;$$;
create function public.problem_url_identity(p_url text) returns text language plpgsql immutable set search_path='' as $$
declare c text:=public.canonical_problem_url(p_url);begin
 if c ~ '^https://codeforces[.]com/contest/[0-9]+/problem/[A-Za-z][A-Za-z0-9]*([?#].*)?$' then return regexp_replace(c,'[?#].*$','');end if;return c;
end;$$;
revoke all on function public.canonical_problem_url(text),public.problem_url_identity(text) from public,anon,authenticated;

create function public.validate_new_problem_rating(p jsonb) returns void language plpgsql set search_path='' as $$
declare d text;parsed date;begin
 if p->>'ratingKind' not in ('official','estimated') or coalesce(p->>'rating','') !~ '^[0-9]{3,4}$' or (p->>'rating')::integer not between 800 and 4000 then raise exception 'Every new problem must be rated.' using errcode='22023';end if;
 if nullif(btrim(p->>'ratingBasis'),'') is null or coalesce(p->>'ratingSource','') !~* '^https://[^/@[:space:]:]+(:[0-9]+)?([/?#][^[:space:]]*)?$' then raise exception 'Rating source and calibration rationale required.' using errcode='22023';end if;
 if p->>'ratingKind'='official' and (p->>'source'<>'Codeforces' or p->>'ratingSource' !~* '^https://codeforces[.]com([/?#]|$)') then raise exception 'Only verified Codeforces ratings are official.' using errcode='22023';end if;
 if p->>'ratingKind'='estimated' and ((p->>'rating')::integer%100<>0 or nullif(btrim(p->>'ratingConfidence'),'') is null) then raise exception 'Estimate needs100-point calibration and confidence.' using errcode='22023';end if;
 d:=case when p->>'ratingKind'='official' then p->>'ratingVerifiedAt' else p->>'ratingEstimatedAt' end;
 if coalesce(d,'') !~ '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' then raise exception 'Rating verification date required.' using errcode='22023';end if;
 begin parsed:=d::date;exception when others then raise exception 'Invalid rating date.' using errcode='22023';end;
 if to_char(parsed,'YYYY-MM-DD')<>d then raise exception 'Invalid rating date.' using errcode='22023';end if;
end;$$;

create function public.validate_problem_content(p jsonb,old_body jsonb,ed jsonb) returns void language plpgsql set search_path='' as $$
declare lvl text;substantive boolean;begin
 lvl:=coalesce(p->>'priorityLevel',old_body->>'priorityLevel',case when (p->>'priority')::boolean then 'high' else 'medium' end);
 if lvl='low' and (jsonb_array_length(coalesce(p->'hints','[]'))>0 or jsonb_array_length(coalesce(p->'hintsEn','[]'))>0) and
  (old_body is null or coalesce(p->'hints','[]') is distinct from coalesce(old_body->'hints','[]') or coalesce(p->'hintsEn','[]') is distinct from coalesce(old_body->'hintsEn','[]')) then raise exception 'Low offers no new hints; retain existing stored hints unchanged.' using errcode='22023';end if;
 if ed is not null and ed<>'null'::jsonb then
  select exists(select 1 from jsonb_path_query(ed,'$.sections[*].blocks[*]') x(b) where
   (b->>'type' in ('p','code') and nullif(btrim(b->>'text'),'') is not null) or
   (b->>'type'='math' and nullif(btrim(b->>'tex'),'') is not null) or
   (b->>'type'='rich' and exists(select 1 from jsonb_array_elements(b->'content') r where nullif(btrim(r->>'text'),'') is not null))) into substantive;
  if not substantive then raise exception 'High editorial needs substantive typed content.' using errcode='22023';end if;
 end if;
end;$$;
CREATE OR REPLACE FUNCTION public.validate_learning_problem(p_body jsonb)
 RETURNS jsonb
 LANGUAGE plpgsql
 SET search_path TO ''
AS $function$
declare rate integer;tag jsonb;hints jsonb;h jsonb;field text;
begin
 perform public.validate_priority_metadata(p_body);
 if p_body is null or jsonb_typeof(p_body)<>'object' or pg_column_size(p_body-'editorial')>65536 or length(p_body::text)>1100000 then raise exception 'Бодлогын өгөгдөл буруу эсвэл хэт том байна.'; end if;
 if nullif(btrim(p_body->>'title'),'') is null or length(p_body->>'title')>200 then raise exception 'Бодлогын нэр 1–200 тэмдэгт байна.'; end if;
 if jsonb_typeof(p_body->'source') is distinct from 'string' then raise exception 'Source нэр оруулна уу.'; end if;
 p_body:=jsonb_set(p_body,'{source}',to_jsonb(public.normalize_problem_source(p_body->>'source')));
 if lower(p_body->>'source')='codeforces' then p_body:=jsonb_set(p_body,'{source}','"Codeforces"'::jsonb); end if;
 if nullif(btrim(p_body->>'ref'),'') is null or length(p_body->>'ref')>80 then raise exception 'Эх бодлогын ID оруулна уу.'; end if;
 p_body:=jsonb_set(p_body,'{url}',coalesce(to_jsonb(public.canonical_problem_url(p_body->>'url')),'null'::jsonb));
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
 if p_body ? 'ratingSource' and not public.valid_task_url(p_body->>'ratingSource') then raise exception 'Rating source HTTPS URL шаардлагатай.'; end if;
 if p_body ? 'sourceTags' then
  if jsonb_typeof(p_body->'sourceTags') is distinct from 'array' then raise exception 'Source tags array шаардлагатай.'; end if;
  if jsonb_array_length(p_body->'sourceTags')>20 then raise exception 'Source tags хэт олон байна.'; end if;
  for tag in select value from jsonb_array_elements(p_body->'sourceTags') loop
   if jsonb_typeof(tag)<>'string' or (tag#>>'{}') !~ '^[a-zA-Z0-9 +/&()_*-]{1,50}$' then raise exception 'Source tag буруу байна.'; end if;
  end loop;
 end if;
 foreach field in array array['sourceId','sourceCategory','verifiedAt','difficultyCategory','ratingBasis','ratingConfidence','ratingEstimatedAt','ratingSource','ratingVerifiedAt'] loop
  if p_body ? field and (jsonb_typeof(p_body->field) is distinct from 'string' or length(p_body->>field)>500) then raise exception 'Metadata талбар буруу: %',field; end if;
 end loop;
 if p_body ? 'editorial' and p_body->'editorial'<>'null'::jsonb then perform public.validate_tutorial_body(p_body#>>'{editorial,id}',p_body->'editorial');end if;
 return p_body;
end;
$function$
;
create function public.validate_problem_editorial(ed jsonb) returns void language plpgsql set search_path='' as $$
declare image_path text;begin
 if ed is not null then
  perform public.validate_tutorial_publication(ed->>'id',ed);
  for image_path in select path from public.tutorial_image_paths(ed) loop
   if not public.can_read_tutorial_media(image_path) then raise exception 'Editorial image is not accessible.' using errcode='42501';end if;
   if not exists(select 1 from storage.objects where bucket_id='tutorial-media' and name=image_path) then raise exception 'Editorial image missing from Storage.' using errcode='22023';end if;
  end loop;
 end if;
end;$$;
revoke all on function public.validate_problem_editorial(jsonb) from public,anon,authenticated;

CREATE OR REPLACE FUNCTION public.admin_save_problem(p_body jsonb, p_number bigint DEFAULT NULL::bigint, p_revision integer DEFAULT NULL::integer)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
declare current_row public.problem_catalog%rowtype;n bigint;task_id text;payload jsonb;pack text;rate integer;ed jsonb;old_ed jsonb;image_path text;
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501'; end if;
 p_body:=public.validate_learning_problem(p_body);
 rate:=case when p_body->>'ratingKind'='unrated' then null else (p_body->>'rating')::integer end;
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 p_body:=jsonb_set(p_body,'{source}',to_jsonb(public.admin_add_source(p_body->>'source')));
 pack:=case when lower(p_body->>'source')='cses' then 'cses' when lower(p_body->>'source')='egoi' then 'egoi' when rate<=1100 then 'foundation' when rate<=1500 then 'core' when rate<=1800 then 'challenge' when rate<=2100 then 'stretch' else 'advanced' end;
 if p_number is null then
  perform public.validate_new_problem_rating(p_body);
  n:=pg_catalog.nextval('public.problem_number_seq');
  task_id:=case when lower(p_body->>'source')='cses' and p_body->>'ref' ~ '^[0-9]+$' then 'cses-'||(p_body->>'ref') when lower(p_body->>'source')='atcoder' and p_body->>'ref' ~* '^dp_[a-z]$' then 'atcoder-'||lower(p_body->>'ref') else 'task-'||n::text end;
 else
  select * into current_row from public.problem_catalog where number=p_number for update;
  if current_row.problem_id is null then raise exception 'Бодлого олдсонгүй.'; end if;
  if current_row.revision is distinct from p_revision then raise exception 'REVISION_CONFLICT: дахин ачаалж засна уу.' using errcode='40001'; end if;
  n:=current_row.number;task_id:=current_row.problem_id;
 end if;
 if exists(select 1 from public.problem_catalog p where p.problem_id is distinct from task_id and (public.problem_url_identity(p.body->>'url')=public.problem_url_identity(p_body->>'url') or (lower(p.body->>'source')=lower(p_body->>'source') and lower(btrim(p.body->>'ref'))=lower(btrim(p_body->>'ref'))))) then raise exception 'Duplicate problem identity (including archived records).' using errcode='23505';end if;
 select body into old_ed from public.problem_editorials where problem_id=task_id;
 ed:=case when p_body ? 'editorial' then nullif(p_body->'editorial','null'::jsonb) else old_ed end;
 perform public.validate_problem_content(p_body,current_row.body,ed);
 perform public.validate_problem_editorial(ed);
 payload:=jsonb_build_object('id',task_id,'number',n,'pack',pack,'title',btrim(p_body->>'title'),'source',p_body->>'source','ref',btrim(p_body->>'ref'),'url',p_body->>'url','rating',rate,'ratingKind',p_body->>'ratingKind','priority',(p_body->>'priority')::boolean,'level',coalesce(p_body->>'level','Practice'),'tags',p_body->'tags','hints',coalesce(p_body->'hints','[]'::jsonb),'hintsEn',coalesce(p_body->'hintsEn','[]'::jsonb),'lesson',coalesce(p_body->>'lesson',''));
 if coalesce(p_body->>'editorialUrl','')<>'' then payload:=payload||jsonb_build_object('editorialUrl',p_body->>'editorialUrl'); end if;
 payload:=payload||jsonb_strip_nulls(jsonb_build_object('sourceId',p_body->>'sourceId','sourceCategory',p_body->>'sourceCategory','verifiedAt',p_body->>'verifiedAt','difficultyCategory',p_body->>'difficultyCategory','ratingBasis',p_body->>'ratingBasis','ratingConfidence',p_body->>'ratingConfidence','ratingEstimatedAt',p_body->>'ratingEstimatedAt','ratingSource',p_body->>'ratingSource','ratingVerifiedAt',p_body->>'ratingVerifiedAt','sourceTags',p_body->'sourceTags'));
 payload:=(coalesce(current_row.body,'{}'::jsonb)-'editorial')||payload||jsonb_build_object('hasEditorial',ed is not null);
 payload:=payload||jsonb_build_object(
  'priorityLevel',coalesce(p_body->>'priorityLevel',current_row.body->>'priorityLevel',case when (p_body->>'priority')::boolean then 'high' else 'medium' end),
  'priorityReason',coalesce(p_body->>'priorityReason',current_row.body->>'priorityReason',''));
 payload:=jsonb_set(payload,'{priority}',to_jsonb(payload->>'priorityLevel'='high'));
 if p_number is null then insert into public.problem_catalog(problem_id,number,body) values(task_id,n,payload);
 else update public.problem_catalog set body=payload,revision=revision+1,updated_at=now() where problem_id=task_id;end if;
 insert into public.problem_changes(problem_id,actor_id,action,previous_body,next_body) values(task_id,auth.uid(),case when p_number is null then 'create' else 'edit' end,current_row.body,payload);
 if ed is distinct from old_ed then
  insert into public.problem_editorial_changes(problem_id,actor_id,problem_revision,previous_body,next_body) values(task_id,auth.uid(),coalesce(current_row.revision,0)+1,old_ed,ed);
  if ed is null then delete from public.problem_editorials where problem_id=task_id;
  else insert into public.problem_editorials(problem_id,body,revision,updated_by) values(task_id,ed,1,auth.uid()) on conflict(problem_id) do update set body=excluded.body,revision=public.problem_editorials.revision+1,updated_at=now(),updated_by=auth.uid();end if;
 end if;
 return payload||jsonb_build_object('editorial',ed)||jsonb_build_object('revision',coalesce(current_row.revision,0)+1,'archived',coalesce(current_row.archived,false));
end;
$function$
;

CREATE OR REPLACE FUNCTION public.admin_import_learning_problems(p_problems jsonb, p_dry_run boolean DEFAULT true)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
declare item jsonb;old public.problem_catalog%rowtype;saved jsonb;result jsonb:='[]'::jsonb;seen_urls text[]:='{}';seen_refs text[]:='{}';ref_key text;url_key text;
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501';end if;
 if jsonb_typeof(p_problems) is distinct from 'array' or jsonb_array_length(p_problems) not between 1 and 50 or pg_column_size(p_problems)>524288 then raise exception '1–50 бодлогын batch шаардлагатай.';end if;
 if p_dry_run is null then raise exception 'Dry run төлөв шаардлагатай.';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 for item in select value from jsonb_array_elements(p_problems) loop
  item:=public.validate_learning_problem(item);url_key:=public.problem_url_identity(item->>'url');ref_key:=lower(item->>'source')||'|'||lower(btrim(item->>'ref'));
  if url_key=any(seen_urls) or ref_key=any(seen_refs) then result:=result||jsonb_build_array(jsonb_build_object('status','duplicate_batch','ref',item->>'ref'));continue;end if;
  seen_urls:=array_append(seen_urls,url_key);seen_refs:=array_append(seen_refs,ref_key);
  select * into old from public.problem_catalog p where public.problem_url_identity(p.body->>'url')=url_key or (lower(p.body->>'source')=lower(item->>'source') and lower(btrim(p.body->>'ref'))=lower(btrim(item->>'ref'))) limit 1;
  if found then result:=result||jsonb_build_array(jsonb_build_object('status','exists','id',old.problem_id,'ref',item->>'ref','archived',old.archived));
  elsif p_dry_run then perform public.validate_new_problem_rating(item);perform public.validate_problem_content(item,null,nullif(item->'editorial','null'::jsonb));perform public.validate_problem_editorial(nullif(item->'editorial','null'::jsonb));result:=result||jsonb_build_array(jsonb_build_object('status','new','ref',item->>'ref','title',item->>'title'));
  else saved:=public.admin_save_problem(item);result:=result||jsonb_build_array(jsonb_build_object('status','created','id',saved->>'id','ref',item->>'ref'));end if;
 end loop;return result;
end;
$function$;

create function public.get_problem_editorial(p_problem_id text) returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_build_object('body',e.body,'revision',e.revision,'problemRevision',p.revision)
 from public.problem_editorials e join public.problem_catalog p using(problem_id)
 where e.problem_id=p_problem_id and p.body is not null and (not p.archived or public.is_admin());
$$;

-- Existing scope values remain unchanged. Prefixes cannot collide with tutorial IDs/change IDs.
create function public.refresh_problem_editorial_media() returns trigger language plpgsql security definer set search_path='' as $$
declare k text;h text;begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if TG_TABLE_NAME='problem_editorial_changes' then
  insert into public.tutorial_media_references(scope,scope_id,object_path) select 'history','problem:'||new.change_id,path from public.tutorial_image_paths(jsonb_build_array(new.previous_body,new.next_body)) on conflict do nothing;return new;
 end if;
 k:=case when TG_OP='DELETE' then old.problem_id else new.problem_id end;
 h:='problem:'||k;
 delete from public.tutorial_media_references where scope in ('published','draft') and scope_id=h;
 insert into public.tutorial_media_references(scope,scope_id,object_path)
 select case when p.archived then 'draft' else 'published' end,h,paths.path from public.problem_editorials e join public.problem_catalog p using(problem_id) cross join lateral public.tutorial_image_paths(e.body) paths where e.problem_id=k;
 if TG_OP='DELETE' then return old;end if;return new;
end;$$;
create trigger problem_editorial_media_current after insert or update or delete on public.problem_editorials for each row execute function public.refresh_problem_editorial_media();
create trigger problem_editorial_media_history after insert on public.problem_editorial_changes for each row execute function public.refresh_problem_editorial_media();
create trigger problem_editorial_media_archive after update of archived on public.problem_catalog for each row execute function public.refresh_problem_editorial_media();

create or replace function public.can_read_tutorial_media(p_path text) returns boolean language sql stable security definer set search_path='' as $$
 select (public.is_admin() and (split_part(p_path,'/',2)=auth.uid()::text or exists(select 1 from public.problem_editorials e cross join lateral public.tutorial_image_paths(e.body) paths where paths.path=p_path)))
 or exists(select 1 from public.tutorial_media_references where scope='published' and object_path=p_path);
$$;
revoke all on function public.validate_new_problem_rating(jsonb),public.validate_problem_content(jsonb,jsonb,jsonb),public.refresh_problem_editorial_media(),public.get_problem_editorial(text) from public,anon,authenticated;
grant execute on function public.get_problem_editorial(text) to anon,authenticated;
-- Existing admin_save/import RPC grants and server-admin checks remain unchanged.
commit;
-- Before application: actual schema/function/ACL/Storage policy audit, private recovery and explicit approval.
-- No catalog/tutorial/progress backfill.033 does not authorize deployment or application of032.
