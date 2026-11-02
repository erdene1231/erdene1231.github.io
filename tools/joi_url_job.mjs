// LOCAL REVIEW PREPARATION ONLY. Generates a draft; no network, submission or authorization inference.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {PGlite} from '@electric-sql/pglite';
import {protectedSql,authoritySql,catalogHashSql,historyHashSql,preflightSql as legacyPreflightSql} from './package02_confirmed_bank_job.mjs';
const policySql="SELECT md5(coalesce(jsonb_agg(to_jsonb(p) ORDER BY schemaname,tablename,policyname)::text,'[]')) FROM pg_policies p WHERE schemaname IN('public','study_private','storage')";
const learningTriggersSql="SELECT md5(coalesce(jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgname)::text,'[]')) FROM pg_trigger WHERE tgrelid='public.learning_records'::regclass AND NOT tgisinternal";
export const preflightSql=()=>`SELECT base.recovery||jsonb_build_object('policy_fingerprint',(${policySql}),'learning_triggers_fingerprint',(${learningTriggersSql})) recovery FROM (${legacyPreflightSql().replace(/;\s*$/,'')}) base;`;
const manifestText=fs.readFileSync(new URL('../audit/joi-ojuz/manifest.json',import.meta.url),'utf8');
export const manifest=JSON.parse(manifestText);
export const reviewedHash='8b0d8dc45230b79c814d0a55799986a7f45e008dc37d473152128643c9e66304';
if(crypto.createHash('sha256').update(manifestText).digest('hex')!==reviewedHash)throw Error('Reviewed manifest hash differs');
const lit=v=>"E'"+String(v).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'";
const json=v=>lit(JSON.stringify(v))+'::jsonb';
export async function buildJoiUrlDraft(g,plan=manifest){
 if(JSON.stringify(plan)!==JSON.stringify(manifest))throw Error('Reviewed URL allowlist differs');
 const matched=plan.records.filter(p=>p.decision==='change-url');
 if(plan.records.length!==24||matched.length!==16||new Set(plan.records.map(p=>p.id)).size!==24||plan.records.filter(p=>p.decision==='already-correct').length!==4||plan.records.filter(p=>p.decision==='retain-unmatched').length!==4)throw Error('Identity coverage differs');
 if(!g.owner_catalog||g.authenticated_app_user||g.triggers!==null||typeof g.policy_fingerprint!=='string'||typeof g.learning_triggers_fingerprint!=='string')throw Error('Fresh unimpersonated owner and trigger guards required');
 for(const m of plan.records){
  const p=g.problems.find(p=>p.problem_id===m.id);
  if(!p||p.archived||p.number!==m.number||p.revision!==m.revision||p.body.source!=='JOI'||p.body.title!==m.catalog_title||p.body.ref!==m.catalog_ref||p.body.url!==m.before_url||p.body_md5!==m.before_body_md5||m.decision!=='retain-unmatched'&&(!m.individual_page_read||new URL(m.after_url).origin!=='https://oj.uz'||new URL(m.after_url).pathname!=='/problem/view/'+m.alias))throw Error('Fresh target identity/revision/URL differs: '+m.id);
 }
 const patches=matched.map(m=>({...m,body_md5:g.problems.find(p=>p.problem_id===m.id).body_md5}));
 const db=new PGlite();let patchHash;try{patchHash=(await db.query('select md5($1::jsonb::text) h',[JSON.stringify(patches)])).rows[0].h;}finally{await db.close();}
 return `-- LOCAL REVIEW DRAFT ONLY. JOI URL allowlist SHA256 ${reviewedHash}.
-- NOT SUBMITTED. Publication approval and a fresh revalidated snapshot are required.
-- One statement; never replay after submission without inspecting its outcome.
DO $joi_urls$
DECLARE patches jsonb := ${json(patches)}; item jsonb; old public.problem_catalog%rowtype; stored jsonb;
 before_rows jsonb; row_now record; before_row jsonb; changed_ids text[] := '{}'; history_ids bigint[] := '{}'; hid bigint;
BEGIN
 PERFORM set_config('lock_timeout','5s',true);
 IF auth.uid() IS NOT NULL OR NOT pg_has_role(current_user,(SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE') THEN RAISE EXCEPTION 'Unimpersonated owner required'; END IF;
 PERFORM pg_advisory_xact_lock(72483160);
 LOCK TABLE public.problem_catalog,public.problem_changes IN SHARE ROW EXCLUSIVE MODE;
 LOCK TABLE public.tutorial_catalog,public.tutorial_changes,public.tutorial_drafts,public.progress,public.learning_records,public.profiles,public.problem_sources IN SHARE MODE;
 IF jsonb_array_length(patches)<>16 OR md5(patches::text)<>${lit(patchHash)} THEN RAISE EXCEPTION 'Allowlist differs'; END IF;
 IF (${catalogHashSql}) IS DISTINCT FROM ${lit(g.catalog_fingerprint)} OR (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count} THEN RAISE EXCEPTION 'Catalog baseline drift'; END IF;
 IF (${historyHashSql}) IS DISTINCT FROM ${lit(g.history_fingerprint)} OR (SELECT count(*) FROM public.problem_changes)<>${g.history_count} THEN RAISE EXCEPTION 'History baseline drift'; END IF;
 IF EXISTS(SELECT 1 FROM pg_trigger WHERE tgrelid IN('public.problem_catalog'::regclass,'public.problem_changes'::regclass) AND NOT tgisinternal) THEN RAISE EXCEPTION 'Unreviewed trigger'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM ${json(g.protected)} OR (${authoritySql}) IS DISTINCT FROM ${json(g.authority)} THEN RAISE EXCEPTION 'Protected state/authority drift'; END IF;
 IF (${policySql}) IS DISTINCT FROM ${lit(g.policy_fingerprint)} OR (${learningTriggersSql}) IS DISTINCT FROM ${lit(g.learning_triggers_fingerprint)} THEN RAISE EXCEPTION 'Policy/learning trigger drift'; END IF;
 IF (SELECT jsonb_build_object('last_value',last_value,'is_called',is_called) FROM public.problem_number_seq) IS DISTINCT FROM ${json(g.sequence)} OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Sequence/source drift'; END IF;
 SELECT jsonb_object_agg(problem_id,to_jsonb(p)) INTO before_rows FROM public.problem_catalog p;
 FOR item IN SELECT value FROM jsonb_array_elements(patches) LOOP
  SELECT * INTO old FROM public.problem_catalog WHERE problem_id=item->>'id' FOR UPDATE;
  IF old.problem_id IS NULL OR old.archived OR old.number<>(item->>'number')::bigint OR old.revision<>(item->>'revision')::integer OR md5(old.body::text) IS DISTINCT FROM item->>'body_md5' OR old.body->>'url' IS DISTINCT FROM item->>'before_url' THEN RAISE EXCEPTION 'Target CAS drift'; END IF;
  stored:=jsonb_set(old.body,'{url}',item->'after_url',false);
  PERFORM public.validate_learning_problem(stored);
  IF stored-'url' IS DISTINCT FROM old.body-'url' OR NOT public.valid_task_url(stored->>'url') THEN RAISE EXCEPTION 'URL-only validation failed'; END IF;
  UPDATE public.problem_catalog SET body=stored,revision=revision+1,updated_at=now() WHERE problem_id=old.problem_id AND revision=old.revision AND body=old.body;
  IF NOT FOUND THEN RAISE EXCEPTION 'Target CAS failed'; END IF;
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(old.problem_id,NULL,'edit',old.body,stored) RETURNING change_id INTO hid;
  history_ids:=array_append(history_ids,hid);changed_ids:=array_append(changed_ids,old.problem_id);
  -- Atomic URL and corresponding edit history complete.
 END LOOP;
 FOR row_now IN SELECT * FROM public.problem_catalog LOOP
  before_row:=before_rows->row_now.problem_id;
  IF row_now.problem_id=ANY(changed_ids) THEN
   SELECT value INTO item FROM jsonb_array_elements(patches) WHERE value->>'id'=row_now.problem_id;
   IF to_jsonb(row_now)-ARRAY['body','revision','updated_at'] IS DISTINCT FROM before_row-ARRAY['body','revision','updated_at'] OR row_now.revision<>(before_row->>'revision')::integer+1 OR row_now.body IS DISTINCT FROM jsonb_set(before_row->'body','{url}',item->'after_url',false) THEN RAISE EXCEPTION 'Changed field scope failed'; END IF;
   IF NOT EXISTS(SELECT 1 FROM public.problem_changes WHERE change_id=ANY(history_ids) AND problem_id=row_now.problem_id AND actor_id IS NULL AND action='edit' AND previous_body=before_row->'body' AND next_body=row_now.body) THEN RAISE EXCEPTION 'Edit history mismatch'; END IF;
  ELSIF to_jsonb(row_now) IS DISTINCT FROM before_row THEN RAISE EXCEPTION 'Unrelated problem changed'; END IF;
 END LOOP;
 IF cardinality(changed_ids)<>16 OR (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count} OR (SELECT count(*) FROM public.problem_changes)<>${g.history_count}+16 OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) FROM public.problem_changes h WHERE NOT(change_id=ANY(history_ids))) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'Catalog/history preservation failed'; END IF;
 IF (${policySql}) IS DISTINCT FROM ${lit(g.policy_fingerprint)} OR (${learningTriggersSql}) IS DISTINCT FROM ${lit(g.learning_triggers_fingerprint)} THEN RAISE EXCEPTION 'Policy/learning trigger postcondition failed'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM ${json(g.protected)} OR (${authoritySql}) IS DISTINCT FROM ${json(g.authority)} OR (SELECT jsonb_build_object('last_value',last_value,'is_called',is_called) FROM public.problem_number_seq) IS DISTINCT FROM ${json(g.sequence)} OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Protected postcondition failed'; END IF;
END $joi_urls$;\n`;
}
