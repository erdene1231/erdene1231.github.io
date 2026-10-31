// Current explicit AtCoder scope; local SQL generation only, no credentials.
import fs from 'node:fs';
import crypto from 'node:crypto';
import {PGlite} from '@electric-sql/pglite';
import {bodyHash} from './part04_tutorial_proposals.mjs';
import {protectedSql,authoritySql,catalogHashSql,historyHashSql,preflightSql} from './package02_confirmed_bank_job.mjs';
export {preflightSql};
const read=name=>fs.readFileSync(new URL('../audit/atcoder-expansion/'+name,import.meta.url),'utf8');
const patchText=read('statement-patches.json'),newText=read('abc-additions.json');
export const statementPatches=JSON.parse(patchText),abcAdditions=JSON.parse(newText);
export const planHashes={statements:'c5dee99a5caaedbd339b86687e6c24311e4eee6f8f54e163bb6bc6f92d597d05',abc:'82e1c1668caceee66561efac43bab37af85ae81a9a07fd8bda1d26369f4448fb'};
if(crypto.createHash('sha256').update(patchText).digest('hex')!==planHashes.statements||crypto.createHash('sha256').update(newText).digest('hex')!==planHashes.abc)throw Error('Reviewed AtCoder file hash differs');
const lit=v=>"E'"+String(v).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'",json=v=>lit(JSON.stringify(v))+'::jsonb';
export async function buildAtcoderJob(g,patches=statementPatches,additions=abcAdditions){
 if(JSON.stringify(patches)!==JSON.stringify(statementPatches)||JSON.stringify(additions)!==JSON.stringify(abcAdditions))throw Error('Reviewed AtCoder allowlist differs');
 if(patches.length!==51||additions.length!==54||new Set(patches.map(p=>p.id)).size!==51||new Set(additions.map(p=>p.canonical_task_id)).size!==54)throw Error('Exact bounded scope required');
 if(!g.owner_catalog||g.authenticated_app_user||g.triggers!==null)throw Error('Fresh unimpersonated owner/trigger baseline required');
 for(const p of patches){const row=g.problems.find(r=>r.problem_id===p.id);if(!row||row.archived||row.number!==p.number||row.revision!==p.expected_revision||bodyHash(row.body)!==p.expected_body_sha256||row.body.source!=='AtCoder'||row.body.ref!==p.ref||row.body.statement||row.body.statementProvenance)throw Error('Fresh statement target CAS differs: '+p.id);}
 for(const p of additions){if(!p.english_available||p.body.source!=='AtCoder'||p.body.ref!==p.canonical_task_id||p.body.url!==p.source_url||Object.hasOwn(p.body,'id')||Object.hasOwn(p.body,'number')||p.body.statement||p.body.editorial)throw Error('Reviewed ABC metadata scope differs');
  if(g.problems.some(r=>r.body.ref?.toLowerCase()===p.canonical_task_id.toLowerCase()||r.body.url?.split(/[?#]/)[0].replace(/\/$/,'').split('/').at(-1).toLowerCase()===p.canonical_task_id.toLowerCase()))throw Error('Existing canonical task duplicate');
 }
 const plan={patches:patches.map(p=>({...p,body_md5:g.problems.find(r=>r.problem_id===p.id).body_md5})),additions};
 const db=new PGlite();let hash;try{hash=(await db.query('select md5($1::jsonb::text) h',[JSON.stringify(plan)])).rows[0].h;}finally{await db.close();}
 return `-- Current reviewed AtCoder request: 51 native bilingual statements + 54 new ABC metadata rows.
-- Plan SHA256 statements=${planHashes.statements}; ABC=${planHashes.abc}.
-- One atomic statement. Allocator gaps on rollback are retained, never reset.
DO $atcoder_catalog$
DECLARE plan jsonb:=${json(plan)}; item jsonb; old public.problem_catalog%rowtype; stored jsonb; before_rows jsonb; row_now record; before_row jsonb;
 created_ids text[]:='{}'; edited_ids text[]:='{}'; history_ids bigint[]:='{}'; hid bigint; n bigint; task_id text;
BEGIN
 PERFORM set_config('lock_timeout','5s',true);
 IF auth.uid() IS NOT NULL OR NOT pg_has_role(current_user,(SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE') THEN RAISE EXCEPTION 'Unimpersonated owner required'; END IF;
 PERFORM pg_advisory_xact_lock(72483160);
 LOCK TABLE public.problem_catalog,public.problem_changes IN SHARE ROW EXCLUSIVE MODE;
 IF md5(plan::text)<>${lit(hash)} OR jsonb_array_length(plan->'patches')<>51 OR jsonb_array_length(plan->'additions')<>54 THEN RAISE EXCEPTION 'Reviewed plan differs'; END IF;
 IF (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count} OR (${catalogHashSql}) IS DISTINCT FROM ${lit(g.catalog_fingerprint)} THEN RAISE EXCEPTION 'Catalog baseline drift'; END IF;
 IF (SELECT count(*) FROM public.problem_changes)<>${g.history_count} OR (${historyHashSql}) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'History baseline drift'; END IF;
 IF EXISTS(SELECT 1 FROM pg_trigger WHERE tgrelid IN('public.problem_catalog'::regclass,'public.problem_changes'::regclass) AND NOT tgisinternal) THEN RAISE EXCEPTION 'Unreviewed trigger'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM ${json(g.protected)} OR (${authoritySql}) IS DISTINCT FROM ${json(g.authority)} THEN RAISE EXCEPTION 'Protected state/authority drift'; END IF;
 IF (SELECT jsonb_build_object('last_value',last_value,'is_called',is_called) FROM public.problem_number_seq) IS DISTINCT FROM ${json(g.sequence)} OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Sequence/source drift'; END IF;
 IF to_regprocedure('public.validate_native_problem_statement(jsonb,jsonb)') IS NULL THEN RAISE EXCEPTION 'Native statement backend required'; END IF;
 SELECT jsonb_object_agg(problem_id,to_jsonb(p)) INTO before_rows FROM public.problem_catalog p;
 -- Validate every target and new identity before allocating any number.
 FOR item IN SELECT value FROM jsonb_array_elements(plan->'patches') LOOP
  SELECT * INTO old FROM public.problem_catalog WHERE problem_id=item->>'id' FOR UPDATE;
  IF old.problem_id IS NULL OR old.archived OR old.number<>(item->>'number')::bigint OR old.revision<>(item->>'expected_revision')::integer OR md5(old.body::text) IS DISTINCT FROM item->>'body_md5' OR old.body?'statement' OR old.body?'statementProvenance' THEN RAISE EXCEPTION 'Statement target CAS drift'; END IF;
  PERFORM public.validate_learning_problem(old.body||jsonb_build_object('statement',item->'statement','statementProvenance',item->'statementProvenance'));
 END LOOP;
 FOR item IN SELECT value FROM jsonb_array_elements(plan->'additions') LOOP
  IF EXISTS(SELECT 1 FROM public.problem_catalog WHERE lower(body->>'ref')=lower(item->>'canonical_task_id') OR lower(regexp_replace(split_part(split_part(rtrim(body->>'url','/'),'?',1),'#',1),'^.*/',''))=lower(item->>'canonical_task_id')) THEN RAISE EXCEPTION 'Canonical ABC duplicate'; END IF;
  IF item->'body' ?| ARRAY['id','number','statement','statementProvenance','editorial'] OR item->'body'->>'source'<>'AtCoder' OR item->'body'->>'ref'<>item->>'canonical_task_id' OR item->'body'->>'url'<>item->>'source_url' THEN RAISE EXCEPTION 'New ABC metadata scope failed'; END IF;
  PERFORM public.validate_learning_problem(item->'body');
 END LOOP;
 FOR item IN SELECT value FROM jsonb_array_elements(plan->'additions') LOOP
  n:=nextval('public.problem_number_seq');task_id:='task-'||n::text;
  stored:=item->'body'||jsonb_build_object('id',task_id,'number',n,'pack',CASE WHEN (item->'body'->>'rating')::integer<=1100 THEN 'foundation' WHEN (item->'body'->>'rating')::integer<=1500 THEN 'core' WHEN (item->'body'->>'rating')::integer<=1800 THEN 'challenge' WHEN (item->'body'->>'rating')::integer<=2100 THEN 'stretch' ELSE 'advanced' END);
  INSERT INTO public.problem_catalog(problem_id,number,body,revision,archived) VALUES(task_id,n,stored,1,false);
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(task_id,NULL,'create',NULL,stored) RETURNING change_id INTO hid;
  created_ids:=array_append(created_ids,task_id);history_ids:=array_append(history_ids,hid);
  -- Atomic ABC create and history complete.
 END LOOP;
 FOR item IN SELECT value FROM jsonb_array_elements(plan->'patches') LOOP
  SELECT * INTO old FROM public.problem_catalog WHERE problem_id=item->>'id';
  stored:=old.body||jsonb_build_object('statement',item->'statement','statementProvenance',item->'statementProvenance');
  UPDATE public.problem_catalog SET body=stored,revision=revision+1,updated_at=now() WHERE problem_id=old.problem_id AND revision=old.revision AND body=old.body;
  IF NOT FOUND THEN RAISE EXCEPTION 'Statement CAS failed'; END IF;
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(old.problem_id,NULL,'edit',old.body,stored) RETURNING change_id INTO hid;
  edited_ids:=array_append(edited_ids,old.problem_id);history_ids:=array_append(history_ids,hid);
  -- Atomic native statement edit and history complete.
 END LOOP;
 FOR row_now IN SELECT * FROM public.problem_catalog LOOP
  before_row:=before_rows->row_now.problem_id;
  IF row_now.problem_id=ANY(created_ids) THEN
   SELECT value INTO item FROM jsonb_array_elements(plan->'additions') WHERE value->'body'->>'ref'=row_now.body->>'ref';
   IF item IS NULL OR row_now.body-ARRAY['id','number','pack'] IS DISTINCT FROM item->'body' OR row_now.body->>'id'<>row_now.problem_id OR (row_now.body->>'number')::bigint<>row_now.number OR row_now.revision<>1 OR row_now.archived OR NOT EXISTS(SELECT 1 FROM public.problem_changes WHERE change_id=ANY(history_ids) AND problem_id=row_now.problem_id AND actor_id IS NULL AND action='create' AND previous_body IS NULL AND next_body=row_now.body) THEN RAISE EXCEPTION 'New ABC postcondition failed'; END IF;
  ELSIF row_now.problem_id=ANY(edited_ids) THEN
   SELECT value INTO item FROM jsonb_array_elements(plan->'patches') WHERE value->>'id'=row_now.problem_id;
   IF to_jsonb(row_now)-ARRAY['body','revision','updated_at'] IS DISTINCT FROM before_row-ARRAY['body','revision','updated_at'] OR row_now.revision<>(before_row->>'revision')::integer+1 OR row_now.body IS DISTINCT FROM (before_row->'body')||jsonb_build_object('statement',item->'statement','statementProvenance',item->'statementProvenance') OR NOT EXISTS(SELECT 1 FROM public.problem_changes WHERE change_id=ANY(history_ids) AND problem_id=row_now.problem_id AND actor_id IS NULL AND action='edit' AND previous_body=before_row->'body' AND next_body=row_now.body) THEN RAISE EXCEPTION 'Statement field/history scope failed'; END IF;
  ELSIF to_jsonb(row_now) IS DISTINCT FROM before_row THEN RAISE EXCEPTION 'Unrelated problem changed'; END IF;
 END LOOP;
 IF cardinality(created_ids)<>54 OR cardinality(edited_ids)<>51 OR (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count}+54 OR (SELECT count(*) FROM public.problem_changes)<>${g.history_count}+105 OR (SELECT last_value FROM public.problem_number_seq)<>${g.sequence.last_value}+54 OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) FROM public.problem_changes h WHERE NOT(change_id=ANY(history_ids))) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'Catalog/history/allocator preservation failed'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM ${json(g.protected)} OR (${authoritySql}) IS DISTINCT FROM ${json(g.authority)} OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Protected postcondition failed'; END IF;
END $atcoder_catalog$;\n`;
}
