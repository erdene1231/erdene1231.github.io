// Exact confirmed package-2 subset only. Generates SQL locally; no credentials/network.
import {PGlite} from '@electric-sql/pglite';
import {bodyHash} from './package02_tutorial_proposals.mjs';
export const reviewedAllowlistHash='07964ff156af381d9d9cd4aea6150d3dddb1bca11775b5814b2cb0ceb908dd23';
const newKeys=['EGOI/2024/gardendecorations','EGOI/2024/lightbulbs','IOI/2020/mushrooms','IOI/2022/prison','IOI/2024/sphinx','IOI/2025/migrations','IOI/2025/souvenirs','IOI/2026/ballmachine','IOI/2026/classroom','IOI/2026/partition'];
const patchIds=['task-736','task-902','task-908','task-911','task-930','task-935'];
const signatures=['admin_import_problems(jsonb)','admin_save_problem(jsonb,bigint,integer)','is_admin()','normalize_problem_source(text)','valid_task_url(text)','validate_learning_problem(jsonb)','validate_priority_metadata(jsonb)'];
const lit=v=>"E'"+String(v).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'",json=v=>lit(JSON.stringify(v))+'::jsonb';
export const protectedSql=`SELECT jsonb_build_object(
 'tutorials',(SELECT md5(coalesce(jsonb_agg(to_jsonb(t) ORDER BY id)::text,'[]')) FROM public.tutorial_catalog t),
 'tutorial_history',(SELECT md5(coalesce(jsonb_agg(to_jsonb(t) ORDER BY to_jsonb(t)::text)::text,'[]')) FROM public.tutorial_changes t),
 'drafts',(SELECT md5(coalesce(jsonb_agg(to_jsonb(t) ORDER BY to_jsonb(t)::text)::text,'[]')) FROM public.tutorial_drafts t),
 'progress',(SELECT md5(coalesce(jsonb_agg(to_jsonb(t) ORDER BY to_jsonb(t)::text)::text,'[]')) FROM public.progress t),
 'learning',(SELECT md5(coalesce(jsonb_agg(to_jsonb(t) ORDER BY to_jsonb(t)::text)::text,'[]')) FROM public.learning_records t),
 'profiles',(SELECT md5(coalesce(jsonb_agg(to_jsonb(t) ORDER BY to_jsonb(t)::text)::text,'[]')) FROM public.profiles t))`;
export const authoritySql=`SELECT jsonb_build_object(
 'objects',(SELECT md5(jsonb_agg(jsonb_build_object('schema',n.nspname,'object',c.relname,'kind',c.relkind,'acl',c.relacl::text,'rls',c.relrowsecurity,'forced',c.relforcerowsecurity) ORDER BY n.nspname,c.relname)::text) FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname IN('public','study_private','storage') AND c.relkind IN('r','p','S','v')),
 'functions',(SELECT md5(jsonb_agg(jsonb_build_object('signature',p.oid::regprocedure::text,'definition',pg_get_functiondef(p.oid),'acl',p.proacl::text) ORDER BY p.oid::regprocedure::text)::text) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname IN('public','study_private') AND p.prokind='f'))`;
export const catalogHashSql='SELECT md5(jsonb_agg(to_jsonb(p) ORDER BY problem_id)::text) FROM public.problem_catalog p';
export const historyHashSql="SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) FROM public.problem_changes h";
export function preflightSql(){return `SELECT jsonb_build_object('captured_at',transaction_timestamp(),'owner_catalog',pg_has_role(current_user,(SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE'),'authenticated_app_user',auth.uid() IS NOT NULL,'problems',(SELECT jsonb_agg(to_jsonb(p)||jsonb_build_object('body_md5',md5(body::text)) ORDER BY number) FROM public.problem_catalog p),'problem_count',(SELECT count(*) FROM public.problem_catalog),'catalog_fingerprint',(${catalogHashSql}),'history_count',(SELECT count(*) FROM public.problem_changes),'history_fingerprint',(${historyHashSql}),'sequence',(SELECT jsonb_build_object('last_value',last_value,'is_called',is_called) FROM public.problem_number_seq),'sources',(SELECT jsonb_agg(name ORDER BY name) FROM public.problem_sources),'source_fingerprint',(SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources),'functions',(SELECT jsonb_agg(jsonb_build_object('signature',p.oid::regprocedure::text,'definition_md5',md5(pg_get_functiondef(p.oid)),'acl',p.proacl::text) ORDER BY p.oid::regprocedure::text) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' AND p.proname IN('admin_import_problems','admin_save_problem','is_admin','normalize_problem_source','valid_task_url','validate_learning_problem','validate_priority_metadata')),'triggers',(SELECT jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgrelid::regclass::text,tgname) FROM pg_trigger WHERE tgrelid IN('public.problem_catalog'::regclass,'public.problem_changes'::regclass) AND NOT tgisinternal),'protected',(${protectedSql}),'authority',(${authoritySql})) AS recovery;`;}
export async function buildConfirmedBankJob(plan,g){
 const manifest={new_records:plan.new_records,tag_patches:plan.tag_patches};
 if(bodyHash(manifest)!==reviewedAllowlistHash)throw Error('Reviewed metadata allowlist hash differs');
 if(JSON.stringify(plan.new_records.map(r=>[r.identity.source,r.identity.year,r.identity.task].join('/')).sort())!==JSON.stringify(newKeys)||JSON.stringify(plan.tag_patches.map(p=>p.id).sort())!==JSON.stringify(patchIds))throw Error('Exact confirmed identity scope required');
 if(!g.owner_catalog||g.authenticated_app_user||g.problem_count!==plan.before_count||!g.sequence.is_called||!Number.isSafeInteger(g.sequence.last_value)||g.sequence.last_value<g.problem_count||g.triggers!==null)throw Error('Fresh unimpersonated owner/catalog guards required');
 const functions=g.functions.map(f=>({...f,signature:f.signature.replace(/^public\./,'')}));if(JSON.stringify(functions.map(f=>f.signature).sort())!==JSON.stringify(signatures))throw Error('Exact installed function guards required');
 for(const field of['catalog_fingerprint','history_fingerprint','source_fingerprint'])if(!/^[a-f0-9]{32}$/.test(g[field]))throw Error('Missing hash guard '+field);
 for(const obj of[g.protected,g.authority])if(!obj||Object.values(obj).some(v=>!/^[a-f0-9]{32}$/.test(v)))throw Error('Protected/authority fingerprints required');
 for(const patch of plan.tag_patches){const old=g.problems.find(p=>p.problem_id===patch.id);if(!old||old.archived||old.number!==patch.number||old.revision!==patch.expected_revision||bodyHash(old.body)!==patch.expected_body_sha256||JSON.stringify(old.body.tags)!==JSON.stringify(patch.expected_tags))throw Error('Tag CAS/body guard differs');}
 const db=new PGlite();let manifestMd5;try{manifestMd5=(await db.query('select md5($1::jsonb::text) h',[JSON.stringify(manifest)])).rows[0].h;}finally{await db.close();}
 return `-- Exact reviewed package-2 confirmed subset: 10 new metadata records + 6 additive tag edits.
-- Existing operator maintenance; no app impersonation, app-RPC retry, schema, grants, RLS or Storage changes.
-- One DO statement is atomic. Failed inserts can consume sequence numbers; never reset/reuse them.
DO $package02_confirmed_bank$
DECLARE
 manifest jsonb := ${json(manifest)};
 fn jsonb; item jsonb; metadata_body jsonb; stored jsonb; current_row public.problem_catalog%rowtype;
 before_rows jsonb; row_before jsonb; record_now record; new_id text; new_number bigint; change_id_text text;
 created_ids text[] := '{}'; changed_ids text[] := '{}'; history_ids text[] := '{}';
 expected_tags jsonb; snapshot jsonb; authority jsonb; seq_before bigint; seq_called boolean;
BEGIN
 PERFORM set_config('lock_timeout','5s',true);
 IF auth.uid() IS NOT NULL OR NOT pg_has_role(current_user,(SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE') THEN RAISE EXCEPTION 'Existing unimpersonated owner authority required'; END IF;
 PERFORM pg_advisory_xact_lock(72483160);
 LOCK TABLE public.problem_catalog IN SHARE ROW EXCLUSIVE MODE;
 LOCK TABLE public.problem_changes IN SHARE ROW EXCLUSIVE MODE;
 IF md5(manifest::text)<>${lit(manifestMd5)} OR jsonb_array_length(manifest->'new_records')<>10 OR jsonb_array_length(manifest->'tag_patches')<>6 THEN RAISE EXCEPTION 'Reviewed manifest differs'; END IF;
 IF (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count} OR (${catalogHashSql}) IS DISTINCT FROM ${lit(g.catalog_fingerprint)} THEN RAISE EXCEPTION 'Catalog baseline drift'; END IF;
 IF (SELECT count(*) FROM public.problem_changes)<>${g.history_count} OR (${historyHashSql}) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'History baseline drift'; END IF;
 SELECT last_value,is_called INTO seq_before,seq_called FROM public.problem_number_seq;
 IF seq_before<>${g.sequence.last_value} OR seq_called IS DISTINCT FROM true THEN RAISE EXCEPTION 'Sequence drift'; END IF;
 IF (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Source registry drift'; END IF;
 IF EXISTS(SELECT 1 FROM pg_trigger WHERE tgrelid IN('public.problem_catalog'::regclass,'public.problem_changes'::regclass) AND NOT tgisinternal) THEN RAISE EXCEPTION 'Unreviewed catalog/history trigger'; END IF;
 FOR fn IN SELECT value FROM jsonb_array_elements(${json(functions)}) LOOP
  IF md5(pg_get_functiondef(to_regprocedure('public.'||(fn->>'signature')))) IS DISTINCT FROM fn->>'definition_md5' OR (SELECT proacl::text FROM pg_proc WHERE oid=to_regprocedure('public.'||(fn->>'signature'))) IS DISTINCT FROM fn->>'acl' THEN RAISE EXCEPTION 'Installed function/ACL drift'; END IF;
 END LOOP;
 snapshot:=(${protectedSql});authority:=(${authoritySql});
 IF snapshot IS DISTINCT FROM ${json(g.protected)} OR authority IS DISTINCT FROM ${json(g.authority)} THEN RAISE EXCEPTION 'Protected state/authority drift'; END IF;
 SELECT jsonb_object_agg(problem_id,to_jsonb(c)) INTO before_rows FROM public.problem_catalog c;
 -- Validate the entire exact new-only allowlist and every additive edit before allocating numbers.
 FOR item IN SELECT value FROM jsonb_array_elements(manifest->'new_records') LOOP
  IF item->'body' ?| ARRAY['id','number','pack','hints','hintsEn','lesson','statement','editorial','editorialUrl'] THEN RAISE EXCEPTION 'Only unassigned problem metadata allowed'; END IF;
  metadata_body:=public.validate_learning_problem(item->'body');
  IF metadata_body->>'source' NOT IN('IOI','EGOI') OR metadata_body->>'ratingKind'<>'estimated' OR metadata_body->>'priorityLevel' NOT IN('low','medium','high') OR nullif(btrim(metadata_body->>'priorityReason'),'') IS NULL OR nullif(btrim(metadata_body->>'ratingBasis'),'') IS NULL OR nullif(btrim(metadata_body->>'ratingSource'),'') IS NULL OR nullif(btrim(metadata_body->>'ratingEstimatedAt'),'') IS NULL OR metadata_body->>'ratingConfidence'<>'rough' OR (metadata_body->>'priority')::boolean IS DISTINCT FROM (metadata_body->>'priorityLevel'='high') THEN RAISE EXCEPTION 'Required curated metadata/provenance missing'; END IF;
  IF NOT EXISTS(SELECT 1 FROM public.problem_sources WHERE name=metadata_body->>'source') THEN RAISE EXCEPTION 'Source not installed'; END IF;
  IF NOT EXISTS(SELECT 1 FROM jsonb_array_elements_text(metadata_body->'tags') WHERE value IN('interactive','communication')) THEN RAISE EXCEPTION 'Type metadata invalid'; END IF;
  IF EXISTS(SELECT 1 FROM public.problem_catalog c WHERE (lower(c.body->>'source')=lower(metadata_body->>'source') AND (regexp_replace(lower(c.body->>'ref'),'[^a-z0-9]','','g') IN(SELECT jsonb_array_elements_text(item->'canonical_refs')) OR regexp_replace(lower(regexp_replace(rtrim(split_part(split_part(c.body->>'url','?',1),'#',1),'/'),'^.*/','')),'[^a-z0-9]','','g') IN(SELECT jsonb_array_elements_text(item->'canonical_refs')))) OR lower(rtrim(split_part(split_part(c.body->>'url','?',1),'#',1),'/'))=lower(rtrim(metadata_body->>'url','/'))) THEN RAISE EXCEPTION 'Existing or archived canonical identity conflict'; END IF;
 END LOOP;
 IF EXISTS(SELECT 1 FROM jsonb_array_elements(manifest->'new_records') r GROUP BY r->'identity' HAVING count(*)>1) THEN RAISE EXCEPTION 'Duplicate new identity'; END IF;
 FOR item IN SELECT value FROM jsonb_array_elements(manifest->'tag_patches') LOOP
  SELECT * INTO current_row FROM public.problem_catalog WHERE problem_id=item->>'id' FOR UPDATE;
  row_before:=before_rows->(item->>'id');
  IF NOT FOUND OR current_row.archived OR current_row.number<>(item->>'number')::bigint OR current_row.revision<>(item->>'expected_revision')::integer OR current_row.body->'tags' IS DISTINCT FROM item->'expected_tags' OR jsonb_array_length(item->'remove_tags')<>0 THEN RAISE EXCEPTION 'Tag CAS/body drift'; END IF;
  expected_tags:=current_row.body->'tags';
  FOR metadata_body IN SELECT value FROM jsonb_array_elements(item->'add_tags') LOOP
   IF metadata_body#>>'{}' NOT IN('interactive','communication') OR expected_tags @> jsonb_build_array(metadata_body) THEN RAISE EXCEPTION 'Only missing type tags may be appended'; END IF;
   expected_tags:=expected_tags||jsonb_build_array(metadata_body);
  END LOOP;
  PERFORM public.validate_learning_problem(current_row.body||jsonb_build_object('tags',expected_tags));
 END LOOP;
 FOR item IN SELECT value FROM jsonb_array_elements(manifest->'new_records') LOOP
  metadata_body:=public.validate_learning_problem(item->'body');new_number:=nextval('public.problem_number_seq');new_id:='task-'||new_number::text;
  stored:=metadata_body||jsonb_build_object('id',new_id,'number',new_number,'pack',CASE WHEN metadata_body->>'source'='EGOI' THEN 'egoi' ELSE 'advanced' END,'hints','[]'::jsonb,'hintsEn','[]'::jsonb,'lesson','');
  INSERT INTO public.problem_catalog(problem_id,number,body,revision,archived) VALUES(new_id,new_number,stored,1,false);
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(new_id,NULL,'create',NULL,stored) RETURNING change_id::text INTO change_id_text;
  created_ids:=array_append(created_ids,new_id);history_ids:=array_append(history_ids,change_id_text);
  IF NOT EXISTS(SELECT 1 FROM public.problem_catalog WHERE problem_id=new_id AND body=stored AND number=new_number AND revision=1 AND NOT archived) THEN RAISE EXCEPTION 'Inserted metadata differs'; END IF;
  -- Atomic new record and create history complete.
 END LOOP;
 FOR item IN SELECT value FROM jsonb_array_elements(manifest->'tag_patches') LOOP
  SELECT * INTO current_row FROM public.problem_catalog WHERE problem_id=item->>'id';expected_tags:=(current_row.body->'tags')||(item->'add_tags');stored:=current_row.body||jsonb_build_object('tags',expected_tags);
  UPDATE public.problem_catalog SET body=stored,revision=revision+1,updated_at=now() WHERE problem_id=current_row.problem_id AND revision=current_row.revision AND body=current_row.body;
  IF NOT FOUND THEN RAISE EXCEPTION 'Concurrent tag change'; END IF;
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(current_row.problem_id,NULL,'edit',current_row.body,stored) RETURNING change_id::text INTO change_id_text;
  changed_ids:=array_append(changed_ids,current_row.problem_id);history_ids:=array_append(history_ids,change_id_text);
  -- Atomic additive tag edit and history complete.
 END LOOP;
 FOR record_now IN SELECT * FROM public.problem_catalog WHERE NOT(problem_id=ANY(created_ids)) LOOP
  row_before:=before_rows->record_now.problem_id;
  IF record_now.problem_id=ANY(changed_ids) THEN
   SELECT value INTO item FROM jsonb_array_elements(manifest->'tag_patches') WHERE value->>'id'=record_now.problem_id;
   IF record_now.body IS DISTINCT FROM (row_before->'body')||jsonb_build_object('tags',(row_before->'body'->'tags')||(item->'add_tags')) OR record_now.revision<>(row_before->>'revision')::integer+1 OR (to_jsonb(record_now)-'body'-'revision'-'updated_at') IS DISTINCT FROM (row_before-'body'-'revision'-'updated_at') THEN RAISE EXCEPTION 'Unrelated patched fields changed'; END IF;
  ELSIF to_jsonb(record_now) IS DISTINCT FROM row_before THEN RAISE EXCEPTION 'Unrelated existing row changed'; END IF;
 END LOOP;
 IF (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count+10} OR cardinality(created_ids)<>10 OR cardinality(changed_ids)<>6 OR (SELECT last_value FROM public.problem_number_seq)<>seq_before+10 OR (SELECT count(*) FROM public.problem_changes)<>${g.history_count+16} OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) FROM public.problem_changes h WHERE NOT(change_id::text=ANY(history_ids))) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'Catalog/history/count preservation failed'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM snapshot OR (${authoritySql}) IS DISTINCT FROM authority OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Protected state or authority changed'; END IF;
END
$package02_confirmed_bank$;
`;
}
