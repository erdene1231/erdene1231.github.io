// Exact licensed reviewed statement batch only; no network or credentials.
import fs from'node:fs';import crypto from'node:crypto';import{PGlite}from'@electric-sql/pglite';
import{bodyHash}from'./part04_tutorial_proposals.mjs';import{protectedSql,authoritySql,catalogHashSql,historyHashSql}from'./package02_confirmed_bank_job.mjs';import{preflightSql}from'./joi_url_job.mjs';
export{preflightSql};
const policySql="SELECT md5(coalesce(jsonb_agg(to_jsonb(p) ORDER BY schemaname,tablename,policyname)::text,'[]')) FROM pg_policies p WHERE schemaname IN('public','study_private','storage')";
const learningTriggersSql="SELECT md5(coalesce(jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgname)::text,'[]')) FROM pg_trigger WHERE tgrelid='public.learning_records'::regclass AND NOT tgisinternal";
const batches={'05':{file:'batch05-plans.json',sha:'59968d680e738ecbf0c75435aca64b41673286d1bb92bd35252dcb2c7974d07e',ids:["task-721", "task-723", "task-896", "task-897", "task-898", "task-899"]},'04':{file:'batch04-plans.json',sha:'e717ca17ea7d7f6e4e2979b2abf3eba2eab603936a290109619e507d1c704c31',ids:["task-720", "task-892", "task-893", "task-894", "task-895"]},'03':{file:'batch03-plans.json',sha:'caa4848e47baced006d649eaf6ad6767f0cbbf3ea01da6d758df0e2b1e48bab4',ids:["task-722", "task-888", "task-889", "task-890", "task-891"]},'02':{file:'batch02-plans.json',sha:'dd65ea56e5ef8e9d5d11196d0e0ed0320cf1173435ff46cc7a9839ffca089c23',ids:['task-884','task-885','task-886','task-887']},'01':{file:'batch01-plans.json',sha:'33303989635d84f50f02eb22c7785536a2e45aa12dbb32c1727b1a7ea4fee06e',ids:['task-880','task-881','task-882','task-883']}};
export function joiStatementBatch(batch='01'){
 const spec=batches[batch];if(!spec)throw Error('Unreviewed statement batch');
 const raw=fs.readFileSync(new URL('../audit/joi-statements/'+spec.file,import.meta.url),'utf8');
 if(crypto.createHash('sha256').update(raw).digest('hex')!==spec.sha)throw Error('Reviewed statement plan hash differs');
 const plan=JSON.parse(raw);if(JSON.stringify(plan.map(p=>p.id))!==JSON.stringify(spec.ids))throw Error('Reviewed statement identity differs');
 return{plan,reviewedHash:spec.sha};
}
export const{plan,reviewedHash}=joiStatementBatch();
const lit=v=>"E'"+String(v).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'",json=v=>lit(JSON.stringify(v))+'::jsonb';
export async function buildFirstJoiStatementJob(g,reviewed=plan){return buildJoiStatementJob('01',g,reviewed);}
export async function buildJoiStatementJob(batch,g,reviewed){
 const{plan,reviewedHash}=joiStatementBatch(batch);reviewed??=plan;
 if(JSON.stringify(reviewed)!==JSON.stringify(plan))throw Error('Reviewed statement allowlist differs');
 if(!g.owner_catalog||g.authenticated_app_user||g.triggers!==null||typeof g.policy_fingerprint!=='string'||typeof g.learning_triggers_fingerprint!=='string')throw Error('Unimpersonated owner/trigger baseline required');
 const db=new PGlite(),items=[];let hash;
 try{for(const p of plan){const row=g.problems.find(r=>r.problem_id===p.id);if(!row||row.archived||row.number!==p.number||row.revision!==p.expected_revision||bodyHash(row.body)!==p.expected_body_sha256||bodyHash(p.statement)!==p.statement_sha256||bodyHash(p.statementProvenance)!==p.provenance_sha256||row.body.statement)throw Error('Fresh statement target CAS differs');const md5=async value=>(await db.query('select md5($1::jsonb::text)h',[JSON.stringify(value)])).rows[0].h;if(await md5(row.body)!==row.body_md5)throw Error('PostgreSQL body representation differs');items.push({id:p.id,number:p.number,revision:p.expected_revision,body_md5:row.body_md5,after_body_md5:await md5({...row.body,statement:p.statement,statementProvenance:p.statementProvenance}),statement:p.statement,statementProvenance:p.statementProvenance});}hash=await (async()=>(await db.query('select md5($1::jsonb::text)h',[JSON.stringify(items)])).rows[0].h)();}finally{await db.close();}
 return `-- User-authorized licensed bilingual statement allowlist SHA256 ${reviewedHash}.
-- Submit once; inspect actual outcome before any retry.
DO $native_statement$
DECLARE items jsonb:=${json(items)};item jsonb;old public.problem_catalog%rowtype;stored jsonb;before_rows jsonb;row_now record;before_row jsonb;edited_ids text[]:='{}';history_ids bigint[]:='{}';hid bigint;
BEGIN
 PERFORM set_config('lock_timeout','5s',true);
 IF auth.uid()IS NOT NULL OR NOT pg_has_role(current_user,(SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE')THEN RAISE EXCEPTION 'Unimpersonated owner required';END IF;
 PERFORM pg_advisory_xact_lock(72483160);LOCK TABLE public.problem_catalog,public.problem_changes IN SHARE ROW EXCLUSIVE MODE;
 IF md5(items::text)<>${lit(hash)} OR jsonb_array_length(items)<>${plan.length} THEN RAISE EXCEPTION 'Reviewed statement allowlist differs';END IF;
 IF (SELECT count(*)FROM public.problem_catalog)<>${g.problem_count} OR(${catalogHashSql})IS DISTINCT FROM ${lit(g.catalog_fingerprint)} THEN RAISE EXCEPTION 'Catalog baseline drift';END IF;
 IF (SELECT count(*)FROM public.problem_changes)<>${g.history_count} OR(${historyHashSql})IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'History baseline drift';END IF;
 IF EXISTS(SELECT 1 FROM pg_trigger WHERE tgrelid IN('public.problem_catalog'::regclass,'public.problem_changes'::regclass)AND NOT tgisinternal)THEN RAISE EXCEPTION 'Unreviewed trigger';END IF;
 IF(${protectedSql})IS DISTINCT FROM ${json(g.protected)} OR(${authoritySql})IS DISTINCT FROM ${json(g.authority)} THEN RAISE EXCEPTION 'Protected state/authority drift';END IF;
 IF(${policySql})IS DISTINCT FROM ${lit(g.policy_fingerprint)} OR(${learningTriggersSql})IS DISTINCT FROM ${lit(g.learning_triggers_fingerprint)} THEN RAISE EXCEPTION 'Policy/learning trigger drift';END IF;
 IF(SELECT jsonb_build_object('last_value',last_value,'is_called',is_called)FROM public.problem_number_seq)IS DISTINCT FROM ${json(g.sequence)} OR(SELECT md5(jsonb_agg(name ORDER BY name)::text)FROM public.problem_sources)IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Allocator/source drift';END IF;
 SELECT jsonb_object_agg(problem_id,to_jsonb(p))INTO before_rows FROM public.problem_catalog p;
 FOR item IN SELECT value FROM jsonb_array_elements(items)LOOP
  SELECT *INTO old FROM public.problem_catalog WHERE problem_id=item->>'id'FOR UPDATE;
  IF old.problem_id IS NULL OR old.archived OR old.number<>(item->>'number')::bigint OR old.revision<>(item->>'revision')::integer OR md5(old.body::text)IS DISTINCT FROM item->>'body_md5' OR old.body?'statement'THEN RAISE EXCEPTION 'Statement target CAS drift';END IF;
  PERFORM public.validate_native_problem_statement(item->'statement',item->'statementProvenance');
  stored:=old.body||jsonb_build_object('statement',item->'statement','statementProvenance',item->'statementProvenance');
  IF stored-ARRAY['statement','statementProvenance']IS DISTINCT FROM old.body OR md5(stored::text)IS DISTINCT FROM item->>'after_body_md5'THEN RAISE EXCEPTION 'Statement-only body mismatch';END IF;
  UPDATE public.problem_catalog SET body=stored,revision=revision+1,updated_at=now()WHERE problem_id=old.problem_id AND revision=old.revision AND body=old.body;
  IF NOT FOUND THEN RAISE EXCEPTION 'Statement CAS failed';END IF;
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body)VALUES(old.problem_id,NULL,'edit',old.body,stored)RETURNING change_id INTO hid;
  edited_ids:=array_append(edited_ids,old.problem_id);history_ids:=array_append(history_ids,hid);
  -- Atomic statement body/history pair complete.
 END LOOP;
 FOR row_now IN SELECT *FROM public.problem_catalog LOOP
  before_row:=before_rows->row_now.problem_id;
  IF row_now.problem_id=ANY(edited_ids)THEN
   SELECT value INTO item FROM jsonb_array_elements(items)WHERE value->>'id'=row_now.problem_id;
   IF to_jsonb(row_now)-ARRAY['body','revision','updated_at']IS DISTINCT FROM before_row-ARRAY['body','revision','updated_at']OR row_now.revision<>(before_row->>'revision')::integer+1 OR row_now.body-ARRAY['statement','statementProvenance']IS DISTINCT FROM before_row->'body' OR md5(row_now.body::text)IS DISTINCT FROM item->>'after_body_md5' OR NOT EXISTS(SELECT 1 FROM public.problem_changes WHERE change_id=ANY(history_ids)AND problem_id=row_now.problem_id AND actor_id IS NULL AND action='edit'AND previous_body=before_row->'body'AND next_body=row_now.body)THEN RAISE EXCEPTION 'Statement field/history scope failed';END IF;
  ELSIF to_jsonb(row_now)IS DISTINCT FROM before_row THEN RAISE EXCEPTION 'Unrelated problem changed';END IF;
 END LOOP;
 IF cardinality(edited_ids)<>${plan.length} OR(SELECT count(*)FROM public.problem_catalog)<>${g.problem_count} OR(SELECT count(*)FROM public.problem_changes)<>${g.history_count}+${plan.length} OR(SELECT md5(coalesce(jsonb_agg(to_jsonb(h)ORDER BY change_id::text)::text,'[]'))FROM public.problem_changes h WHERE NOT(change_id=ANY(history_ids)))IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'Catalog/history preservation failed';END IF;
 IF(${policySql})IS DISTINCT FROM ${lit(g.policy_fingerprint)} OR(${learningTriggersSql})IS DISTINCT FROM ${lit(g.learning_triggers_fingerprint)} THEN RAISE EXCEPTION 'Policy/learning trigger drift';END IF;
 IF(${protectedSql})IS DISTINCT FROM ${json(g.protected)} OR(${authoritySql})IS DISTINCT FROM ${json(g.authority)} OR(SELECT jsonb_build_object('last_value',last_value,'is_called',is_called)FROM public.problem_number_seq)IS DISTINCT FROM ${json(g.sequence)} OR(SELECT md5(jsonb_agg(name ORDER BY name)::text)FROM public.problem_sources)IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Protected postcondition failed';END IF;
END $native_statement$;\n`;
}
