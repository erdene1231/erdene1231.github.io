-- Native statement persistence for the current AtCoder scope. No old proposal replay.
-- Existing problem table, RLS, RPC grants, CAS and edit history are retained.
BEGIN;
DO $guard$ BEGIN
IF to_regprocedure('public.validate_native_problem_statement(jsonb,jsonb)') IS NOT NULL THEN RAISE EXCEPTION 'Native statement helper exists; re-audit instead of replay'; END IF;
IF md5(replace(pg_get_functiondef('public.validate_learning_problem(jsonb)'::regprocedure),E'\r\n',E'\n')) <> '670d939c72ef36a1bb9153d536415383' THEN RAISE EXCEPTION 'Fresh baseline drift: validate_learning_problem'; END IF;
IF md5(replace(pg_get_functiondef('public.admin_save_problem(jsonb,bigint,integer)'::regprocedure),E'\r\n',E'\n')) <> 'dacc200a2a3c0db0c9911c1cd16964ae' THEN RAISE EXCEPTION 'Fresh baseline drift: admin_save_problem'; END IF;
IF md5(replace(pg_get_functiondef('public.get_catalog()'::regprocedure),E'\r\n',E'\n')) <> 'be41869b3d7d7239d67aceabacafd809' THEN RAISE EXCEPTION 'Fresh baseline drift: get_catalog'; END IF;
IF md5(replace(pg_get_functiondef('public.get_admin_catalog()'::regprocedure),E'\r\n',E'\n')) <> '322515001dce00881be622ecb99620a4' THEN RAISE EXCEPTION 'Fresh baseline drift: get_admin_catalog'; END IF;
END $guard$;
create function public.validate_native_problem_statement(doc jsonb,provenance jsonb) returns void language plpgsql set search_path='' as $$
declare version jsonb;section jsonb;field text;d date;mn_samples jsonb;en_samples jsonb;begin
 if doc is null or doc='null'::jsonb then
  if provenance is not null and provenance<>'null'::jsonb then raise exception 'NATIVE_STATEMENT_PROVENANCE_WITHOUT_BODY' using errcode='22023';end if;
  return;
 end if;
 if jsonb_typeof(provenance)is distinct from 'object' or pg_column_size(provenance)>16384 then raise exception 'Statement provenance required, at most16KB'using errcode='22023';end if;
 perform public.validate_tutorial_publication(doc->>'id',doc);
 foreach field in array array['mn','en'] loop
  version:=case when field='mn' then doc else doc#>'{translations,en}' end;
  if nullif(btrim(version->>'title'),'') is null or coalesce(jsonb_array_length(version->'sections'),0)<5 then raise exception 'Both statement languages require task/input/output/constraints/samples' using errcode='22023';end if;
  for section in select s from jsonb_array_elements(version->'sections')with ordinality x(s,n)where n<=5 loop
   if not exists(select 1 from jsonb_array_elements(section->'blocks') b where
    (b->>'type' in ('p','code')and nullif(btrim(b->>'text'),'')is not null)or
    (b->>'type'='rich'and exists(select 1 from jsonb_array_elements(b->'content')i where nullif(btrim(i->>'text'),'')is not null))or
    (b->>'type'='math'and nullif(btrim(b->>'tex'),'')is not null)or b->>'type' in ('list','ordered','table'))then raise exception 'Empty statement section' using errcode='22023';end if;
  end loop;
 end loop;
 select jsonb_agg(b->'text' order by n)into mn_samples from jsonb_array_elements(doc#>'{sections,4,blocks}')with ordinality x(b,n)where b->>'type'='code';
 select jsonb_agg(b->'text' order by n)into en_samples from jsonb_array_elements(doc#>'{translations,en,sections,4,blocks}')with ordinality x(b,n)where b->>'type'='code';
 if coalesce(jsonb_array_length(mn_samples),0)<2 or jsonb_array_length(mn_samples)%2<>0 or mn_samples is distinct from en_samples then raise exception 'Literal sample input/output pairs must match across languages' using errcode='22023';end if;
 if not coalesce(public.valid_task_url(provenance->>'sourceUrl'),false) or length(provenance->>'sourceUrl')>1000 or coalesce(provenance->>'sourceSha256','')!~'^[a-f0-9]{64}$' then raise exception 'Source HTTPS/hash required' using errcode='22023';end if;
 if coalesce(provenance->>'rightsBasis','') not in ('original-functional-restatement','licensed','public-domain')then raise exception 'Supported rights basis required' using errcode='22023';end if;
 if provenance->>'rightsBasis'in('licensed','public-domain')and not coalesce(public.valid_task_url(provenance->>'rightsReference'),false)then raise exception 'License/permission reference required' using errcode='22023';end if;
 foreach field in array array['task','input','output','constraints','samples','translation','rights']loop
  if provenance#>array['checks',field]is distinct from 'true'::jsonb then raise exception 'Statement review incomplete: %',field using errcode='22023';end if;
 end loop;
 if coalesce(provenance->>'reviewedAt','')!~'^\d{4}-\d{2}-\d{2}$'then raise exception 'Review date required' using errcode='22023';end if;
 begin d:=(provenance->>'reviewedAt')::date;exception when others then raise exception 'Review date invalid' using errcode='22023';end;
 if to_char(d,'YYYY-MM-DD')<>provenance->>'reviewedAt'then raise exception 'Review date invalid' using errcode='22023';end if;
 -- Inline documents use text, MathJax and the existing typed native blocks.
 -- Images need separate reference lifecycle support and are deliberately rejected.
 if jsonb_path_exists(doc,'$.** ? (@.type == "image")') then raise exception 'Inline statement image references are not supported' using errcode='22023';end if;
end;$$;
revoke all on function public.validate_native_problem_statement(jsonb,jsonb)from public,anon,authenticated;

CREATE OR REPLACE FUNCTION public.validate_learning_problem(p_body jsonb)
 RETURNS jsonb
 LANGUAGE plpgsql
 SET search_path TO ''
AS $function$
declare rate integer;tag jsonb;hints jsonb;h jsonb;field text;
begin
 if p_body ? 'statement' or p_body ? 'statementProvenance' then perform public.validate_native_problem_statement(nullif(p_body->'statement','null'::jsonb),nullif(p_body->'statementProvenance','null'::jsonb));end if;
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
 payload:=payload||jsonb_strip_nulls(jsonb_build_object('sourceId',p_body->>'sourceId','sourceCategory',p_body->>'sourceCategory','verifiedAt',p_body->>'verifiedAt','difficultyCategory',p_body->>'difficultyCategory','ratingBasis',p_body->>'ratingBasis','ratingConfidence',p_body->>'ratingConfidence','ratingEstimatedAt',p_body->>'ratingEstimatedAt','ratingSource',p_body->>'ratingSource','ratingVerifiedAt',p_body->>'ratingVerifiedAt','sourceTags',p_body->'sourceTags'));
 payload:=coalesce(current_row.body,'{}'::jsonb)||payload;
 payload:=payload||jsonb_build_object(
  'priorityLevel',coalesce(p_body->>'priorityLevel',current_row.body->>'priorityLevel',case when (p_body->>'priority')::boolean then 'high' else 'medium' end),
  'priorityReason',coalesce(p_body->>'priorityReason',current_row.body->>'priorityReason',''));
 payload:=jsonb_set(payload,'{priority}',to_jsonb(payload->>'priorityLevel'='high'));
 if p_body ? 'statement' then
  if p_body->'statement'='null'::jsonb then payload:=payload-ARRAY['statement','statementProvenance'];
  else payload:=payload||jsonb_build_object('statement',p_body->'statement','statementProvenance',p_body->'statementProvenance');end if;
 end if;
 if p_number is null then insert into public.problem_catalog(problem_id,number,body) values(task_id,n,payload);
 else update public.problem_catalog set body=payload,revision=revision+1,updated_at=now() where problem_id=task_id;end if;
 insert into public.problem_changes(problem_id,actor_id,action,previous_body,next_body) values(task_id,auth.uid(),case when p_number is null then 'create' else 'edit' end,current_row.body,payload);
 return payload||jsonb_build_object('revision',coalesce(current_row.revision,0)+1,'archived',coalesce(current_row.archived,false));
end;
$function$
;
CREATE OR REPLACE FUNCTION public.get_catalog()
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO ''
AS $function$
 select jsonb_build_object(
 'problems',coalesce((select jsonb_agg((pc.body-ARRAY['statement','statementProvenance'])||jsonb_build_object('hasStatement',pc.body?'statement','id',pc.problem_id,'number',pc.number,'revision',pc.revision) order by pc.number) from public.problem_catalog pc where not pc.archived and pc.body is not null),'[]'::jsonb),
 'knownIds',coalesce((select jsonb_agg(problem_id) from public.problem_catalog),'[]'::jsonb),
 'sources',coalesce((select jsonb_agg(name order by lower(name)) from public.problem_sources),'[]'::jsonb));
$function$
;
CREATE OR REPLACE FUNCTION public.get_admin_catalog()
 RETURNS jsonb
 LANGUAGE plpgsql
 STABLE SECURITY DEFINER
 SET search_path TO ''
AS $function$
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501'; end if;
 return coalesce((select jsonb_agg((pc.body-ARRAY['statement','statementProvenance'])||jsonb_build_object('hasStatement',pc.body?'statement','id',pc.problem_id,'number',pc.number,'revision',pc.revision,'archived',pc.archived) order by pc.number) from public.problem_catalog pc where pc.body is not null),'[]'::jsonb);
end;
$function$
;
COMMIT;
