-- Erdene Club: groups and daily learning reports. Run after account/admin setup (004+).
-- Independent of tutorial migrations. Repeatable, no seed data or existing data replacement.
begin;

alter table public.profiles add column if not exists first_name text not null default '' check (length(first_name) <= 100);
alter table public.profiles add column if not exists last_name text not null default '' check (length(last_name) <= 100);

create table if not exists public.study_groups (
 id uuid primary key default gen_random_uuid(),
 name text not null check (length(btrim(name)) between 1 and 100),
 description text not null default '' check (length(description) <= 2000),
 visibility text not null default 'private' check (visibility in ('private','public')),
 created_by uuid not null references auth.users(id),
 created_at timestamptz not null default now()
);
create table if not exists public.study_group_members (
 group_id uuid not null references public.study_groups(id) on delete cascade,
 user_id uuid not null references auth.users(id) on delete cascade,
 role text not null default 'member' check (role in ('admin','member')),
 joined_at timestamptz not null default now(),
 primary key (group_id,user_id)
);
create index if not exists study_member_user on public.study_group_members(user_id,group_id);
create table if not exists public.study_reports (
 group_id uuid not null references public.study_groups(id) on delete cascade,
 user_id uuid not null references auth.users(id) on delete cascade,
 report_date date not null check (isfinite(report_date)),
 solved_problems text not null default '' check (length(solved_problems) <= 12000),
 problem_count integer check (problem_count between 0 and 100000),
 difficulty text not null default '' check (length(difficulty) <= 1200),
 topics text not null default '' check (length(topics) <= 2000),
 notes text not null default '' check (length(notes) <= 8000),
 revision integer not null default 1 check (revision > 0),
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 updated_by uuid references auth.users(id) on delete set null,
 primary key (group_id,user_id,report_date)
);
create index if not exists study_reports_date on public.study_reports(group_id,report_date,user_id);
create table if not exists public.study_report_history (
 id bigint generated always as identity primary key,
 group_id uuid not null,
 user_id uuid not null,
 report_date date not null,
 revision integer not null,
 actor_id uuid references auth.users(id) on delete set null,
 previous_body jsonb,
 new_body jsonb not null,
 changed_at timestamptz not null default now(),
 foreign key (group_id,user_id,report_date)
   references public.study_reports(group_id,user_id,report_date) on delete cascade
);
alter table public.study_groups enable row level security;
alter table public.study_group_members enable row level security;
alter table public.study_reports enable row level security;
alter table public.study_report_history enable row level security;
revoke all on public.study_groups,public.study_group_members,public.study_reports,public.study_report_history from public,anon,authenticated;
revoke all on sequence public.study_report_history_id_seq from public,anon,authenticated;
grant select on public.study_groups,public.study_group_members,public.study_reports,public.study_report_history to authenticated;

-- Non-exposed helpers avoid recursive membership RLS. No arbitrary user ID argument.
create schema if not exists study_private;
revoke all on schema study_private from public,anon,authenticated;
grant usage on schema study_private to authenticated;
create or replace function study_private.is_member(p_group_id uuid) returns boolean
language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and exists (
   select 1 from public.study_group_members where group_id=p_group_id and user_id=auth.uid());
$$;
create or replace function study_private.can_manage(p_group_id uuid) returns boolean
language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and (public.is_admin() or exists (
   select 1 from public.study_group_members where group_id=p_group_id and user_id=auth.uid() and role='admin'));
$$;
create or replace function study_private.can_view(p_group_id uuid) returns boolean
language sql stable security definer set search_path='' as $$
 select auth.uid() is not null and exists (
   select 1 from public.study_groups where id=p_group_id and
     (visibility='public' or public.is_admin() or study_private.is_member(p_group_id)));
$$;
revoke all on function study_private.is_member(uuid),study_private.can_manage(uuid),study_private.can_view(uuid) from public,anon,authenticated;
grant execute on function study_private.is_member(uuid),study_private.can_manage(uuid),study_private.can_view(uuid) to authenticated;
drop policy if exists study_group_read on public.study_groups;
create policy study_group_read on public.study_groups for select to authenticated using (study_private.can_view(id));
drop policy if exists study_members_read on public.study_group_members;
create policy study_members_read on public.study_group_members for select to authenticated using (study_private.can_view(group_id));
drop policy if exists study_reports_read on public.study_reports;
create policy study_reports_read on public.study_reports for select to authenticated using (study_private.can_view(group_id));
drop policy if exists study_history_read on public.study_report_history;
create policy study_history_read on public.study_report_history for select to authenticated using (study_private.can_manage(group_id));

create or replace function public.study_list_groups() returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if auth.uid() is null then raise exception 'Эхлээд нэвтэрнэ үү.' using errcode='42501'; end if;
 return jsonb_build_object('site_admin',public.is_admin(),'groups',coalesce((
   select jsonb_agg(item order by is_mine desc,created_at desc) from (
     select g.created_at,m.user_id is not null as is_mine,
       to_jsonb(g)||jsonb_build_object('my_role',m.role,'member_count',
         (select count(*) from public.study_group_members all_m where all_m.group_id=g.id)) as item
     from public.study_groups g
     left join public.study_group_members m on m.group_id=g.id and m.user_id=auth.uid()
     where study_private.can_view(g.id)
   ) s),'[]'::jsonb));
end;
$$;
create or replace function public.study_create_group(p_name text,p_description text default '',p_visibility text default 'private') returns uuid
language plpgsql security definer set search_path='' as $$
declare gid uuid;
begin
 if auth.uid() is null then raise exception 'Эхлээд нэвтэрнэ үү.' using errcode='42501'; end if;
 insert into public.study_groups(name,description,visibility,created_by)
 values(btrim(p_name),coalesce(p_description,''),p_visibility,auth.uid()) returning id into gid;
 insert into public.study_group_members(group_id,user_id,role) values(gid,auth.uid(),'admin');
 return gid;
end;
$$;
create or replace function public.study_update_group(p_group_id uuid,p_name text,p_description text,p_visibility text) returns void
language plpgsql security definer set search_path='' as $$
begin
 perform 1 from public.study_groups where id=p_group_id for update;
 if not found or not study_private.can_manage(p_group_id) then raise exception 'Группын админ эрх шаардлагатай.' using errcode='42501'; end if;
 update public.study_groups set name=btrim(p_name),description=coalesce(p_description,''),visibility=p_visibility where id=p_group_id;
end;
$$;
create or replace function public.study_add_member(p_group_id uuid,p_username text) returns uuid
language plpgsql security definer set search_path='' as $$
declare target uuid;
begin
 perform 1 from public.study_groups where id=p_group_id for update;
 if not found or auth.uid() is null or not (study_private.is_member(p_group_id) or public.is_admin()) then
   raise exception 'Гишүүн нэмэхийн тулд энэ группын гишүүн байна.' using errcode='42501';
 end if;
 select user_id into target from public.profiles where username=lower(btrim(p_username));
 if target is null then raise exception 'Username олдсонгүй. Тухайн сурагч эхлээд бүртгүүлж, username-ээ тохируулна.' using errcode='22023'; end if;
 insert into public.study_group_members(group_id,user_id) values(p_group_id,target) on conflict do nothing;
 return target;
end;
$$;
create or replace function public.study_member_role(p_group_id uuid,p_user_id uuid,p_role text) returns void
language plpgsql security definer set search_path='' as $$
declare old_role text;
begin
 perform 1 from public.study_groups where id=p_group_id for update;
 if not found or not study_private.can_manage(p_group_id) then raise exception 'Группын админ эрх шаардлагатай.' using errcode='42501'; end if;
 if p_role is null or p_role not in ('admin','member','remove') then raise exception 'Буруу эрх.' using errcode='22023'; end if;
 select role into old_role from public.study_group_members where group_id=p_group_id and user_id=p_user_id;
 if old_role is null then raise exception 'Гишүүн олдсонгүй.' using errcode='22023'; end if;
 if old_role='admin' and p_role<>'admin' and (select count(*) from public.study_group_members where group_id=p_group_id and role='admin')<=1 then
   raise exception 'Групп дор хаяж нэг админтай байна. Эхлээд өөр гишүүнд админ эрх өгнө үү.' using errcode='22023';
 end if;
 if p_role='remove' then
   delete from public.study_group_members where group_id=p_group_id and user_id=p_user_id;
 else
   update public.study_group_members set role=p_role where group_id=p_group_id and user_id=p_user_id;
 end if;
end;
$$;
create or replace function public.study_group_detail(p_group_id uuid) returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not study_private.can_view(p_group_id) then raise exception 'Энэ группт хандах эрхгүй.' using errcode='42501'; end if;
 return jsonb_build_object('group',(select to_jsonb(g) from public.study_groups g where id=p_group_id),
   'can_manage',study_private.can_manage(p_group_id),'is_member',study_private.is_member(p_group_id),
   'members',coalesce((select jsonb_agg(jsonb_build_object('user_id',m.user_id,'role',m.role,
       'username',p.username,'full_name',p.full_name,'first_name',p.first_name,'last_name',p.last_name)
       order by m.role,p.username nulls last,m.user_id)
     from public.study_group_members m left join public.profiles p on p.user_id=m.user_id
     where m.group_id=p_group_id),'[]'::jsonb));
end;
$$;
create or replace function public.study_report_data(p_group_id uuid,p_dates date[]) returns jsonb
language plpgsql stable security definer set search_path='' as $$
begin
 if not study_private.can_view(p_group_id) then raise exception 'Энэ группын тайланг харах эрхгүй.' using errcode='42501'; end if;
 if p_dates is null or cardinality(p_dates) not between 1 and 62 or array_position(p_dates,null) is not null
    or exists(select 1 from unnest(p_dates) d where not isfinite(d)) then
   raise exception '1–62 өдөр сонгоно уу.' using errcode='22023';
 end if;
 return coalesce((with days as (select distinct unnest(p_dates) as day), roster as (
   select user_id from public.study_group_members where group_id=p_group_id
   union select user_id from public.study_reports where group_id=p_group_id and report_date=any(p_dates)
 ) select jsonb_agg(jsonb_build_object(
     'user_id',roster.user_id,'username',p.username,'last_name',p.last_name,'first_name',p.first_name,
     'full_name',p.full_name,'school',p.school,'report_date',days.day,'is_member',m.user_id is not null,
     'has_report',r.user_id is not null,'solved_problems',coalesce(r.solved_problems,''),
     'problem_count',r.problem_count,'difficulty',coalesce(r.difficulty,''),'topics',coalesce(r.topics,''),
     'notes',coalesce(r.notes,''),'revision',r.revision,'updated_at',r.updated_at,
     'can_edit',study_private.can_manage(p_group_id) or (roster.user_id=auth.uid() and m.user_id is not null))
     order by days.day,p.username nulls last,roster.user_id)
   from days cross join roster
   left join public.profiles p on p.user_id=roster.user_id
   left join public.study_group_members m on m.group_id=p_group_id and m.user_id=roster.user_id
   left join public.study_reports r on r.group_id=p_group_id and r.user_id=roster.user_id and r.report_date=days.day
 ),'[]'::jsonb);
end;
$$;

create or replace function public.study_save_report(p_group_id uuid,p_user_id uuid,p_date date,p_fields jsonb,p_expected_revision integer default null) returns jsonb
language plpgsql security definer set search_path='' as $$
declare old_row public.study_reports%rowtype; new_row public.study_reports%rowtype;
 count_value integer; fld text; field_limit integer;
begin
 -- Lock group before checking membership; removal/role changes use the same lock.
 perform 1 from public.study_groups where id=p_group_id for update;
 if not found or auth.uid() is null or not (study_private.can_manage(p_group_id) or
    (p_user_id=auth.uid() and study_private.is_member(p_group_id))) then
   raise exception 'Зөвхөн өөрийн тэмдэглэлээ засна. Бусдын тэмдэглэлд админ эрх шаардлагатай.' using errcode='42501';
 end if;
 if p_date is null or not isfinite(p_date) then raise exception 'Огноо сонгоно уу.' using errcode='22023'; end if;
 select * into old_row from public.study_reports where group_id=p_group_id and user_id=p_user_id and report_date=p_date for update;
 if not exists(select 1 from public.study_group_members where group_id=p_group_id and user_id=p_user_id) and old_row.user_id is null then
   raise exception 'Тухайн сурагч группын гишүүн биш байна.' using errcode='22023';
 end if;
 if old_row.revision is distinct from p_expected_revision then
   raise exception 'Тэмдэглэл өөрчлөгдсөн байна. Дахин ачаалаад өөрчлөлтөө оруулна уу.' using errcode='40001';
 end if;
 if p_fields is null or jsonb_typeof(p_fields)<>'object' then raise exception 'Тэмдэглэлийн өгөгдөл буруу.' using errcode='22023'; end if;
 if exists(select 1 from jsonb_object_keys(p_fields) k where k not in ('solved_problems','problem_count','difficulty','topics','notes')) then
   raise exception 'Танихгүй талбар байна.' using errcode='22023';
 end if;
 foreach fld in array array['solved_problems','difficulty','topics','notes'] loop
   field_limit:=case fld when 'solved_problems' then 12000 when 'difficulty' then 1200 when 'topics' then 2000 else 8000 end;
   if (p_fields?fld and jsonb_typeof(p_fields->fld) not in ('string','null')) or length(coalesce(p_fields->>fld,''))>field_limit then
     raise exception 'Талбарын утга эсвэл урт буруу: %',fld using errcode='22023';
   end if;
 end loop;
 if p_fields?'problem_count' and p_fields->'problem_count'<>'null'::jsonb then
   if jsonb_typeof(p_fields->'problem_count')<>'number' or (p_fields->>'problem_count') !~ '^[0-9]{1,6}$' then
     raise exception 'Бодлогын тоо 0–100000 бүхэл тоо байна.' using errcode='22023';
   end if;
   count_value:=(p_fields->>'problem_count')::integer;
   if count_value>100000 then raise exception 'Бодлогын тоо 0–100000 байна.' using errcode='22023'; end if;
 end if;
 if old_row.user_id is not null and old_row.solved_problems=coalesce(p_fields->>'solved_problems','') and
    old_row.problem_count is not distinct from count_value and old_row.difficulty=coalesce(p_fields->>'difficulty','') and
    old_row.topics=coalesce(p_fields->>'topics','') and old_row.notes=coalesce(p_fields->>'notes','') then
   return to_jsonb(old_row);
 end if;
 insert into public.study_reports as r(group_id,user_id,report_date,solved_problems,problem_count,difficulty,topics,notes,updated_by)
 values(p_group_id,p_user_id,p_date,coalesce(p_fields->>'solved_problems',''),count_value,
   coalesce(p_fields->>'difficulty',''),coalesce(p_fields->>'topics',''),coalesce(p_fields->>'notes',''),auth.uid())
 on conflict(group_id,user_id,report_date) do update set solved_problems=excluded.solved_problems,
   problem_count=excluded.problem_count,difficulty=excluded.difficulty,topics=excluded.topics,notes=excluded.notes,
   updated_by=excluded.updated_by,updated_at=now(),revision=r.revision+1
 returning * into new_row;
 insert into public.study_report_history(group_id,user_id,report_date,revision,actor_id,previous_body,new_body)
 values(p_group_id,p_user_id,p_date,new_row.revision,auth.uid(),case when old_row.user_id is null then null else to_jsonb(old_row) end,to_jsonb(new_row));
 return to_jsonb(new_row);
end;
$$;

revoke all on function public.study_list_groups(),public.study_create_group(text,text,text),public.study_update_group(uuid,text,text,text),public.study_add_member(uuid,text),public.study_member_role(uuid,uuid,text),public.study_group_detail(uuid),public.study_report_data(uuid,date[]),public.study_save_report(uuid,uuid,date,jsonb,integer) from public,anon,authenticated;
grant execute on function public.study_list_groups(),public.study_create_group(text,text,text),public.study_update_group(uuid,text,text,text),public.study_add_member(uuid,text),public.study_member_role(uuid,uuid,text),public.study_group_detail(uuid),public.study_report_data(uuid,date[]),public.study_save_report(uuid,uuid,date,jsonb,integer) to authenticated;

notify pgrst,'reload schema';
commit;
