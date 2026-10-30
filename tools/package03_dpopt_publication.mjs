// Preparation only. One new, completed lesson; never submits SQL or changes access.
import {bodyHash} from './package02_tutorial_proposals.mjs';
const lit=x=>"E'"+String(x).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'";
const json=x=>lit(JSON.stringify(x))+'::jsonb';
export function dpoptPublicationSql(candidate, guard) {
 const body=candidate.body;
 if(candidate.id!=='dp-optimizations'||body.id!=='dp-optimizations'||candidate.expected_absent!==true||bodyHash(body)!==candidate.reviewed_body_sha256||candidate.proposed_body_sha256!==candidate.reviewed_body_sha256)throw Error('Exact reviewed dp-optimizations required');
 for(const key of ['catalog_fingerprint','all_drafts_fingerprint'])if(!/^[a-f0-9]{32}$/.test(guard[key]))throw Error('Missing fresh state guard');
 if(!Number.isSafeInteger(guard.catalog_count)||guard.catalog_count<1||guard.functions.length!==7||!guard.catalog_triggers.length)throw Error('Missing inventory/authority guard');
 for(const f of guard.functions)if(!/^[a-f0-9]{32}$/.test(f.definition_md5)||!/^(?:public\.)?[a-z_]+\([a-z ,]*\)$/.test(f.signature))throw Error('Invalid function fingerprint');
 const expected=['admin_publish_tutorial_draft','admin_save_tutorial','admin_store_learning_tutorial','check_tutorial_media_exists','refresh_tutorial_media_references','validate_tutorial_body','validate_tutorial_publication'].sort();
 if(JSON.stringify(guard.functions.map(f=>f.signature.split('(')[0].replace(/^public\./,'')).sort())!==JSON.stringify(expected))throw Error('Exact publication guards required');
 const sql=`-- Atomic content publication under the owner's standing package-3 authority.
-- No app impersonation, DDL, grants, private-draft updates, or existing lesson changes.
DO $dpopt_publish$
DECLARE
 candidate_body jsonb := ${json(body)};
 funcs jsonb := ${json(guard.functions.map(f=>({signature:f.signature.startsWith('public.')?f.signature:'public.'+f.signature,definition_md5:f.definition_md5,acl:f.acl})))};
 triggers jsonb := ${json(guard.catalog_triggers)};
 fn jsonb; actual_triggers jsonb; history_before text; history_limit bigint; history_count bigint;
BEGIN
 IF auth.uid() IS NOT NULL OR NOT pg_catalog.pg_has_role((SELECT relowner FROM pg_class WHERE oid='public.tutorial_catalog'::regclass),'USAGE') THEN RAISE EXCEPTION 'Existing owner context required'; END IF;
 PERFORM pg_advisory_xact_lock(72483161);
 LOCK TABLE public.tutorial_catalog IN SHARE ROW EXCLUSIVE MODE;
 IF EXISTS(SELECT 1 FROM public.tutorial_catalog WHERE id='dp-optimizations') OR EXISTS(SELECT 1 FROM public.tutorial_deleted_ids WHERE id='dp-optimizations') OR EXISTS(SELECT 1 FROM public.tutorial_changes WHERE tutorial_id='dp-optimizations') OR EXISTS(SELECT 1 FROM public.tutorial_drafts WHERE tutorial_id='dp-optimizations') THEN RAISE EXCEPTION 'DP optimizations identity already used; do not replay'; END IF;
 IF (SELECT count(*) FROM public.tutorial_catalog)<>${guard.catalog_count} OR (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t) IS DISTINCT FROM ${lit(guard.catalog_fingerprint)} THEN RAISE EXCEPTION 'Catalog drift'; END IF;
 IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM ${lit(guard.all_drafts_fingerprint)} THEN RAISE EXCEPTION 'Private draft drift'; END IF;
 FOR fn IN SELECT value FROM jsonb_array_elements(funcs) LOOP
  IF md5(pg_get_functiondef(to_regprocedure(fn->>'signature'))) IS DISTINCT FROM fn->>'definition_md5' OR (SELECT proacl::text FROM pg_proc WHERE oid=to_regprocedure(fn->>'signature')) IS DISTINCT FROM fn->>'acl' THEN RAISE EXCEPTION 'Function or ACL drift'; END IF;
 END LOOP;
 SELECT jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgname) INTO actual_triggers FROM pg_trigger WHERE tgrelid='public.tutorial_catalog'::regclass AND NOT tgisinternal;
 IF actual_triggers IS DISTINCT FROM triggers THEN RAISE EXCEPTION 'Trigger drift'; END IF;
 SELECT count(*),coalesce(max(change_id),0),md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id)::text,'[]')) INTO history_count,history_limit,history_before FROM public.tutorial_changes h;
 PERFORM public.validate_tutorial_body('dp-optimizations',candidate_body);
 PERFORM public.validate_tutorial_publication('dp-optimizations',candidate_body);
 INSERT INTO public.tutorial_catalog(id,body,revision,published,published_at,updated_by) VALUES('dp-optimizations',candidate_body,1,true,now(),NULL);
 INSERT INTO public.tutorial_changes(tutorial_id,actor_id,revision,previous_body,new_body) VALUES('dp-optimizations',NULL,1,'{}'::jsonb,candidate_body);
 -- Atomic boundary: catalog and initial history exist together.
 IF (SELECT count(*) FROM public.tutorial_catalog)<>${guard.catalog_count+1} OR (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t WHERE id<>'dp-optimizations') IS DISTINCT FROM ${lit(guard.catalog_fingerprint)} THEN RAISE EXCEPTION 'Existing lesson preservation failed'; END IF;
 IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM ${lit(guard.all_drafts_fingerprint)} THEN RAISE EXCEPTION 'Private draft preservation failed'; END IF;
 IF (SELECT count(*) FROM public.tutorial_changes)<>history_count+1 OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id)::text,'[]')) FROM public.tutorial_changes h WHERE change_id<=history_limit) IS DISTINCT FROM history_before THEN RAISE EXCEPTION 'History preservation failed'; END IF;
 IF NOT EXISTS(SELECT 1 FROM public.tutorial_catalog t WHERE t.id='dp-optimizations' AND t.revision=1 AND t.published AND t.published_at IS NOT NULL AND t.body=candidate_body) THEN RAISE EXCEPTION 'Body postcheck failed'; END IF;
 IF NOT EXISTS(SELECT 1 FROM public.tutorial_changes h WHERE h.change_id>history_limit AND h.tutorial_id='dp-optimizations' AND h.revision=1 AND h.actor_id IS NULL AND h.previous_body='{}'::jsonb AND h.new_body=candidate_body) THEN RAISE EXCEPTION 'History postcheck failed'; END IF;
END
$dpopt_publish$;
`;
 if(sql.split('$dpopt_publish$').length!==3)throw Error('Unsafe SQL content delimiter');return sql;
}
