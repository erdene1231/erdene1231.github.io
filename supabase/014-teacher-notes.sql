-- Run AFTER 013-study-groups.sql. Repeatable; existing learner reports are untouched.
begin;
create table if not exists public.study_teacher_notes (
 group_id uuid not null references public.study_groups(id) on delete cascade,
 user_id uuid not null references auth.users(id) on delete cascade,
 report_date date not null check (isfinite(report_date)),
 note text not null default '' check (length(note)<=8000),
 revision integer not null default 1 check (revision>0),
 updated_at timestamptz not null default now(),
 updated_by uuid references auth.users(id) on delete set null,
 primary key(group_id,user_id,report_date)
);
create table if not exists public.study_teacher_note_history (
 id bigint generated always as identity primary key,
 group_id uuid not null, user_id uuid not null, report_date date not null,
 revision integer not null, actor_id uuid references auth.users(id) on delete set null,
 previous_note text, new_note text not null, changed_at timestamptz not null default now(),
 foreign key(group_id,user_id,report_date) references public.study_teacher_notes(group_id,user_id,report_date) on delete cascade
);
alter table public.study_teacher_notes enable row level security;
alter table public.study_teacher_note_history enable row level security;
revoke all on public.study_teacher_notes,public.study_teacher_note_history from public,anon,authenticated;
revoke all on sequence public.study_teacher_note_history_id_seq from public,anon,authenticated;
grant select on public.study_teacher_notes,public.study_teacher_note_history to authenticated;
drop policy if exists teacher_note_read on public.study_teacher_notes;
create policy teacher_note_read on public.study_teacher_notes for select to authenticated using(study_private.can_view(group_id));
drop policy if exists teacher_note_history_read on public.study_teacher_note_history;
create policy teacher_note_history_read on public.study_teacher_note_history for select to authenticated using(study_private.can_manage(group_id));

create or replace function public.study_save_teacher_note(p_group_id uuid,p_user_id uuid,p_date date,p_note text,p_expected_revision integer default null) returns jsonb
language plpgsql security definer set search_path='' as $$
declare old_row public.study_teacher_notes%rowtype; new_row public.study_teacher_notes%rowtype;
begin
 perform 1 from public.study_groups where id=p_group_id for update;
 if not found or not study_private.can_manage(p_group_id) then
   raise exception 'Багшийн тэмдэглэл засахад группын эсвэл сайтын админ эрх шаардлагатай.' using errcode='42501';
 end if;
 if p_date is null or not isfinite(p_date) or p_note is null or length(p_note)>8000 then
   raise exception 'Огноогоо сонгож, 8000 хүртэл тэмдэгттэй тайлбар бичнэ үү.' using errcode='22023';
 end if;
 select * into old_row from public.study_teacher_notes
   where group_id=p_group_id and user_id=p_user_id and report_date=p_date for update;
 if not exists(select 1 from public.study_group_members where group_id=p_group_id and user_id=p_user_id)
   and not exists(select 1 from public.study_reports where group_id=p_group_id and user_id=p_user_id and report_date=p_date)
   and old_row.user_id is null then
   raise exception 'Тухайн өдөр энэ сурагчид тэмдэглэл үүсгэх боломжгүй.' using errcode='22023';
 end if;
 if old_row.revision is distinct from p_expected_revision then
   raise exception 'Багшийн тэмдэглэл өөрчлөгдсөн байна. Сүүлийн хувилбарыг дахин нээнэ үү.' using errcode='40001';
 end if;
 if old_row.user_id is not null and old_row.note=p_note then return to_jsonb(old_row); end if;
 insert into public.study_teacher_notes as t(group_id,user_id,report_date,note,updated_by)
 values(p_group_id,p_user_id,p_date,p_note,auth.uid())
 on conflict(group_id,user_id,report_date) do update
   set note=excluded.note,revision=t.revision+1,updated_at=now(),updated_by=excluded.updated_by
 returning * into new_row;
 insert into public.study_teacher_note_history(group_id,user_id,report_date,revision,actor_id,previous_note,new_note)
 values(p_group_id,p_user_id,p_date,new_row.revision,auth.uid(),old_row.note,p_note);
 return to_jsonb(new_row);
end;
$$;
revoke all on function public.study_save_teacher_note(uuid,uuid,date,text,integer) from public,anon,authenticated;
grant execute on function public.study_save_teacher_note(uuid,uuid,date,text,integer) to authenticated;

-- Shared read path for the site and every export format. Each note joins on ALL keys.
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
   union select user_id from public.study_teacher_notes where group_id=p_group_id and report_date=any(p_dates)
 ) select jsonb_agg(jsonb_build_object(
     'user_id',roster.user_id,'username',p.username,'last_name',p.last_name,'first_name',p.first_name,
     'full_name',p.full_name,'school',p.school,'report_date',days.day,'is_member',m.user_id is not null,
     'has_report',r.user_id is not null,'solved_problems',coalesce(r.solved_problems,''),
     'problem_count',r.problem_count,'difficulty',coalesce(r.difficulty,''),'topics',coalesce(r.topics,''),
     'notes',coalesce(r.notes,''),'revision',r.revision,'updated_at',r.updated_at,
     'can_edit',study_private.can_manage(p_group_id) or (roster.user_id=auth.uid() and m.user_id is not null),
     'teacher_note',coalesce(t.note,''),'teacher_revision',t.revision,'has_teacher_note',t.user_id is not null,
     'can_edit_teacher',study_private.can_manage(p_group_id))
     order by days.day,p.username nulls last,roster.user_id)
   from days cross join roster
   left join public.profiles p on p.user_id=roster.user_id
   left join public.study_group_members m on m.group_id=p_group_id and m.user_id=roster.user_id
   left join public.study_reports r on r.group_id=p_group_id and r.user_id=roster.user_id and r.report_date=days.day
   left join public.study_teacher_notes t on t.group_id=p_group_id and t.user_id=roster.user_id and t.report_date=days.day
 ),'[]'::jsonb);
end;
$$;
revoke all on function public.study_report_data(uuid,date[]) from public,anon,authenticated;
grant execute on function public.study_report_data(uuid,date[]) to authenticated;
notify pgrst,'reload schema';
commit;
