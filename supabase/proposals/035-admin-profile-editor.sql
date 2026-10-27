-- PROPOSAL ONLY. No production installation or user/avatar mutation authorized.
-- Independent of032–034. Existing profiles/Storage/is_admin actual-state audit required.
begin;
do $$begin
 if to_regclass('public.admin_profile_audit')is not null or to_regprocedure('public.admin_save_profile(uuid,text,jsonb)')is not null then raise exception '035 exists: re-audit, never replay';end if;
 if not(select relrowsecurity from pg_class where oid='public.profiles'::regclass)or not(select relrowsecurity from pg_class where oid='storage.objects'::regclass)then raise exception '035 requires audited profiles/Storage RLS';end if;
end$$;
create table public.admin_profile_audit(
 audit_id bigint generated always as identity primary key,actor_id uuid not null,target_id uuid not null,
 previous_fields jsonb not null,next_fields jsonb not null,created_at timestamptz not null default now()
);
create table public.admin_profile_avatar_uploads(
 path text primary key,actor_id uuid not null,target_id uuid not null,expires_at timestamptz not null
);
alter table public.admin_profile_audit enable row level security;
alter table public.admin_profile_avatar_uploads enable row level security;
revoke all on public.admin_profile_audit,public.admin_profile_avatar_uploads from public,anon,authenticated;
revoke all on sequence public.admin_profile_audit_audit_id_seq from public,anon,authenticated;
create function public._admin_profile_view(p public.profiles)returns jsonb language sql immutable set search_path=''as $$
 select jsonb_build_object('user_id',p.user_id,'first_name',coalesce(p.first_name,''),'last_name',coalesce(p.last_name,''),'username',p.username,'avatar_path',p.avatar_path,'snapshot',md5(to_jsonb(p)::text));
$$;
create function public.admin_profile_for_edit(p_username text default null,p_target uuid default null)returns jsonb language plpgsql stable security definer set search_path=''as $$
declare p public.profiles%rowtype;begin
 if not public.is_admin()then raise exception 'Admin required'using errcode='42501';end if;
 if (p_username is null)=(p_target is null)then raise exception 'Supply exactly one target'using errcode='22023';end if;
 if p_target is not null then select * into p from public.profiles where user_id=p_target;
 else select * into p from public.profiles where username=lower(btrim(p_username));end if;
 if not found then raise exception 'Profile not found'using errcode='P0002';end if;return public._admin_profile_view(p);
end$$;
create function public.admin_prepare_profile_avatar(p_target uuid,p_expected text)returns text language plpgsql security definer set search_path=''as $$
declare p public.profiles%rowtype;path text;begin
 if not public.is_admin()then raise exception 'Admin required'using errcode='42501';end if;
 select * into p from public.profiles where user_id=p_target for update;
 if not found then raise exception 'Profile not found'using errcode='P0002';end if;
 if md5(to_jsonb(p)::text)is distinct from p_expected then raise exception 'PROFILE_CONFLICT: reload before editing'using errcode='40001';end if;
 path:=p_target::text||'/admin_'||auth.uid()::text||'_'||gen_random_uuid()::text||'.webp';
 insert into public.admin_profile_avatar_uploads values(path,auth.uid(),p_target,now()+interval'15 minutes');return path;
end$$;
create function public.can_upload_admin_profile_avatar(p_path text)returns boolean language sql stable security definer set search_path=''as $$
 select public.is_admin()and exists(select 1 from public.admin_profile_avatar_uploads r join public.profiles p on p.user_id=r.target_id where r.path=p_path and r.actor_id=auth.uid()and r.expires_at>now());
$$;
create function public.can_cleanup_admin_profile_avatar(p_path text)returns boolean language sql stable security definer set search_path=''as $$
 select public.is_admin()and exists(select 1 from public.admin_profile_avatar_uploads r where r.path=p_path and r.actor_id=auth.uid())
 and not exists(select 1 from public.profiles where avatar_path=p_path)
 and not exists(select 1 from public.admin_profile_audit where previous_fields->>'avatar_path'=p_path or next_fields->>'avatar_path'=p_path);
$$;
create policy "Admin reserved profile avatar upload"on storage.objects for insert to authenticated
 with check(bucket_id='think-cp-avatars'and public.can_upload_admin_profile_avatar(name));
create policy "Admin reserved profile avatar inspect"on storage.objects for select to authenticated
 using(bucket_id='think-cp-avatars'and(public.can_upload_admin_profile_avatar(name)or public.can_cleanup_admin_profile_avatar(name)));
create policy "Admin unused reserved profile avatar cleanup"on storage.objects for delete to authenticated
 using(bucket_id='think-cp-avatars'and public.can_cleanup_admin_profile_avatar(name));
create function public.admin_save_profile(p_target uuid,p_expected text,p_changes jsonb)returns jsonb language plpgsql security definer set search_path=''as $$
declare old public.profiles%rowtype;updated public.profiles%rowtype;v_first_name text;v_last_name text;v_username text;avatar text;meta jsonb;begin
 if not public.is_admin()then raise exception 'Admin required'using errcode='42501';end if;
 if jsonb_typeof(p_changes)is distinct from'object'or pg_column_size(p_changes)>4096 then raise exception 'Invalid profile fields'using errcode='22023';end if;
 if exists(select 1 from jsonb_object_keys(p_changes)k where k not in('first_name','last_name','username','avatar_path'))then raise exception 'Field not permitted'using errcode='22023';end if;
 if jsonb_typeof(p_changes->'first_name')is distinct from'string'or jsonb_typeof(p_changes->'last_name')is distinct from'string'or jsonb_typeof(p_changes->'username')is distinct from'string'then raise exception 'Names and username required'using errcode='22023';end if;
 v_first_name:=btrim(p_changes->>'first_name');v_last_name:=btrim(p_changes->>'last_name');v_username:=lower(btrim(p_changes->>'username'));
 if length(v_first_name)>100 or length(v_last_name)>100 or length(btrim(v_last_name||' '||v_first_name))>100 or v_first_name~'[[:cntrl:]]'or v_last_name~'[[:cntrl:]]'or v_username!~'^[a-z0-9_]{3,24}$'then raise exception 'Invalid name or username'using errcode='22023';end if;
 select * into old from public.profiles p where p.user_id=p_target for update;
 if not found then raise exception 'Profile not found'using errcode='P0002';end if;
 if md5(to_jsonb(old)::text)is distinct from p_expected then raise exception 'PROFILE_CONFLICT: reload before editing'using errcode='40001';end if;
 if v_username is distinct from old.username and v_username=any(array['admin','administrator','root','system','support','moderator','erdeneclub','api','auth','null','undefined','constructor','prototype'])then raise exception 'Reserved username'using errcode='22023';end if;
 avatar:=old.avatar_path;
 if p_changes?'avatar_path'then
  if jsonb_typeof(p_changes->'avatar_path')not in('string','null')then raise exception 'Invalid avatar'using errcode='22023';end if;
  avatar:=p_changes->>'avatar_path';
  if avatar is distinct from old.avatar_path and avatar is not null then
   if not exists(select 1 from public.admin_profile_avatar_uploads r where r.path=avatar and r.actor_id=auth.uid()and r.target_id=p_target and r.expires_at>now())then raise exception 'Avatar target/reservation mismatch'using errcode='42501';end if;
   select o.metadata into meta from storage.objects o where o.bucket_id='think-cp-avatars'and o.name=avatar;
   if meta is null or meta->>'mimetype'is distinct from'image/webp'or coalesce(meta->>'size','')!~'^[0-9]{1,8}$'then raise exception 'Invalid uploaded image metadata'using errcode='22023';end if;
   if (meta->>'size')::bigint not between 1 and 2097152 then raise exception 'Image must be at most2MiB'using errcode='22023';end if;
  end if;
 end if;
 update public.profiles p set first_name=v_first_name,last_name=v_last_name,full_name=btrim(v_last_name||' '||v_first_name),username=v_username,avatar_path=avatar where p.user_id=p_target returning * into updated;
 insert into public.admin_profile_audit(actor_id,target_id,previous_fields,next_fields)values(auth.uid(),p_target,public._admin_profile_view(old)-'snapshot',public._admin_profile_view(updated)-'snapshot');
 return public._admin_profile_view(updated);
end$$;
revoke all on function public._admin_profile_view(public.profiles),public.admin_profile_for_edit(text,uuid),public.admin_prepare_profile_avatar(uuid,text),public.can_upload_admin_profile_avatar(text),public.can_cleanup_admin_profile_avatar(text),public.admin_save_profile(uuid,text,jsonb)from public,anon,authenticated;
grant execute on function public.admin_profile_for_edit(text,uuid),public.admin_prepare_profile_avatar(uuid,text),public.can_upload_admin_profile_avatar(text),public.can_cleanup_admin_profile_avatar(text),public.admin_save_profile(uuid,text,jsonb)to authenticated;
commit;
-- No Auth/email/password/roles/school/progress changes;no direct profile table RLS change.
-- Bucket remains public2MiB;no bucket config change;no SQL deletion of Storage objects.
-- Client decodes/re-encodes WebP;server verifies fixed bucket/reservation/MIME/size metadata,
-- not binary pixel content. Live Storage gateway/codec integration is a separate approved check.
