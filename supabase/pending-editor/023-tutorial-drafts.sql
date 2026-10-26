-- Recovery 022-tutorial-drafts.sql -> 023-tutorial-drafts.sql; production 021 prerequisite validation is distinct.
-- Purpose: private per-editor drafts + optimistic revisions. Dependency: 021.
begin;
alter table public.tutorial_catalog add column if not exists published boolean not null default true;
alter table public.tutorial_catalog add column if not exists published_at timestamptz;
create table if not exists public.tutorial_drafts (
 tutorial_id text not null check(tutorial_id ~ '^[a-z0-9-]{1,80}$'),
 editor_id uuid not null references auth.users(id) on delete cascade,
 body jsonb not null check(jsonb_typeof(body)='object' and pg_column_size(body)<=1500000),
 base_revision integer not null check(base_revision>=0),revision integer not null default 1 check(revision>0),
 updated_at timestamptz not null default now(),primary key(tutorial_id,editor_id)
);
alter table public.tutorial_drafts enable row level security;
revoke all on public.tutorial_drafts from public,anon,authenticated;
-- RPC writes enforce both actor and optimistic revision; no direct table writes.
create or replace function public.admin_tutorial_workspace() returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 return jsonb_build_object('catalog',coalesce((select jsonb_agg(jsonb_build_object('id',id,'title',body->>'title','category',body->>'category','levelKey',body->>'levelKey','published',published,'revision',revision,'updated_at',updated_at) order by body->>'title') from public.tutorial_catalog),'[]'::jsonb),
 'drafts',coalesce((select jsonb_agg(jsonb_build_object('tutorial_id',tutorial_id,'title',body->>'title','category',body->>'category','levelKey',body->>'levelKey','revision',revision,'base_revision',base_revision,'updated_at',updated_at) order by updated_at desc) from public.tutorial_drafts where editor_id=auth.uid()),'[]'::jsonb));
end;
$$;
create or replace function public.admin_tutorial_document(p_id text) returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 return jsonb_build_object('current',(select jsonb_build_object('body',body,'revision',revision,'published',published,'updated_at',updated_at) from public.tutorial_catalog where id=p_id),
 'draft',(select to_jsonb(d)-'editor_id' from public.tutorial_drafts d where d.tutorial_id=p_id and d.editor_id=auth.uid()));
end;
$$;
create or replace function public.admin_save_tutorial_draft(p_id text,p_body jsonb,p_base_revision integer,p_draft_revision integer,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare d public.tutorial_drafts%rowtype;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 if p_id is null or p_id !~ '^[a-z0-9-]{1,80}$' or jsonb_typeof(p_body) is distinct from 'object' or p_body->>'id' is distinct from p_id or pg_column_size(p_body)>1500000 or p_base_revision is null or p_base_revision<0 or p_draft_revision is null or p_draft_revision<0 then raise exception 'Invalid draft.' using errcode='22023';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 select * into d from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid() for update;
 if coalesce(d.revision,0)<>p_draft_revision then raise exception 'REVISION_CONFLICT: draft changed.' using errcode='40001';end if;
 if d.tutorial_id is not null and d.base_revision<>p_base_revision then raise exception 'REVISION_CONFLICT: draft base changed.' using errcode='40001';end if;
 insert into public.tutorial_drafts(tutorial_id,editor_id,body,base_revision,revision) values(p_id,auth.uid(),p_body,p_base_revision,1)
 on conflict(tutorial_id,editor_id) do update set body=excluded.body,revision=tutorial_drafts.revision+1,updated_at=now()
 returning * into d;return to_jsonb(d)-'editor_id';
end;
$$;
-- Explicit rebase after the editor has compared local and published versions.
create or replace function public.admin_rebase_tutorial_draft(p_id text,p_body jsonb,p_current_revision integer,p_draft_revision integer,p_actor uuid) returns jsonb
language plpgsql security definer set search_path='' as $$
declare d public.tutorial_drafts%rowtype;current_revision integer;
begin
 if not public.is_admin() or auth.uid() is distinct from p_actor then raise exception 'Admin/actor mismatch.' using errcode='42501';end if;
 if p_id is null or p_id !~ '^[a-z0-9-]{1,80}$' or jsonb_typeof(p_body) is distinct from 'object' or p_body->>'id' is distinct from p_id or pg_column_size(p_body)>1500000 then raise exception 'Invalid draft.' using errcode='22023';end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 select revision into current_revision from public.tutorial_catalog where id=p_id for update;
 select * into d from public.tutorial_drafts where tutorial_id=p_id and editor_id=auth.uid() for update;
 if coalesce(current_revision,0) is distinct from p_current_revision or coalesce(d.revision,0) is distinct from p_draft_revision then raise exception 'REVISION_CONFLICT: compare the latest versions again.' using errcode='40001';end if;
 insert into public.tutorial_drafts(tutorial_id,editor_id,body,base_revision,revision) values(p_id,auth.uid(),p_body,p_current_revision,1)
 on conflict(tutorial_id,editor_id) do update set body=excluded.body,base_revision=excluded.base_revision,revision=tutorial_drafts.revision+1,updated_at=now()
 returning * into d;
 return to_jsonb(d)-'editor_id';
end;
$$;
revoke all on function public.admin_rebase_tutorial_draft(text,jsonb,integer,integer,uuid) from public,anon;
grant execute on function public.admin_rebase_tutorial_draft(text,jsonb,integer,integer,uuid) to authenticated;
create or replace function public.admin_tutorial_history(p_id text) returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 return coalesce((select jsonb_agg(jsonb_build_object('revision',revision,'title',body->>'title','updated_at',stamp) order by revision desc) from (
  select distinct on(revision) revision,body,stamp from (
   select revision,body,updated_at stamp from public.tutorial_catalog where id=p_id
   union all select revision,new_body,created_at from public.tutorial_changes where tutorial_id=p_id
   union all select revision-1,previous_body,created_at from public.tutorial_changes where tutorial_id=p_id and revision>1
  ) versions where body->>'id'=p_id order by revision desc,stamp desc limit 50
 ) v),'[]'::jsonb);
end;
$$;
create or replace function public.admin_tutorial_history_body(p_id text,p_revision integer) returns jsonb
language plpgsql stable security definer set search_path='' as $$
declare result jsonb;
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 select body into result from (
  select revision,body,updated_at stamp from public.tutorial_catalog where id=p_id
  union all select revision,new_body,created_at from public.tutorial_changes where tutorial_id=p_id
  union all select revision-1,previous_body,created_at from public.tutorial_changes where tutorial_id=p_id and revision>1
 ) v where revision=p_revision and body->>'id'=p_id order by stamp desc limit 1;
 if result is null then raise exception 'Revision not found.' using errcode='22023';end if;return result;
end;
$$;
revoke all on function public.admin_tutorial_workspace(),public.admin_tutorial_document(text),public.admin_save_tutorial_draft(text,jsonb,integer,integer,uuid),public.admin_tutorial_history(text),public.admin_tutorial_history_body(text,integer) from public,anon;
grant execute on function public.admin_tutorial_workspace(),public.admin_tutorial_document(text),public.admin_save_tutorial_draft(text,jsonb,integer,integer,uuid),public.admin_tutorial_history(text),public.admin_tutorial_history_body(text,integer) to authenticated;
commit;
-- Verify: select to_regprocedure('public.admin_save_tutorial_draft(text,jsonb,integer,integer,uuid)');
