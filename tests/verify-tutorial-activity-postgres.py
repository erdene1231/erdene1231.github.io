"""Isolated network-less PostgreSQL17 fixture; no production/user connections."""
import subprocess,json,time,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];container='erdene-activity-fixture';docker=['env','-u','DOCKER_HOST','-u','DOCKER_CONTEXT','-u','DOCKER_TLS','-u','DOCKER_TLS_VERIFY','-u','DOCKER_CERT_PATH','docker','--host=unix:///var/run/docker.sock'];alice='00000000-0000-0000-0000-000000000001';bob='00000000-0000-0000-0000-000000000002'
def command():return docker+['exec','-i',container,'psql','-U','postgres','-v','ON_ERROR_STOP=1','-Atq']
def sql(text):
 p=subprocess.run(command(),input=text,text=True,capture_output=True,timeout=30)
 if p.returncode:raise AssertionError(p.stderr)
 return p.stdout.strip()
def actor(text,user=alice):return f"set role authenticated;set request.jwt.claim.sub='{user}';"+text
serial=0
def value(kind='viewed',sections=None,eid=None):
 global serial
 serial+=1;return{'readSections':sections or[0],'checks':['purpose'],'unknown':{'keep':True},'_activityEvent':{'id':eid or f'00000000-0000-4000-8000-{serial:012d}','type':kind,'requestedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'sectionCount':2}}
def put(key,v):return"insert into learning_records(user_id,kind,key,value)values('"+alice+"','tutorial','"+key+"',"+"'"+json.dumps(v).replace("'","''")+"'::jsonb)on conflict(user_id,kind,key)do update set value=excluded.value returning value::text;"
def get(key):return json.loads(sql(actor("select value::text from learning_records where key='"+key+"';")))
try:
 for _ in range(60):
  main=subprocess.run(docker+['exec',container,'cat','/proc/1/comm'],capture_output=True,text=True)
  p=subprocess.run(docker+['exec',container,'pg_isready','-U','postgres'],capture_output=True)
  if main.stdout.strip()=='postgres'and p.returncode==0:break
  time.sleep(.2)
 else:raise AssertionError('Fixture PostgreSQL did not become ready')
 sql(f"create role anon;create role authenticated;create schema auth;create table auth.users(id uuid primary key);insert into auth.users values('{alice}'),('{bob}');create function auth.uid()returns uuid language sql stable as $$select nullif(current_setting('request.jwt.claim.sub',true),'')::uuid$$;grant usage on schema auth to authenticated;")
 sql((ROOT/'supabase/016-learning-records.sql').read_text());permissions=sql("select coalesce(relacl::text,'')||':'||relrowsecurity from pg_class where oid='learning_records'::regclass;")
 sql((ROOT/'supabase/040-explicit-tutorial-activity.sql').read_text());assert permissions==sql("select coalesce(relacl::text,'')||':'||relrowsecurity from pg_class where oid='learning_records'::regclass;")
 first=value('completed',[0,1]);returned=json.loads(sql(actor(put('insert',first))));committed=get('insert');assert '_activityEvent'in returned and'_activityEvent'not in committed;assert committed['completedAt']and committed['viewedAt'];assert committed['checks']==['purpose']and committed['unknown']=={'keep':True}
 retry={**committed,'_activityEvent':{**first['_activityEvent'],'requestedAt':'2000-01-01T00:00:00Z'}};sql(actor(put('insert',retry)));assert get('insert')==committed
 # Real independent sessions overlap on an absent row. B waits on A's insert.
 a=value('viewed',[0]);a['unknown']={'concurrent':'first'};b=value('viewed',[1]);b['unknown']={'stale':'second'};pa=subprocess.Popen(command(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);pa.stdin.write(actor('begin;'+put('raced-insert',a)+'select pg_sleep(1);commit;'));pa.stdin.close();time.sleep(.15)
 pb=subprocess.Popen(command(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);pb.stdin.write(actor(put('raced-insert',b)));pb.stdin.close();time.sleep(.2);blocked=int(sql("select count(*)from pg_stat_activity where wait_event_type='Lock'and query like '%raced-insert%';"));assert blocked>=1
 assert pa.wait(timeout=10)==pb.wait(timeout=10)==0;after=get('raced-insert');assert after['completionEventId']==b['_activityEvent']['id'];assert after['completedAt']and'_activityEvent'not in after;assert after['readSections']==[0,1]and after['unknown']=={'concurrent':'first'}and after['checks']==['purpose']
 # Concurrent updates: later explicit viewing preserves the first completion.
 a=value('completed',[0,1]);b=value('viewed',[0,1]);sql(actor(put('raced-update',value('viewed',[0]))));pa=subprocess.Popen(command(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);pa.stdin.write(actor('begin;'+put('raced-update',a)+'select pg_sleep(1);commit;'));pa.stdin.close();time.sleep(.15)
 pb=subprocess.Popen(command(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);pb.stdin.write(actor(put('raced-update',b)));pb.stdin.close();time.sleep(.2);blocked_update=int(sql("select count(*)from pg_stat_activity where wait_event_type='Lock'and query like '%raced-update%';"));assert blocked_update>=1;assert pa.wait(timeout=10)==pb.wait(timeout=10)==0;after=get('raced-update');assert after['completionEventId']==a['_activityEvent']['id']and after['viewEventId']==b['_activityEvent']['id']
 ordinary={**after,'completedAt':'2000-01-01T00:00:00Z','viewedAt':'2000-01-01T00:00:00Z','checks':['purpose','correctness']};sql(actor(put('raced-update',ordinary)));saved=get('raced-update');assert saved['completedAt']==after['completedAt']and saved['viewedAt']==after['viewedAt'];assert saved['unknown']=={'keep':True}
 legacy={'readSections':[0,1],'checks':['purpose'],'unknown':{'legacy':True}};sql(actor(put('legacy',legacy)));assert'completedAt'not in get('legacy');sql(actor(put('legacy',{**legacy,'_activityEvent':value('completed',[0,1])['_activityEvent']})));assert'completedAt'not in get('legacy')
 assert sql(actor('select count(*)from learning_records;',bob))=='0';foreign=subprocess.run(command(),input=actor(put('foreign',value()),bob),text=True,capture_output=True);assert foreign.returncode!=0 and'row-level security'in foreign.stderr
 before=sql('select jsonb_agg(to_jsonb(l)order by key)::text from learning_records l;');sql((ROOT/'supabase/040-explicit-tutorial-activity.sql').read_text());assert before==sql('select jsonb_agg(to_jsonb(l)order by key)::text from learning_records l;')
 assert sql("select has_function_privilege('authenticated','track_tutorial_activity()','execute')or has_function_privilege('authenticated','preserve_tutorial_activity()','execute')or has_function_privilege('anon','track_tutorial_activity()','execute');")=='f'
 result={'status':'passed','postgres_version':sql('show server_version;'),'isolated_container_network':'none; no published ports; synthetic users only','true_insert_and_on_conflict_update':True,'actual_independent_session_insert_contention_observed':blocked,'actual_independent_session_update_contention_observed':blocked_update,'concurrent_read_sections_merged_and_completion_detected':True,'stale_reading_intents_preserve_server_checks_and_unknown_fields':True,'upsert_returning_stale_intent_demonstrated':True,'fresh_committed_own_row_readback':True,'uncertain_response_same_event_id_retry_stable_even_after_expiry':True,'ordinary_dates_unknown_fields_checks_preserved':True,'legacy_undated_completion_not_backfilled':True,'owner_RLS_isolation_and_function_execute_denial':True,'table_grants_and_RLS_unchanged':True,'migration_does_not_rewrite_existing_rows':True,'production_connections':0}
 (ROOT/'audit/ui-followup/040-postgres-concurrency.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
finally:
 subprocess.run(docker+['stop',container],capture_output=True,timeout=30)
