-- Delete only the acting editor's private, never-published draft. No installation DML.
begin;
DO $baseline$
BEGIN
 IF to_regclass('public.tutorial_deleted_ids') IS NULL OR to_regprocedure('public.admin_delete_tutorial(text,integer,text,uuid)') IS NULL
 OR to_regprocedure('public.admin_delete_tutorial_draft(text,integer,text,uuid)') IS NOT NULL THEN
  RAISE EXCEPTION '030 baseline missing, changed or already applied; re-audit instead of replaying';
 END IF;
 IF md5(replace(pg_get_functiondef('public.admin_save_tutorial_draft(text,jsonb,integer,integer,uuid)'::regprocedure),E'\r\n',E'\n'))<>'55d7fa5a2b24bcb99554f61cc01e8768' THEN RAISE EXCEPTION '030 baseline changed; re-audit';END IF;
 IF md5(replace(pg_get_functiondef('public.admin_delete_tutorial(text,integer,text,uuid)'::regprocedure),E'\r\n',E'\n'))<>'b09ce531a47ae2df7721c43e3bfbba82' THEN RAISE EXCEPTION '030 baseline changed; re-audit';END IF;
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure),E'\r\n',E'\n'))<>'d17381308438362f364065137f8ad1a2' THEN RAISE EXCEPTION '030 baseline changed; re-audit';END IF;
END;
$baseline$;
create function public.admin_delete_tutorial_draft(p_id text,p_draft_revision integer,p_confirmation text,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare d public.tutorial_drafts%rowtype;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 if p_id is null or p_id !~ '^[a-z0-9-]{1,80}$' or p_confirmation is distinct from p_id then raise exception 'TYPE_ID_TO_CONFIRM: type the exact draft ID.' using errcode='22023';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if exists(select 1 from public.tutorial_catalog where id=p_id) then raise exception 'REVISION_CONFLICT: catalog exists; reload and review its state.' using errcode='40001';end if;
 select * into d from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid() for update;
 if coalesce(d.revision,0) is distinct from p_draft_revision then raise exception 'REVISION_CONFLICT: draft changed.' using errcode='40001';end if;
 delete from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid();
 return jsonb_build_object('id',p_id,'deleted',true);
end;
$$;
revoke all on function public.admin_delete_tutorial_draft(text,integer,text,uuid) from public,anon,authenticated;
grant execute on function public.admin_delete_tutorial_draft(text,integer,text,uuid) to authenticated;
commit;
