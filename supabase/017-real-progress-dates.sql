-- Dependency: schema.sql. Existing undated solves are never backfilled.
begin;
alter table public.progress add column if not exists first_solved_at timestamptz;
alter table public.progress add column if not exists first_attempted_at timestamptz;
-- Legacy clients/imports omit this intent flag, so they keep unknown dates.
alter table public.progress add column if not exists record_activity boolean not null default false;
create or replace function public.track_first_progress_dates() returns trigger
language plpgsql set search_path='' as $$
begin
 if TG_OP='INSERT' then
  new.first_attempted_at:=case when new.record_activity and new.status in ('trying','solved') then now() end;
  new.first_solved_at:=case when new.record_activity and new.status='solved' then now() end;
 else
  new.first_attempted_at:=old.first_attempted_at;new.first_solved_at:=old.first_solved_at;
  if new.record_activity and old.status='new' and new.status in ('trying','solved') and new.first_attempted_at is null then new.first_attempted_at:=now();end if;
  if new.record_activity and old.status<>'solved' and new.status='solved' and new.first_solved_at is null then new.first_solved_at:=now();end if;
 end if;new.record_activity:=false;return new;
end;
$$;
revoke all on function public.track_first_progress_dates() from public,anon,authenticated;
drop trigger if exists erdene_first_progress_dates on public.progress;
create trigger erdene_first_progress_dates before insert or update on public.progress for each row execute function public.track_first_progress_dates();
create index if not exists progress_user_solved_time on public.progress(user_id,first_solved_at) where first_solved_at is not null;
notify pgrst, 'reload schema';
commit;
-- Verify: select count(*) filter(where status='solved' and first_solved_at is null) as undated_legacy from public.progress;
