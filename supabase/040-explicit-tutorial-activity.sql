-- Dependency:016. Explicit self-reported activity, server-stamped on the existing
-- authenticated owner-only learning_records save path. No rows are backfilled.
begin;
create or replace function public.preserve_tutorial_activity() returns trigger
language plpgsql set search_path='' as $$
declare prior jsonb:=case when TG_OP='UPDATE' then old.value else '{}'::jsonb end;field text;event jsonb:=new.value->'_activityEvent';preserved jsonb;sections jsonb;item jsonb;
begin
 if new.kind<>'tutorial' or pg_trigger_depth()>1 then return new;end if;
 if event is not null then
  if jsonb_typeof(event)<>'object' then raise exception 'Invalid tutorial activity event';end if;
  -- A reading event is a patch, not permission to replace concurrent checks or
  -- unknown fields. The client removes a field from preserve only for an
  -- explicit edit made while this same intent is pending.
  preserved:=event->'preserve';
  if preserved is null then select coalesce(jsonb_agg(k),'[]'::jsonb)into preserved from jsonb_object_keys(new.value)k where k not in('readSections','_activityEvent','viewedAt','viewedDays','completedAt','viewEventId','completionEventId');end if;
  if jsonb_typeof(preserved)<>'array' then raise exception 'Invalid activity preservation fields';end if;
  new.value:=prior||new.value;
  for field in select jsonb_array_elements_text(preserved)loop
   if field not in('readSections','_activityEvent')and prior?field then new.value:=jsonb_set(new.value,array[field],prior->field);end if;
  end loop;
  if jsonb_typeof(prior->'readSections')='array'and jsonb_typeof(new.value->'readSections')='array'then
   sections:=prior->'readSections';
   for item in select value from jsonb_array_elements(new.value->'readSections')loop if not(sections@>jsonb_build_array(item))then sections:=sections||jsonb_build_array(item);end if;end loop;
   new.value:=jsonb_set(new.value,'{readSections}',sections);
  end if;
 end if;
 foreach field in array array['viewedAt','viewedDays','completedAt','viewEventId','completionEventId']loop
  new.value:=new.value-field;
  if prior?field then new.value:=new.value||jsonb_build_object(field,prior->field);end if;
 end loop;
 return new;
end;
$$;
revoke all on function public.preserve_tutorial_activity() from public,anon,authenticated;
create or replace function public.track_tutorial_activity() returns trigger
language plpgsql set search_path='' as $$
declare
 prior jsonb:=case when TG_OP='UPDATE' then old.value else '{}'::jsonb end;
 event jsonb:=new.value->'_activityEvent';
 stamp text;accepted_at timestamptz;event_id text;action text;section_count integer;was_complete boolean;is_complete boolean;
begin
 if new.kind<>'tutorial' or event is null then return new;end if;
 new.value:=new.value-'_activityEvent';
 if event is null then return new;end if;
 if jsonb_typeof(event)<>'object' then raise exception 'Invalid tutorial activity event';end if;
 event_id:=event->>'id';action:=event->>'type';
 if event_id is null or event_id!~'^[a-f0-9-]{36}$' or action is null or action not in('viewed','completed') then raise exception 'Invalid tutorial activity event';end if;
 if action='viewed' and prior->>'viewEventId'=event_id then
  update public.learning_records set value=new.value where user_id=new.user_id and kind=new.kind and key=new.key;return new;end if;
 if action='completed' and prior->>'completionEventId'=event_id then
  update public.learning_records set value=new.value where user_id=new.user_id and kind=new.kind and key=new.key;return new;end if;
 -- Delayed offline retries must not turn an old interaction into today's event.
 if coalesce(event->>'requestedAt','')!~'^\d{4}-\d{2}-\d{2}T' then raise exception 'Invalid activity time';end if;
 if abs(extract(epoch from(clock_timestamp()-(event->>'requestedAt')::timestamptz)))>600 then raise exception 'Activity request expired; mark the lesson again';end if;
 accepted_at:=clock_timestamp();
 stamp:=to_char(accepted_at at time zone'UTC','YYYY-MM-DD"T"HH24:MI:SS.MS"Z"');
 if action='completed'or event?'sectionCount'then
  if coalesce(event->>'sectionCount','')!~'^[1-9][0-9]{0,3}$'then raise exception 'Invalid tutorial section count';end if;
  section_count:=(event->>'sectionCount')::integer;
  if section_count>1000 then raise exception 'Invalid tutorial section count';end if;
  is_complete:=jsonb_typeof(new.value->'readSections')='array'and not exists(select 1 from generate_series(0,section_count-1)i where not(coalesce(new.value->'readSections','[]'::jsonb)@>jsonb_build_array(i)));
  if action='completed'and not coalesce(is_complete,false)then raise exception 'Complete all tutorial sections first';end if;
  was_complete:=jsonb_typeof(prior->'readSections')='array'and not exists(select 1 from generate_series(0,section_count-1)i where not(coalesce(prior->'readSections','[]'::jsonb)@>jsonb_build_array(i)));
  -- A merged final section from concurrent explicit reading events is also a
  -- real incomplete-to-complete transition. Legacy full reads stay undated.
  if coalesce(is_complete,false)and not coalesce(was_complete,false)and not(prior?'completedAt')then
   new.value:=new.value||jsonb_build_object('completedAt',stamp,'completionEventId',event_id);
  end if;
 end if;
 new.value:=new.value||jsonb_build_object('viewedAt',stamp,'viewEventId',event_id);
 -- Keep distinct real view days so revisiting a lesson never erases an earlier
 -- week's activity. Existing undated reading contributes no historical day.
 if jsonb_typeof(prior->'viewedDays')is distinct from'array' then new.value:=new.value||jsonb_build_object('viewedDays','[]'::jsonb);end if;
 if not(new.value->'viewedDays'@>jsonb_build_array(to_char(accepted_at at time zone'Asia/Ulaanbaatar','YYYY-MM-DD')))then
  new.value:=jsonb_set(new.value,'{viewedDays}',(new.value->'viewedDays')||jsonb_build_array(to_char(accepted_at at time zone'Asia/Ulaanbaatar','YYYY-MM-DD')));
 end if;
 -- The outer row is already locked and RLS still applies. The nested write has
 -- no intent, so it cannot recurse; only this trigger's own update skips the
 -- before-trigger's date preservation. ON CONFLICT now has its true OLD row.
 update public.learning_records set value=new.value where user_id=new.user_id and kind=new.kind and key=new.key;
 return new;
end;
$$;
revoke all on function public.track_tutorial_activity() from public,anon,authenticated;
drop trigger if exists erdene_tutorial_activity_preserve on public.learning_records;
create trigger erdene_tutorial_activity_preserve before insert or update on public.learning_records
for each row execute function public.preserve_tutorial_activity();
drop trigger if exists erdene_tutorial_activity on public.learning_records;
create trigger erdene_tutorial_activity after insert or update on public.learning_records
for each row execute function public.track_tutorial_activity();
commit;
