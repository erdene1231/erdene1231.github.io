-- Read-only verification after 015–020; run sections separately as needed.
-- 015
select to_regprocedure('public.validate_learning_problem(jsonb)') as validator,
       to_regprocedure('public.admin_save_problem(jsonb,bigint,integer)') as save_problem;

-- 016: RLS enabled, owner policy, no anon/public table grants.
select relname, relrowsecurity from pg_class
where oid = to_regclass('public.learning_records');
select policyname, roles, cmd, qual, with_check
from pg_policies where schemaname = 'public' and tablename = 'learning_records';
select grantee, privilege_type from information_schema.role_table_grants
where table_schema = 'public' and table_name = 'learning_records'
order by grantee, privilege_type;

-- 017: existing undated solves should not suddenly become today's activity.
select column_name, data_type from information_schema.columns
where table_schema = 'public' and table_name = 'progress'
  and column_name in ('first_solved_at','first_attempted_at','record_activity');
select count(*) filter (where status='solved' and first_solved_at is null) as undated_legacy,
       count(*) filter (where record_activity) as unconsumed_intents
from public.progress;
select tgname from pg_trigger
where tgrelid='public.progress'::regclass and not tgisinternal;

-- 018–020
select to_regprocedure('public.get_learning_profile(uuid)') as public_profile,
       to_regprocedure('public.admin_import_learning_problems(jsonb,boolean)') as safe_import,
       to_regprocedure('public.admin_store_learning_tutorial(jsonb,integer)') as tutorial_store;

-- Count after import. New numbers depend on actual insert order.
select body->>'source' as source, count(*) as active_problems
from public.problem_catalog where not archived group by 1 order by 1;
select problem_id, number, body->>'title' as title
from public.problem_catalog where body->>'source' ilike 'cses' and body->>'ref'='1071';
select id from public.tutorial_catalog
where id in ('lower-bound','upper-bound','sliding-window','connected-components',
 'bipartite','interval-dp','tree-dp','bellman-ford','string-hashing',
 'invariant','debugging','subtask-strategy') order by id;
