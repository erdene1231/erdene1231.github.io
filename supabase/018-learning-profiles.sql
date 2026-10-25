-- Dependencies: 003, 016, 017. Only public profile/status facts, no private notes.
begin;
alter table public.profiles add column if not exists bio text not null default '' check(length(bio)<=300);
create or replace function public.get_learning_profile(p_user_id uuid) returns jsonb
language sql stable security definer set search_path='' as $$
 select jsonb_build_object(
  'profile',to_jsonb(pr)||jsonb_build_object('bio',p.bio,'joined_at',u.created_at),
  'progress',coalesce((select jsonb_agg(jsonb_build_object('problem_id',pg.problem_id,'status',pg.status,'first_solved_at',pg.first_solved_at,'first_attempted_at',pg.first_attempted_at))
   from public.progress pg join public.problem_catalog pc using(problem_id) where pg.user_id=p_user_id and pg.status in ('trying','solved')),'[]'::jsonb),
  'plan',coalesce((select jsonb_build_object('started',lr.value ? 'startedAt','paused',coalesce(lr.value->'paused'='true'::jsonb,false),'completedDays',case when jsonb_typeof(lr.value->'completedDays')='array' then (select count(distinct day_index) from (select case when jsonb_typeof(d.value)='number' and d.value::text ~ '^[0-9]{1,3}$' then d.value::text::integer end as day_index from jsonb_array_elements(lr.value->'completedDays') d(value)) valid_days where day_index between 1 and 100) else 0 end)
   from public.learning_records lr where lr.user_id=p_user_id and lr.kind='plan' and lr.key='olympiad-100-v1'),'{}'::jsonb))
 from public.get_public_profile(p_user_id) pr join public.profiles p on p.user_id=pr.user_id join auth.users u on u.id=p.user_id;
$$;
revoke all on function public.get_learning_profile(uuid) from public;
grant execute on function public.get_learning_profile(uuid) to anon,authenticated;
commit;
-- Verify: select to_regprocedure('public.get_learning_profile(uuid)');
