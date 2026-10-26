-- Recovery 024-tutorial-media.sql -> 025-tutorial-media.sql; production 021 prerequisite validation is distinct.
-- Purpose: private tutorial media bucket, safe published delivery and cleanup.
-- Dependencies: 022–024, Supabase Storage. No storage object is directly deleted.
begin;
DO $baseline$
BEGIN
 IF md5(replace(pg_get_functiondef('public.validate_tutorial_body(text,jsonb)'::regprocedure), E'\r\n', E'\n'))<>'d17381308438362f364065137f8ad1a2'
 OR md5(replace(pg_get_functiondef('public.validate_tutorial_publication(text,jsonb)'::regprocedure), E'\r\n', E'\n'))<>'9f866c7b3439bd45d062ce46efbb7e0b'
 OR to_regclass('public.tutorial_media_references') IS NOT NULL
 OR EXISTS(SELECT 1 FROM storage.buckets WHERE id='tutorial-media')
 OR NOT (SELECT relrowsecurity FROM pg_class WHERE oid='storage.objects'::regclass)
 OR EXISTS(SELECT 1 FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' AND p.proname IN ('tutorial_image_paths','refresh_tutorial_media_references','check_tutorial_media_exists','can_read_tutorial_media','can_cleanup_tutorial_media','admin_unused_tutorial_media')) THEN
  RAISE EXCEPTION '025 baseline changed or already applied; re-audit instead of replaying';
 END IF;
END;
$baseline$;
insert into storage.buckets(id,name,public,file_size_limit,allowed_mime_types)
values('tutorial-media','tutorial-media',false,5242880,array['image/webp']);
create table public.tutorial_media_references (
 scope text not null check(scope in ('published','draft','history')),scope_id text not null,
 object_path text not null,primary key(scope,scope_id,object_path)
);
alter table public.tutorial_media_references enable row level security;
revoke all on public.tutorial_media_references from public,anon,authenticated;
create index tutorial_media_reference_path on public.tutorial_media_references(object_path);
create function public.tutorial_image_paths(p_body jsonb) returns table(path text)
language sql immutable set search_path='' as $$
 select distinct value->>'path' from jsonb_path_query(coalesce(p_body,'{}'::jsonb),'$.** ? (@.type == "image")') x(value)
 where value->>'path' ~ '^[a-z0-9-]{1,80}/[0-9a-f-]{36}/[0-9a-f-]{36}\.webp$';
$$;
create function public.refresh_tutorial_media_references() returns trigger
language plpgsql security definer set search_path='' as $$
declare s text;sid text;payload jsonb;
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if TG_TABLE_NAME='tutorial_catalog' then s:='published';sid:=coalesce(new.id,old.id);
 elsif TG_TABLE_NAME='tutorial_drafts' then s:='draft';sid:=coalesce(new.editor_id,old.editor_id)::text||':'||coalesce(new.tutorial_id,old.tutorial_id);
 else s:='history';sid:=new.change_id::text;end if;
 delete from public.tutorial_media_references where scope=s and scope_id=sid;
 if TG_OP='DELETE' then return old;end if;
 if TG_TABLE_NAME='tutorial_catalog' then
  if not new.published then return new;end if;
 end if;
 if TG_TABLE_NAME='tutorial_changes' then payload:=jsonb_build_array(new.previous_body,new.new_body);else payload:=new.body;end if;
 insert into public.tutorial_media_references(scope,scope_id,object_path) select s,sid,path from public.tutorial_image_paths(payload) on conflict do nothing;
 return new;
end;
$$;
create function public.check_tutorial_media_exists() returns trigger
language plpgsql security definer set search_path='' as $$
declare p text;
begin
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 if new.published then
  for p in select path from public.tutorial_image_paths(new.body) loop
   if auth.uid() is not null and not public.can_read_tutorial_media(p) then raise exception 'Image is not accessible to this editor.' using errcode='42501';end if;
   if not exists(select 1 from storage.objects where bucket_id='tutorial-media' and name=p) then raise exception 'Image is missing from Storage: %',p using errcode='22023';end if;
  end loop;
 end if;return new;
end;
$$;
create trigger tutorial_media_check before insert or update on public.tutorial_catalog for each row execute function public.check_tutorial_media_exists();
create trigger tutorial_media_catalog_refs after insert or update or delete on public.tutorial_catalog for each row execute function public.refresh_tutorial_media_references();
create trigger tutorial_media_draft_refs after insert or update or delete on public.tutorial_drafts for each row execute function public.refresh_tutorial_media_references();
create trigger tutorial_media_history_refs after insert on public.tutorial_changes for each row execute function public.refresh_tutorial_media_references();
-- Backfill reference metadata only; never rewrite existing tutorial/draft/history bodies.
insert into public.tutorial_media_references(scope,scope_id,object_path)
select 'published',t.id,p.path from public.tutorial_catalog t cross join lateral public.tutorial_image_paths(t.body) p where t.published
union select 'draft',d.editor_id::text||':'||d.tutorial_id,p.path from public.tutorial_drafts d cross join lateral public.tutorial_image_paths(d.body) p
union select 'history',c.change_id::text,p.path from public.tutorial_changes c cross join lateral public.tutorial_image_paths(jsonb_build_array(c.previous_body,c.new_body)) p
on conflict do nothing;
create function public.can_read_tutorial_media(p_path text) returns boolean
language sql stable security definer set search_path='' as $$
 select (public.is_admin() and split_part(p_path,'/',2)=auth.uid()::text) or exists(select 1 from public.tutorial_media_references where scope='published' and object_path=p_path);
$$;
create function public.can_cleanup_tutorial_media(p_path text) returns boolean
language plpgsql security definer set search_path='' as $$
begin
 if not public.is_admin() then return false;end if;
 perform pg_catalog.pg_advisory_xact_lock(72483161);
 return exists(select 1 from storage.objects where bucket_id='tutorial-media' and name=p_path and created_at<now()-interval '7 days')
 and not exists(select 1 from public.tutorial_media_references where object_path=p_path);
end;
$$;
create function public.admin_unused_tutorial_media() returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not public.is_admin() then raise exception 'Admin required.' using errcode='42501';end if;
 return coalesce((select jsonb_agg(jsonb_build_object('path',name,'created_at',created_at,'bytes',metadata->>'size') order by created_at) from storage.objects o
 where bucket_id='tutorial-media' and created_at<now()-interval '7 days' and not exists(select 1 from public.tutorial_media_references where object_path=o.name)),'[]'::jsonb);
end;
$$;
revoke all on function public.tutorial_image_paths(jsonb),public.refresh_tutorial_media_references(),public.check_tutorial_media_exists() from public,anon,authenticated;
revoke all on function public.can_read_tutorial_media(text),public.can_cleanup_tutorial_media(text),public.admin_unused_tutorial_media() from public,anon,authenticated;
grant execute on function public.can_read_tutorial_media(text) to anon,authenticated;
grant execute on function public.can_cleanup_tutorial_media(text),public.admin_unused_tutorial_media() to authenticated;
create policy "Tutorial images admin insert" on storage.objects for insert to authenticated with check(
 bucket_id='tutorial-media' and (select public.is_admin())
 and name ~ '^[a-z0-9-]{1,80}/[0-9a-f-]{36}/[0-9a-f-]{36}\.webp$'
 and split_part(name,'/',2)=(select auth.uid())::text
);
create policy "Tutorial image published read" on storage.objects for select to anon,authenticated using(bucket_id='tutorial-media' and public.can_read_tutorial_media(name));
create policy "Unused tutorial image cleanup" on storage.objects for delete to authenticated using(bucket_id='tutorial-media' and public.can_cleanup_tutorial_media(name));
DO $existing_images$
BEGIN
 IF EXISTS(SELECT 1 FROM public.tutorial_media_references r WHERE r.scope='published' AND NOT EXISTS(SELECT 1 FROM storage.objects o WHERE o.bucket_id='tutorial-media' AND o.name=r.object_path)) THEN
  RAISE EXCEPTION 'Existing published image is missing; re-audit before migration';
 END IF;
END;
$existing_images$;
commit;
-- Verify: select policyname,cmd from pg_policies where tablename='objects' and policyname like '%utorial%';
-- Cleanup deletes through Storage API only; history/draft/published references block it.
