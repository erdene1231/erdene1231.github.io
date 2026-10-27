-- PROPOSAL ONLY. Requires reviewed032+033, fresh actual schema/ACL/Storage audit,
-- private recovery and separate approval. Never run this as an automatic queue.
begin;
do $$begin
 if to_regprocedure('public.get_problem_statement(text)') is not null or to_regclass('public.problem_statements') is not null then raise exception '034 already exists: re-audit, do not replay';end if;
 if to_regclass('public.problem_editorials') is null or to_regprocedure('public.get_problem_editorial(text)') is null then raise exception 'Reviewed033 prerequisite absent';end if;
 if exists(select 1 from public.problem_catalog where body ? 'statement' or body ? 'statementProvenance') then raise exception 'Audit unexpected inline legacy statements';end if;
 if md5(replace(pg_get_functiondef('public.admin_save_problem(jsonb,bigint,integer)'::regprocedure),E'\r\n',E'\n'))<>'82f77cdaf239bc231563eef3ce78f4e3'then raise exception '034 baseline drift: re-audit admin_save_problem';end if;
 if md5(replace(pg_get_functiondef('public.get_catalog()'::regprocedure),E'\r\n',E'\n'))<>'be41869b3d7d7239d67aceabacafd809'then raise exception '034 baseline drift: re-audit get_catalog';end if;
 if md5(replace(pg_get_functiondef('public.get_admin_catalog()'::regprocedure),E'\r\n',E'\n'))<>'322515001dce00881be622ecb99620a4'then raise exception '034 baseline drift: re-audit get_admin_catalog';end if;
 if md5(replace(pg_get_functiondef('public.can_read_tutorial_media(text)'::regprocedure),E'\r\n',E'\n'))<>'b29d3015ff2016cf1e4fcecf4e0fa381'then raise exception '034 baseline drift: re-audit can_read_tutorial_media';end if;
 if md5(replace(pg_get_functiondef('public.admin_import_learning_problems(jsonb,boolean)'::regprocedure),E'\r\n',E'\n'))<>'772bb1c000141510d805c12d97d49172'then raise exception '034 baseline drift: re-audit admin_import_learning_problems';end if;
 if md5(replace(pg_get_functiondef('public.admin_import_problems(jsonb)'::regprocedure),E'\r\n',E'\n'))<>'df2dccc4cd8665421c55e3d6e5b71d53'then raise exception '034 baseline drift: re-audit admin_import_problems';end if;
 if md5(replace(pg_get_functiondef('public.admin_archive_problem(bigint,integer,boolean)'::regprocedure),E'\r\n',E'\n'))<>'9fdebacc28f4d7767635d88ed1ea8e02'then raise exception '034 baseline drift: re-audit admin_archive_problem';end if;
end$$;
create table public.problem_statements(
 problem_id text primary key references public.problem_catalog(problem_id),body jsonb not null,provenance jsonb not null,
 revision integer not null check(revision>0),updated_at timestamptz not null default now(),updated_by uuid not null
);
create table public.problem_statement_changes(
 change_id bigserial primary key,problem_id text not null references public.problem_catalog(problem_id),
 actor_id uuid not null,problem_revision integer not null,previous_body jsonb,next_body jsonb,previous_provenance jsonb,next_provenance jsonb,created_at timestamptz not null default now()
);
alter table public.problem_statements enable row level security;
alter table public.problem_statement_changes enable row level security;
revoke all on public.problem_statements,public.problem_statement_changes from public,anon,authenticated;
revoke all on sequence public.problem_statement_changes_change_id_seq from public,anon,authenticated;

create function public.validate_problem_statement(doc jsonb,provenance jsonb) returns void language plpgsql set search_path='' as $$
declare version jsonb;section jsonb;field text;d date;mn_samples jsonb;en_samples jsonb;begin
 if doc is null or doc='null'::jsonb then
  if provenance is not null and provenance<>'null'::jsonb then raise exception 'Statement provenance without body' using errcode='22023';end if;
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
 -- Existing tutorial publication validator plus access/existence checks for media.
 perform public.validate_problem_editorial(doc);
end;$$;
revoke all on function public.validate_problem_statement(jsonb,jsonb)from public,anon,authenticated;

alter function public.admin_save_problem(jsonb,bigint,integer)rename to _admin_save_problem_033;
revoke all on function public._admin_save_problem_033(jsonb,bigint,integer)from public,anon,authenticated;
create function public.admin_save_problem(p_body jsonb,p_number bigint default null,p_revision integer default null)returns jsonb language plpgsql security definer set search_path='' as $$
declare old_doc public.problem_statements%rowtype;problem_id_value text;current_revision integer;doc jsonb;provenance jsonb;saved jsonb;begin
 if not public.is_admin()then raise exception 'Admin required' using errcode='42501';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 if p_number is not null then select problem_id,revision into problem_id_value,current_revision from public.problem_catalog where number=p_number for update;if problem_id_value is null then raise exception 'Problem not found'using errcode='22023';end if;if current_revision is distinct from p_revision then raise exception 'REVISION_CONFLICT'using errcode='40001';end if;select * into old_doc from public.problem_statements where problem_id=problem_id_value;end if;
 doc:=case when p_body?'statement'then nullif(p_body->'statement','null'::jsonb)else old_doc.body end;
 provenance:=case when p_body?'statementProvenance'then p_body->'statementProvenance'else old_doc.provenance end;
 if doc is null and provenance is not null then raise exception 'Statement provenance without body'using errcode='22023';end if;
 if p_number is null or doc is not null or old_doc.body is not null then perform public.validate_problem_statement(doc,provenance);end if;
 saved:=public._admin_save_problem_033(p_body-'statement'-'statementProvenance',p_number,p_revision);
 problem_id_value:=saved->>'id';
 if doc is distinct from old_doc.body or provenance is distinct from old_doc.provenance then
  insert into public.problem_statement_changes(problem_id,actor_id,problem_revision,previous_body,next_body,previous_provenance,next_provenance)values(problem_id_value,auth.uid(),(saved->>'revision')::integer,old_doc.body,doc,old_doc.provenance,provenance);
  insert into public.problem_statements(problem_id,body,provenance,revision,updated_by)values(problem_id_value,doc,provenance,1,auth.uid())on conflict(problem_id)do update set body=excluded.body,provenance=excluded.provenance,revision=public.problem_statements.revision+1,updated_at=now(),updated_by=auth.uid();
 end if;
 return saved||jsonb_build_object('hasStatement',doc is not null,'statement',doc,'statementProvenance',provenance);
end;$$;
revoke all on function public.admin_save_problem(jsonb,bigint,integer)from public,anon,authenticated;
grant execute on function public.admin_save_problem(jsonb,bigint,integer)to authenticated;

create function public.get_problem_statement(p_problem_id text)returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_build_object('body',s.body,'provenance',s.provenance,'revision',s.revision,'problemRevision',p.revision)from public.problem_statements s join public.problem_catalog p using(problem_id)where s.problem_id=p_problem_id and(not p.archived or public.is_admin());
$$;
alter function public.get_catalog()rename to _get_catalog_033;
alter function public.get_admin_catalog()rename to _get_admin_catalog_033;
revoke all on function public._get_catalog_033(),public._get_admin_catalog_033()from public,anon,authenticated;
create function public.get_catalog()returns jsonb language sql stable security definer set search_path='' as $$
 select jsonb_set(c,'{problems}',coalesce((select jsonb_agg(p||jsonb_build_object('hasStatement',exists(select 1 from public.problem_statements s where s.problem_id=p->>'id'))order by n)from jsonb_array_elements(c->'problems')with ordinality x(p,n)),'[]'::jsonb))from public._get_catalog_033()c;
$$;
create function public.get_admin_catalog()returns jsonb language plpgsql stable security definer set search_path='' as $$
begin if not public.is_admin()then raise exception 'Admin required'using errcode='42501';end if;return(select coalesce(jsonb_agg(p||jsonb_build_object('hasStatement',exists(select 1 from public.problem_statements s where s.problem_id=p->>'id'))order by n),'[]'::jsonb)from jsonb_array_elements(public._get_admin_catalog_033())with ordinality x(p,n));end;$$;
revoke all on function public.get_catalog(),public.get_admin_catalog(),public.get_problem_statement(text)from public,anon,authenticated;
grant execute on function public.get_catalog(),public.get_problem_statement(text)to anon,authenticated;
grant execute on function public.get_admin_catalog()to authenticated;

create function public.refresh_problem_statement_media()returns trigger language plpgsql security definer set search_path='' as $$
declare k text;begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if TG_TABLE_NAME='problem_statement_changes'then
  insert into public.tutorial_media_references(scope,scope_id,object_path)select'history','statement:'||new.change_id,path from public.tutorial_image_paths(jsonb_build_array(new.previous_body,new.next_body))on conflict do nothing;return new;
 end if;
 k:=case when TG_OP='DELETE'then old.problem_id else new.problem_id end;
 delete from public.tutorial_media_references where scope in('published','draft')and scope_id='statement:'||k;
 insert into public.tutorial_media_references(scope,scope_id,object_path)select case when p.archived then'draft'else'published'end,'statement:'||k,path from public.problem_statements s join public.problem_catalog p using(problem_id)cross join lateral public.tutorial_image_paths(s.body)paths where s.problem_id=k;
 if TG_OP='DELETE'then return old;end if;return new;
end;$$;
create trigger problem_statement_media_current after insert or update or delete on public.problem_statements for each row execute function public.refresh_problem_statement_media();
create trigger problem_statement_media_history after insert on public.problem_statement_changes for each row execute function public.refresh_problem_statement_media();
create trigger problem_statement_media_archive after update of archived on public.problem_catalog for each row execute function public.refresh_problem_statement_media();
create or replace function public.can_read_tutorial_media(p_path text)returns boolean language sql stable security definer set search_path='' as $$
 select(public.is_admin()and(split_part(p_path,'/',2)=auth.uid()::text or exists(select 1 from public.problem_editorials e cross join lateral public.tutorial_image_paths(e.body)paths where paths.path=p_path)or exists(select 1 from public.problem_statements s cross join lateral public.tutorial_image_paths(s.body)paths where paths.path=p_path)))or exists(select 1 from public.tutorial_media_references where scope='published'and object_path=p_path);
$$;
revoke all on function public.refresh_problem_statement_media()from public,anon,authenticated;
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
  elsif p_dry_run then perform public.validate_problem_statement(item->'statement',item->'statementProvenance');perform public.validate_new_problem_rating(item);perform public.validate_problem_content(item,null,nullif(item->'editorial','null'::jsonb));perform public.validate_problem_editorial(nullif(item->'editorial','null'::jsonb));result:=result||jsonb_build_array(jsonb_build_object('status','new','ref',item->>'ref','title',item->>'title'));
  else saved:=public.admin_save_problem(item);result:=result||jsonb_build_array(jsonb_build_object('status','created','id',saved->>'id','ref',item->>'ref'));end if;
 end loop;return result;
end;
$function$;

-- Recreate the unchanged bulk wrapper to invalidate any cached call plan bound
-- to the renamed033 helper; every path must resolve the guarded034 save.
CREATE OR REPLACE FUNCTION public.admin_import_problems(p_problems jsonb)
 RETURNS jsonb
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
declare task_body jsonb; result jsonb:='[]'::jsonb; saved jsonb; idx integer:=0;
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501'; end if;
 if p_problems is null or jsonb_typeof(p_problems)<>'array' then raise exception 'Бодлогын жагсаалт оруулна уу.'; end if;
 if jsonb_array_length(p_problems) not between 1 and 200 or pg_column_size(p_problems)>2097152 then raise exception 'Нэг удаад 1–200 бодлого, 2 MB хүртэл байна.'; end if;
 -- Entire batch is one transaction. Concurrent imports cannot bypass duplicate checks.
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 for task_body in select value from jsonb_array_elements(p_problems) loop
  idx:=idx+1;
  begin
   if exists(select 1 from public.problem_catalog p where p.body->>'url'=task_body->>'url' or (lower(p.body->>'source')=lower(public.normalize_problem_source(task_body->>'source')) and lower(btrim(p.body->>'ref'))=lower(btrim(task_body->>'ref')))) then
    raise exception 'Энэ бодлого санд байна (хассан бодлого ч багтана).';
   end if;
   saved:=public.admin_save_problem(task_body);
   result:=result||jsonb_build_array(saved);
  exception when others then raise exception 'Бодлого %: %',idx,sqlerrm;
  end;
 end loop;
 return result;
end;
$function$;

-- Serialize archive with save/import before row/media locks; preserve signature,
-- existing grants, server-admin checks and shared revision behavior.
CREATE OR REPLACE FUNCTION public.admin_archive_problem(p_number bigint, p_revision integer, p_archived boolean)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
declare r public.problem_catalog%rowtype; begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501'; end if;
 if p_archived is null then raise exception 'Үйлдлээ сонгоно уу.'; end if;
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 select * into r from public.problem_catalog where number=p_number for update;
 if r.problem_id is null then raise exception 'Бодлого олдсонгүй.'; end if;
 if r.revision is distinct from p_revision then raise exception 'Бодлого өөрчлөгдсөн байна. Дахин ачаална уу.' using errcode='40001'; end if;
 update public.problem_catalog set archived=p_archived,revision=revision+1,updated_at=now() where problem_id=r.problem_id;
 insert into public.problem_changes(problem_id,actor_id,action,previous_body,next_body) values(r.problem_id,auth.uid(),case when p_archived then 'archive' else 'restore' end,r.body,r.body);
end;
$function$;
commit;
