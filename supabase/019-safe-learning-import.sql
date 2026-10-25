-- Dependency: 015. Admin-only, insert-only, batch 1–50; dry-run is the default.
begin;
create or replace function public.admin_import_learning_problems(p_problems jsonb,p_dry_run boolean default true) returns jsonb
language plpgsql security definer set search_path='' as $$
declare item jsonb;old public.problem_catalog%rowtype;saved jsonb;result jsonb:='[]'::jsonb;seen_urls text[]:='{}';seen_refs text[]:='{}';ref_key text;url_key text;
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501';end if;
 if jsonb_typeof(p_problems) is distinct from 'array' or jsonb_array_length(p_problems) not between 1 and 50 or pg_column_size(p_problems)>524288 then raise exception '1–50 бодлогын batch шаардлагатай.';end if;
 if p_dry_run is null then raise exception 'Dry run төлөв шаардлагатай.';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483160);
 for item in select value from jsonb_array_elements(p_problems) loop
  item:=public.validate_learning_problem(item);url_key:=rtrim(item->>'url','/');ref_key:=lower(item->>'source')||'|'||lower(btrim(item->>'ref'));
  if url_key=any(seen_urls) or ref_key=any(seen_refs) then result:=result||jsonb_build_array(jsonb_build_object('status','duplicate_batch','ref',item->>'ref'));continue;end if;
  seen_urls:=array_append(seen_urls,url_key);seen_refs:=array_append(seen_refs,ref_key);
  select * into old from public.problem_catalog p where rtrim(p.body->>'url','/')=url_key or (lower(p.body->>'source')=lower(item->>'source') and lower(btrim(p.body->>'ref'))=lower(btrim(item->>'ref'))) limit 1;
  if found then result:=result||jsonb_build_array(jsonb_build_object('status','exists','id',old.problem_id,'ref',item->>'ref','archived',old.archived));
  elsif p_dry_run then result:=result||jsonb_build_array(jsonb_build_object('status','new','ref',item->>'ref','title',item->>'title'));
  else saved:=public.admin_save_problem(item);result:=result||jsonb_build_array(jsonb_build_object('status','created','id',saved->>'id','ref',item->>'ref'));end if;
 end loop;return result;
end;
$$;
revoke all on function public.admin_import_learning_problems(jsonb,boolean) from public,anon;
grant execute on function public.admin_import_learning_problems(jsonb,boolean) to authenticated;
commit;
-- Verify: select to_regprocedure('public.admin_import_learning_problems(jsonb,boolean)');
