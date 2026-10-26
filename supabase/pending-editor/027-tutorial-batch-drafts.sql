-- Recovery 026-tutorial-batch-drafts.sql -> 027-tutorial-batch-drafts.sql; production 021 prerequisite validation is distinct.
-- Atomic batch draft import. Existing publication stays unchanged.
-- Replaced private drafts are recoverable only by their original editor.
-- Dependencies: 023-026. No lesson content is embedded in this migration.
begin;
create table if not exists public.tutorial_import_backups (
 backup_id bigint generated always as identity primary key,
 editor_id uuid not null references auth.users(id) on delete cascade,
 tutorial_id text not null,
 body jsonb not null,
 base_revision integer not null,
 draft_revision integer not null,
 created_at timestamptz not null default now()
);
alter table public.tutorial_import_backups enable row level security;
revoke all on public.tutorial_import_backups from public,anon,authenticated;
create index if not exists tutorial_import_backup_owner on public.tutorial_import_backups(editor_id,tutorial_id,backup_id desc);

create or replace function public.tutorial_import_backup_media() returns trigger
language plpgsql security definer set search_path='' as $$
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if tg_op='DELETE' then
  delete from public.tutorial_media_references where scope='history' and scope_id='import:'||old.backup_id::text;
  return old;
 end if;
 insert into public.tutorial_media_references(scope,scope_id,object_path)
 select 'history','import:'||new.backup_id::text,path from public.tutorial_image_paths(new.body)
 on conflict do nothing;
 return new;
end;
$$;
drop trigger if exists tutorial_import_backup_media_refs on public.tutorial_import_backups;
create trigger tutorial_import_backup_media_refs after insert or delete on public.tutorial_import_backups
 for each row execute function public.tutorial_import_backup_media();

create or replace function public.admin_import_tutorial_drafts(p_items jsonb,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare item jsonb;lesson_id text;base integer;draft_rev integer;current_rev integer;
 previous public.tutorial_drafts%rowtype;saved jsonb;result jsonb:='[]'::jsonb;backup bigint;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 if jsonb_typeof(p_items) is distinct from 'array' then raise exception 'Expected import array.' using errcode='22023';end if;
 if jsonb_array_length(p_items) not between 1 and 20 or octet_length(p_items::text)>8388608 then raise exception 'Import supports 1-20 lessons and 8 MB.' using errcode='22023';end if;
 if (select count(*)<>count(distinct value->>'id') from jsonb_array_elements(p_items)) then raise exception 'Duplicate tutorial ID.' using errcode='22023';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 for item in select value from jsonb_array_elements(p_items) loop
  lesson_id:=item->>'id';backup:=null;
  if lesson_id is null or lesson_id !~ '^[a-z0-9-]{1,80}$' or item#>>'{body,id}' is distinct from lesson_id
   or jsonb_typeof(item->'body') is distinct from 'object'
   or jsonb_typeof(item->'baseRevision') is distinct from 'number'
   or jsonb_typeof(item->'draftRevision') is distinct from 'number'
  then raise exception 'Invalid import document.' using errcode='22023';end if;
  if (item->>'baseRevision')::numeric not between 0 and 2147483647
   or (item->>'draftRevision')::numeric not between 0 and 2147483647
   or (item->>'baseRevision')::numeric<>trunc((item->>'baseRevision')::numeric)
   or (item->>'draftRevision')::numeric<>trunc((item->>'draftRevision')::numeric)
  then raise exception 'Invalid revision.' using errcode='22023';end if;
  base:=(item->>'baseRevision')::integer;draft_rev:=(item->>'draftRevision')::integer;
  select revision into current_rev from public.tutorial_catalog where tutorial_catalog.id=lesson_id for update;
  select * into previous from public.tutorial_drafts where tutorial_id=lesson_id and editor_id=auth.uid() for update;
  if coalesce(current_rev,0)<>base or coalesce(previous.revision,0)<>draft_rev
   or (previous.tutorial_id is not null and previous.base_revision<>base)
  then raise exception 'REVISION_CONFLICT: refresh the import preview for %.',lesson_id using errcode='40001';end if;
  if previous.tutorial_id is not null then
   if item->'replaceDraft' is distinct from 'true'::jsonb then raise exception 'Explicit draft replacement selection required.' using errcode='22023';end if;
   insert into public.tutorial_import_backups(editor_id,tutorial_id,body,base_revision,draft_revision)
    values(auth.uid(),lesson_id,previous.body,previous.base_revision,previous.revision) returning backup_id into backup;
  end if;
  saved:=public.admin_save_tutorial_draft(lesson_id,item->'body',base,draft_rev,p_actor);
  result:=result||jsonb_build_array(jsonb_build_object('id',lesson_id,'revision',saved->'revision','backupId',backup));
 end loop;
 return result;
end;
$$;

create or replace function public.admin_tutorial_import_backups(p_id text) returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 return coalesce((select jsonb_agg(to_jsonb(x)) from (
  select backup_id,tutorial_id,body->>'title' as title,base_revision,draft_revision,created_at
  from public.tutorial_import_backups where editor_id=auth.uid() and tutorial_id=p_id
  order by backup_id desc limit 20) x),'[]'::jsonb);
end;
$$;
create or replace function public.admin_tutorial_import_backup_body(p_backup_id bigint) returns jsonb
language plpgsql stable security definer set search_path='' as $$
declare result jsonb;
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 select body into result from public.tutorial_import_backups where backup_id=p_backup_id and editor_id=auth.uid();
 if result is null then raise exception 'Backup not found.' using errcode='22023';end if;
 return result;
end;
$$;
revoke all on function public.tutorial_import_backup_media() from public,anon,authenticated;
revoke all on function public.admin_import_tutorial_drafts(jsonb,uuid),
 public.admin_tutorial_import_backups(text),public.admin_tutorial_import_backup_body(bigint) from public,anon;
grant execute on function public.admin_import_tutorial_drafts(jsonb,uuid),
 public.admin_tutorial_import_backups(text),public.admin_tutorial_import_backup_body(bigint) to authenticated;
commit;
-- Verify: select to_regprocedure('public.admin_import_tutorial_drafts(jsonb,uuid)');
