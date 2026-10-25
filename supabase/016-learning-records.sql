-- Dependency: schema.sql. Private tutorial, plan and bookmark records.
begin;
create table if not exists public.learning_records (
 user_id uuid not null references auth.users(id) on delete cascade,
 kind text not null check(kind in ('tutorial','plan','bookmark')),
 key text not null check(key ~ '^[a-zA-Z0-9_-]{1,100}$'),
 value jsonb not null check(jsonb_typeof(value)='object' and pg_column_size(value)<=20000),
 updated_at timestamptz not null default now(),primary key(user_id,kind,key)
);
alter table public.learning_records enable row level security;
revoke all on public.learning_records from public,anon;
grant select,insert,update,delete on public.learning_records to authenticated;
drop policy if exists "Learning records belong to owner" on public.learning_records;
create policy "Learning records belong to owner" on public.learning_records for all to authenticated
 using ((select auth.uid())=user_id) with check ((select auth.uid())=user_id);
commit;
-- Verify: select tablename,policyname from pg_policies where tablename='learning_records';
