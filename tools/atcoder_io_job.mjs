// Screenshot-driven formatting only; generates SQL without network/credentials.
import fs from 'node:fs';import crypto from 'node:crypto';
import {PGlite} from '@electric-sql/pglite';
import {bodyHash} from './part04_tutorial_proposals.mjs';
import {protectedSql,authoritySql,catalogHashSql,historyHashSql,preflightSql} from './package02_confirmed_bank_job.mjs';
export {preflightSql};
const raw=fs.readFileSync(new URL('../audit/atcoder-io-format/patches.json',import.meta.url),'utf8');
export const patches=JSON.parse(raw),reviewedHash='45065d2498f61d1dc8baa2f4abea3ef3f06e62edc041f12ec2645a708e08f6c8';
if(crypto.createHash('sha256').update(raw).digest('hex')!==reviewedHash)throw Error('Reviewed I/O plan hash differs');
export function applyIoChanges(doc,changes){const result=structuredClone(doc);for(const c of changes){let block=result;for(const k of c.path.slice(0,-1))block=block[k];if(c.path.at(-1)!=='language'||block.type!=='code'||block.language!==c.before||!['Input','Output'].includes(c.after))throw Error('Native subtype path differs');block.language=c.after;}return result;}
export async function buildIoJob(g,plan=patches){
 if(JSON.stringify(plan)!==JSON.stringify(patches)||plan.length!==51||plan.reduce((n,p)=>n+p.changes.length,0)!==678)throw Error('Reviewed I/O allowlist differs');
 if(!g.owner_catalog||g.authenticated_app_user||g.triggers!==null)throw Error('Fresh unimpersonated owner/trigger baseline required');
 const db=new PGlite(),items=[];let hash;
 try{for(const p of plan){const row=g.problems.find(r=>r.problem_id===p.id);if(!row||row.archived||row.number!==p.number||row.revision!==p.expected_revision||bodyHash(row.body)!==p.expected_body_sha256||bodyHash(row.body.statement)!==p.expected_statement_sha256)throw Error('Fresh I/O target CAS differs');
  const doc=applyIoChanges(row.body.statement,p.changes);if(bodyHash(doc)!==p.after_statement_sha256||JSON.stringify(doc)!==JSON.stringify(p.after_statement))throw Error('Only reviewed subtype changes allowed');
  const beforeMd5=(await db.query('select md5($1::jsonb::text) h',[JSON.stringify(row.body)])).rows[0].h;if(beforeMd5!==row.body_md5)throw Error('PostgreSQL JSON body representation differs');
  const afterMd5=(await db.query('select md5($1::jsonb::text) h',[JSON.stringify({...row.body,statement:doc})])).rows[0].h;
  items.push({id:p.id,number:p.number,revision:p.expected_revision,body_md5:row.body_md5,after_body_md5:afterMd5,changes:p.changes.map(c=>({path:c.path,before:c.before,after:c.after}))});
 }hash=(await db.query('select md5($1::jsonb::text) h',[JSON.stringify(items)])).rows[0].h;}finally{await db.close();}
 return `-- Exact native code subtype-only plan SHA256 ${reviewedHash}.
-- One atomic statement; never replay after submission without outcome inspection.
DO $atcoder_io$
DECLARE items jsonb:=${json(items)}; item jsonb; change jsonb; path text[]; old public.problem_catalog%rowtype; stored jsonb; before_rows jsonb; row_now record; before_row jsonb;
 edited_ids text[]:='{}'; history_ids bigint[]:='{}'; hid bigint; changed_blocks integer:=0;
BEGIN
 PERFORM set_config('lock_timeout','5s',true);
 IF auth.uid() IS NOT NULL OR NOT pg_has_role(current_user,(SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE') THEN RAISE EXCEPTION 'Unimpersonated owner required'; END IF;
 PERFORM pg_advisory_xact_lock(72483160);LOCK TABLE public.problem_catalog,public.problem_changes IN SHARE ROW EXCLUSIVE MODE;
 IF md5(items::text)<>${lit(hash)} OR jsonb_array_length(items)<>51 THEN RAISE EXCEPTION 'Reviewed subtype allowlist differs'; END IF;
 IF (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count} OR (${catalogHashSql}) IS DISTINCT FROM ${lit(g.catalog_fingerprint)} THEN RAISE EXCEPTION 'Catalog baseline drift'; END IF;
 IF (SELECT count(*) FROM public.problem_changes)<>${g.history_count} OR (${historyHashSql}) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'History baseline drift'; END IF;
 IF EXISTS(SELECT 1 FROM pg_trigger WHERE tgrelid IN('public.problem_catalog'::regclass,'public.problem_changes'::regclass) AND NOT tgisinternal) THEN RAISE EXCEPTION 'Unreviewed trigger'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM ${json(g.protected)} OR (${authoritySql}) IS DISTINCT FROM ${json(g.authority)} THEN RAISE EXCEPTION 'Protected state/authority drift'; END IF;
 IF (SELECT jsonb_build_object('last_value',last_value,'is_called',is_called) FROM public.problem_number_seq) IS DISTINCT FROM ${json(g.sequence)} OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Allocator/source drift'; END IF;
 SELECT jsonb_object_agg(problem_id,to_jsonb(p)) INTO before_rows FROM public.problem_catalog p;
 FOR item IN SELECT value FROM jsonb_array_elements(items) LOOP
  SELECT * INTO old FROM public.problem_catalog WHERE problem_id=item->>'id' FOR UPDATE;
  IF old.problem_id IS NULL OR old.archived OR old.number<>(item->>'number')::bigint OR old.revision<>(item->>'revision')::integer OR md5(old.body::text) IS DISTINCT FROM item->>'body_md5' THEN RAISE EXCEPTION 'Subtype target CAS drift'; END IF;
  stored:=old.body;
  FOR change IN SELECT value FROM jsonb_array_elements(item->'changes') LOOP
   SELECT array_agg(v ORDER BY n) INTO path FROM jsonb_array_elements_text(change->'path') WITH ORDINALITY x(v,n);
   IF path[array_length(path,1)]<>'language' OR stored#>>(ARRAY['statement']||path) IS DISTINCT FROM change->>'before' OR stored#>>(ARRAY['statement']||path[1:array_length(path,1)-1]||ARRAY['type'])<>'code' OR change->>'after' NOT IN('Input','Output') THEN RAISE EXCEPTION 'Native code subtype path differs'; END IF;
   stored:=jsonb_set(stored,ARRAY['statement']||path,change->'after',false);changed_blocks:=changed_blocks+1;
  END LOOP;
  IF md5(stored::text) IS DISTINCT FROM item->>'after_body_md5' THEN RAISE EXCEPTION 'Exact formatting-only body mismatch'; END IF;
  PERFORM public.validate_native_problem_statement(stored->'statement',stored->'statementProvenance');
  UPDATE public.problem_catalog SET body=stored,revision=revision+1,updated_at=now() WHERE problem_id=old.problem_id AND revision=old.revision AND body=old.body;
  IF NOT FOUND THEN RAISE EXCEPTION 'Subtype CAS failed'; END IF;
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(old.problem_id,NULL,'edit',old.body,stored) RETURNING change_id INTO hid;
  edited_ids:=array_append(edited_ids,old.problem_id);history_ids:=array_append(history_ids,hid);
  -- Atomic native subtype edit and history complete.
 END LOOP;
 FOR row_now IN SELECT * FROM public.problem_catalog LOOP
  before_row:=before_rows->row_now.problem_id;
  IF row_now.problem_id=ANY(edited_ids) THEN
   SELECT value INTO item FROM jsonb_array_elements(items) WHERE value->>'id'=row_now.problem_id;
   IF to_jsonb(row_now)-ARRAY['body','revision','updated_at'] IS DISTINCT FROM before_row-ARRAY['body','revision','updated_at'] OR row_now.revision<>(before_row->>'revision')::integer+1 OR md5(row_now.body::text) IS DISTINCT FROM item->>'after_body_md5' OR NOT EXISTS(SELECT 1 FROM public.problem_changes WHERE change_id=ANY(history_ids) AND problem_id=row_now.problem_id AND actor_id IS NULL AND action='edit' AND previous_body=before_row->'body' AND next_body=row_now.body) THEN RAISE EXCEPTION 'Subtype field/history scope failed'; END IF;
  ELSIF to_jsonb(row_now) IS DISTINCT FROM before_row THEN RAISE EXCEPTION 'Unrelated problem changed'; END IF;
 END LOOP;
 IF cardinality(edited_ids)<>51 OR changed_blocks<>678 OR (SELECT count(*) FROM public.problem_catalog)<>${g.problem_count} OR (SELECT count(*) FROM public.problem_changes)<>${g.history_count}+51 OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) FROM public.problem_changes h WHERE NOT(change_id=ANY(history_ids))) IS DISTINCT FROM ${lit(g.history_fingerprint)} THEN RAISE EXCEPTION 'Catalog/history preservation failed'; END IF;
 IF (${protectedSql}) IS DISTINCT FROM ${json(g.protected)} OR (${authoritySql}) IS DISTINCT FROM ${json(g.authority)} OR (SELECT jsonb_build_object('last_value',last_value,'is_called',is_called) FROM public.problem_number_seq) IS DISTINCT FROM ${json(g.sequence)} OR (SELECT md5(jsonb_agg(name ORDER BY name)::text) FROM public.problem_sources) IS DISTINCT FROM ${lit(g.source_fingerprint)} THEN RAISE EXCEPTION 'Protected postcondition failed'; END IF;
END $atcoder_io$;\n`;
}
const lit=v=>"E'"+String(v).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'",json=v=>lit(JSON.stringify(v))+'::jsonb';
