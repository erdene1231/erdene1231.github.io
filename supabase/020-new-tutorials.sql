-- Dependency: 008. Insert missing lessons; existing edits require matching revisions.
begin;
create or replace function public.admin_store_learning_tutorial(p_body jsonb,p_revision integer default 0) returns jsonb
language plpgsql security definer set search_path='' as $$
declare tid text:=p_body->>'id';current_row public.tutorial_catalog%rowtype;
begin
 if not public.is_admin() then raise exception 'Admin эрх шаардлагатай.' using errcode='42501';end if;
 perform public.validate_tutorial_body(tid,p_body);perform pg_catalog.pg_advisory_xact_lock(72483161);
 select * into current_row from public.tutorial_catalog where id=tid for update;
 if found then return public.admin_save_tutorial(tid,p_body,p_revision);end if;
 if p_revision<>0 then raise exception 'REVISION_CONFLICT: reload tutorial.' using errcode='40001';end if;
 insert into public.tutorial_catalog(id,body,revision,updated_by) values(tid,p_body,1,auth.uid());
 return jsonb_build_object('body',p_body,'revision',1);
end;
$$;
revoke all on function public.admin_store_learning_tutorial(jsonb,integer) from public,anon;
grant execute on function public.admin_store_learning_tutorial(jsonb,integer) to authenticated;
commit;
-- Verify: select to_regprocedure('public.admin_store_learning_tutorial(jsonb,integer)');
