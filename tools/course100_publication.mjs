// Generates only the three reviewed setup lessons; no network or credentials.
import {bodyHash} from './package02_tutorial_proposals.mjs';
export const setupIds=['cpp-devcpp','cpp-terminal-ioi','cpp-windows-vscode'];
const lit=x=>"E'"+String(x).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'";
const json=x=>lit(JSON.stringify(x))+'::jsonb';
export function setupPublicationSql(bodies,g){
 if(JSON.stringify(bodies.map(b=>b.id).sort())!==JSON.stringify(setupIds)||bodies.some(b=>g.reviewed_hashes?.[b.id]!==bodyHash(b)))throw Error('Exact reviewed setup scope required');
 for(const k of['catalog_fingerprint','all_drafts_fingerprint','protected_fingerprint'])if(!/^[a-f0-9]{32}$/.test(g[k]))throw Error('Fresh preservation guards required');
 if(!Number.isSafeInteger(g.catalog_count)||g.catalog_count<1||g.functions?.length!==7||!g.catalog_triggers?.length)throw Error('Fresh authority guards required');
 const names=['admin_publish_tutorial_draft','admin_save_tutorial','admin_store_learning_tutorial','check_tutorial_media_exists','refresh_tutorial_media_references','validate_tutorial_body','validate_tutorial_publication'];
 if(JSON.stringify(g.functions.map(f=>f.signature.split('(')[0].replace(/^public\./,'')).sort())!==JSON.stringify(names)||g.functions.some(f=>!/^public\.[a-z_]+\([a-z ,]*\)$/.test(f.signature)&&!/^[a-z_]+\([a-z ,]*\)$/.test(f.signature)))throw Error('Exact publication functions required');
 const ids=setupIds.map(lit).join(',');
 return `DO $course_setup$
DECLARE bodies jsonb:=${json(bodies)}; b jsonb; fn jsonb; history_before text; history_count bigint; history_limit bigint;
BEGIN
 IF auth.uid() IS NOT NULL OR NOT pg_catalog.pg_has_role((SELECT relowner FROM pg_class WHERE oid='public.tutorial_catalog'::regclass),'USAGE') THEN RAISE EXCEPTION 'Existing owner context required'; END IF;
 PERFORM pg_advisory_xact_lock(72483161);
 LOCK TABLE public.tutorial_catalog IN SHARE ROW EXCLUSIVE MODE;
 IF EXISTS(SELECT 1 FROM public.tutorial_catalog WHERE id IN(${ids})) OR EXISTS(SELECT 1 FROM public.tutorial_deleted_ids WHERE id IN(${ids})) OR EXISTS(SELECT 1 FROM public.tutorial_changes WHERE tutorial_id IN(${ids})) OR EXISTS(SELECT 1 FROM public.tutorial_drafts WHERE tutorial_id IN(${ids})) THEN RAISE EXCEPTION 'Setup identity used; inspect, never replay'; END IF;
 IF (SELECT count(*) FROM public.tutorial_catalog)<>${g.catalog_count} OR (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t) IS DISTINCT FROM ${lit(g.catalog_fingerprint)} THEN RAISE EXCEPTION 'Catalog drift'; END IF;
 IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM ${lit(g.all_drafts_fingerprint)} THEN RAISE EXCEPTION 'Draft drift'; END IF;
 FOR fn IN SELECT value FROM jsonb_array_elements(${json(g.functions)}) LOOP
 IF md5(pg_get_functiondef(to_regprocedure(fn->>'signature'))) IS DISTINCT FROM fn->>'definition_md5' OR (SELECT proacl::text FROM pg_proc WHERE oid=to_regprocedure(fn->>'signature')) IS DISTINCT FROM fn->>'acl' THEN RAISE EXCEPTION 'Function/ACL drift'; END IF;
 END LOOP;
 IF (SELECT jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgname) FROM pg_trigger WHERE tgrelid='public.tutorial_catalog'::regclass AND NOT tgisinternal) IS DISTINCT FROM ${json(g.catalog_triggers)} THEN RAISE EXCEPTION 'Trigger drift'; END IF;
 IF (${g.protected_sql}) IS DISTINCT FROM ${lit(g.protected_fingerprint)} THEN RAISE EXCEPTION 'Protected state drift'; END IF;
 SELECT count(*),coalesce(max(change_id),0),md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id)::text,'[]')) INTO history_count,history_limit,history_before FROM public.tutorial_changes h;
 FOR b IN SELECT value FROM jsonb_array_elements(bodies) LOOP
 PERFORM public.validate_tutorial_body(b->>'id',b);
 PERFORM public.validate_tutorial_publication(b->>'id',b);
 INSERT INTO public.tutorial_catalog(id,body,revision,published,published_at,updated_by) VALUES(b->>'id',b,1,true,now(),NULL);
 INSERT INTO public.tutorial_changes(tutorial_id,actor_id,revision,previous_body,new_body) VALUES(b->>'id',NULL,1,'{}'::jsonb,b);
 END LOOP;
 -- Atomic preservation boundary, including all previous private and public content.
 IF (SELECT count(*) FROM public.tutorial_catalog)<>${g.catalog_count+3} OR (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t WHERE id NOT IN(${ids})) IS DISTINCT FROM ${lit(g.catalog_fingerprint)} THEN RAISE EXCEPTION 'Existing catalog preservation failed'; END IF;
 IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM ${lit(g.all_drafts_fingerprint)} OR (${g.protected_sql}) IS DISTINCT FROM ${lit(g.protected_fingerprint)} THEN RAISE EXCEPTION 'Protected data preservation failed'; END IF;
 IF (SELECT count(*) FROM public.tutorial_changes)<>history_count+3 OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id)::text,'[]')) FROM public.tutorial_changes h WHERE change_id<=history_limit) IS DISTINCT FROM history_before THEN RAISE EXCEPTION 'History preservation failed'; END IF;
 FOR b IN SELECT value FROM jsonb_array_elements(bodies) LOOP
 IF NOT EXISTS(SELECT 1 FROM public.tutorial_catalog WHERE id=b->>'id' AND body=b AND revision=1 AND published AND published_at IS NOT NULL) OR NOT EXISTS(SELECT 1 FROM public.tutorial_changes WHERE tutorial_id=b->>'id' AND new_body=b AND previous_body='{}'::jsonb AND revision=1 AND actor_id IS NULL AND change_id>history_limit) THEN RAISE EXCEPTION 'Exact readback failed'; END IF;
 END LOOP;
END $course_setup$;`;
}
