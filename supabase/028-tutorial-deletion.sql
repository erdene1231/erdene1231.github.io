-- Explicit permanent removal of an already unpublished tutorial.
-- Depends on applied 021-025. Pending 026/027 are unrelated and are not replayed.
-- No existing content, progress, IDs or Storage objects are changed by installation.
begin;
DO $baseline$
DECLARE expected record;
BEGIN
 IF to_regclass('public.tutorial_deleted_ids') IS NOT NULL
 OR EXISTS (SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace
  WHERE n.nspname='public' AND p.proname IN ('tutorial_deletion_references','guard_deleted_tutorial','admin_delete_tutorial')) THEN
  RAISE EXCEPTION '028 already exists or is partial; re-audit instead of replaying';
 END IF;
 FOR expected IN SELECT * FROM (VALUES
  ('public.validate_tutorial_body(text,jsonb)','d17381308438362f364065137f8ad1a2'),
  ('public.validate_tutorial_publication(text,jsonb)','9f866c7b3439bd45d062ce46efbb7e0b'),
  ('public.admin_set_tutorial_publication(text,integer,boolean,uuid)','74e58fcdc6c7ef51d4b18721b5dc3f5a'),
  ('public.admin_tutorial_document(text)','aa3e740d8a9d8abae5a8ea0ac0f853af'),
  ('public.admin_save_tutorial_draft(text,jsonb,integer,integer,uuid)','55d7fa5a2b24bcb99554f61cc01e8768'),
  ('public.admin_rebase_tutorial_draft(text,jsonb,integer,integer,uuid)','01f6a8cd2db1ea5602240a2b4feef690'),
  ('public.admin_publish_tutorial_draft(text,jsonb,integer,integer,uuid)','81108a26f946a44fdb092377979d0ce6'),
  ('public.refresh_tutorial_media_references()','6448b239602d7eb527c7cd45291dd7bb')
 ) AS baseline(signature,fingerprint) LOOP
  IF to_regprocedure(expected.signature) IS NULL OR
   md5(replace(pg_get_functiondef(to_regprocedure(expected.signature)),E'\r\n',E'\n')) IS DISTINCT FROM expected.fingerprint THEN
   RAISE EXCEPTION '028 baseline changed: %; re-audit before applying',expected.signature;
  END IF;
 END LOOP;
END;
$baseline$;

-- Reserve deleted IDs so old browser drafts cannot resurrect a deleted lesson or
-- attach preserved learner progress to a different tutorial with the same ID.
-- This table contains only IDs: no lesson body, draft, history or user identity.
create table public.tutorial_deleted_ids (
 id text primary key check(id ~ '^[a-z0-9-]{1,80}$')
);
alter table public.tutorial_deleted_ids enable row level security;
revoke all on public.tutorial_deleted_ids from public,anon,authenticated;

-- Read references defensively: drafts may have incomplete or malformed fields.
-- The recursive paths include MN/EN blocks, inline links, and typed links.
create function public.tutorial_deletion_references(p_body jsonb) returns table(target text)
language plpgsql immutable set search_path='' as $$
declare relations jsonb;
begin
 return query select distinct value#>>'{}' from (
  select value from jsonb_path_query(coalesce(p_body,'{}'::jsonb),'$.**.prerequisiteIds[*]') x(value)
  union all select value from jsonb_path_query(coalesce(p_body,'{}'::jsonb),'$.**.related[*]') x(value)
  union all select value from jsonb_path_query(coalesce(p_body,'{}'::jsonb),'$.**.tutorialId') x(value)
  union all select value from jsonb_path_query(coalesce(p_body,'{}'::jsonb),'$.**.learningRelations.next') x(value)
 ) refs where jsonb_typeof(value)='string';
 return query select distinct (regexp_match(value#>>'{}','^#tutorial/([a-z0-9-]+)(/part/[0-9]+)?$'))[1]
  from jsonb_path_query(coalesce(p_body,'{}'::jsonb),'$.**.href') x(value)
  where jsonb_typeof(value)='string' and value#>>'{}' ~ '^#tutorial/([a-z0-9-]+)(/part/[0-9]+)?$';
 if jsonb_typeof(p_body->'_draftRelationsText')='string' then
  begin relations:=(p_body->>'_draftRelationsText')::jsonb;
  exception when data_exception or program_limit_exceeded then relations:=null;end;
  return query select distinct value#>>'{}' from (
   select value from jsonb_path_query(coalesce(relations,'{}'::jsonb),'$.next') x(value)
   union all select value from jsonb_path_query(coalesce(relations,'{}'::jsonb),'$.variants[*].tutorialId') x(value)
  ) refs where jsonb_typeof(value)='string';
 end if;
end;
$$;

create function public.guard_deleted_tutorial() returns trigger
language plpgsql security definer set search_path='' as $$
declare tutorial_id text;
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if TG_TABLE_NAME='tutorial_catalog' then tutorial_id:=new.id;else tutorial_id:=new.tutorial_id;end if;
 if exists(select 1 from public.tutorial_deleted_ids where id=tutorial_id) then
  raise exception 'TUTORIAL_DELETED: this tutorial ID is permanently reserved.' using errcode='22023';
 end if;
 if exists(select 1 from public.tutorial_deletion_references(new.body) r
  join public.tutorial_deleted_ids d on d.id=r.target) then
  raise exception 'TUTORIAL_DELETED_REFERENCE: remove the link to a permanently deleted tutorial.' using errcode='22023';
 end if;
 return new;
end;
$$;
create trigger tutorial_deleted_catalog_guard before insert or update on public.tutorial_catalog
 for each row execute function public.guard_deleted_tutorial();
create trigger tutorial_deleted_draft_guard before insert or update on public.tutorial_drafts
 for each row execute function public.guard_deleted_tutorial();

-- Keep the existing admin-only document contract, adding a reserved-ID flag so
-- fresh editors can explain deleted IDs before creating an unusable local draft.
create or replace function public.admin_tutorial_document(p_id text) returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 return jsonb_build_object('current',(select jsonb_build_object('body',body,'revision',revision,'published',published,'updated_at',updated_at) from public.tutorial_catalog where id=p_id),
 'draft',(select to_jsonb(d)-'editor_id' from public.tutorial_drafts d where d.tutorial_id=p_id and d.editor_id=auth.uid()),
 'deleted',exists(select 1 from public.tutorial_deleted_ids where id=p_id));
end;
$$;

create function public.admin_delete_tutorial(p_id text,p_revision integer,p_confirmation text,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare t public.tutorial_catalog%rowtype;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then
  raise exception 'Admin/actor mismatch.' using errcode='42501';
 end if;
 if p_id is null or p_confirmation is distinct from p_id then
  raise exception 'TYPE_ID_TO_CONFIRM: type the exact tutorial ID.' using errcode='22023';
 end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 select * into t from public.tutorial_catalog where id=p_id for update;
 if t.id is null or t.revision is distinct from p_revision then
  raise exception 'REVISION_CONFLICT: publication changed or the tutorial was already deleted.' using errcode='40001';
 end if;
 if t.published then
  raise exception 'UNPUBLISH_FIRST: temporarily remove this tutorial before deleting it permanently.' using errcode='22023';
 end if;
 if exists(select 1 from public.tutorial_catalog other
  cross join lateral public.tutorial_deletion_references(other.body) r where other.id<>p_id and r.target=p_id)
 or exists(select 1 from public.tutorial_drafts other
  cross join lateral public.tutorial_deletion_references(other.body) r where other.tutorial_id<>p_id and r.target=p_id) then
  -- Do not expose another editor's private content in the error.
  raise exception 'TUTORIAL_REFERENCED: another tutorial or private draft still links to this lesson.' using errcode='22023';
 end if;
 insert into public.tutorial_deleted_ids(id) values(p_id);
 -- History has a catalog FK and an INSERT-only media reference trigger. Remove
 -- its reference metadata before removing history. Catalog/draft DELETE triggers
 -- already remove their own media references. Never touch storage.objects here.
 delete from public.tutorial_media_references r where r.scope='history'
  and r.scope_id in(select change_id::text from public.tutorial_changes where tutorial_id=p_id);
 delete from public.tutorial_changes where tutorial_id=p_id;
 delete from public.tutorial_drafts where tutorial_id=p_id;
 delete from public.tutorial_catalog where id=p_id;
 return jsonb_build_object('id',p_id,'deleted',true);
end;
$$;
revoke all on function public.tutorial_deletion_references(jsonb),public.guard_deleted_tutorial() from public,anon,authenticated;
revoke all on function public.admin_delete_tutorial(text,integer,text,uuid) from public,anon,authenticated;
grant execute on function public.admin_delete_tutorial(text,integer,text,uuid) to authenticated;
revoke all on function public.admin_tutorial_document(text) from public,anon,authenticated;
grant execute on function public.admin_tutorial_document(text) to authenticated;
commit;
