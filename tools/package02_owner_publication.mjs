// Generates a separately reviewed one-off owner maintenance statement. Never submits SQL.
// This is not an app RPC, authentication substitute, migration or permission change.
import {bodyHash} from './package02_tutorial_proposals.mjs';
const literal = value => "E'" + String(value).replace(/\\/g, '\\\\').replace(/'/g, "''") + "'";
const json = value => literal(JSON.stringify(value)) + '::jsonb';

export function ownerPublicationSql(batch, guard) {
    const ids = batch.targets.map(row=>row.id).sort();
    if (JSON.stringify(ids) !== JSON.stringify(['binary-search','dynamic-programming','greedy'])) {
        throw Error('Only the three reviewed foundation lessons are allowed');
    }
    for (const row of batch.targets) {
        if (row.expected_revision !== 5 || row.expected_published !== true || row.body.id !== row.id ||
            bodyHash(row.body) !== row.proposed_body_sha256 || !/^[a-f0-9]{32}$/.test(row.expected_body_md5)) {
            throw Error('Publication payload guard failed: ' + row.id);
        }
    }
    if (!/^[a-f0-9]{32}$/.test(guard.draft_fingerprint) || guard.functions.length !== 7 || !guard.catalog_triggers.length) {
        throw Error('Fresh draft/function/trigger guards are required');
    }
    const expectedFunctions = ['admin_publish_tutorial_draft','admin_save_tutorial','admin_store_learning_tutorial',
        'check_tutorial_media_exists','refresh_tutorial_media_references','validate_tutorial_body','validate_tutorial_publication'].sort();
    const actualFunctions = guard.functions.map(fn=>fn.signature.split('(')[0].replace(/^public\./,'')).sort();
    if (JSON.stringify(actualFunctions)!==JSON.stringify(expectedFunctions)) throw Error('Exact publication function guards required');
    const statement = `-- PROPOSED ONLY. Requires exact owner-maintenance execution authorization.
-- One atomic DO statement; no grants, role claims, DDL, private-draft writes or other content.
DO $package02_owner_publish$
DECLARE
    approved jsonb := ${json(batch.targets)};
    functions jsonb := ${json(guard.functions.map(fn=>({signature:fn.signature.startsWith('public.')?fn.signature:'public.'+fn.signature,definition_md5:fn.definition_md5,acl:fn.acl})))};
    triggers jsonb := ${json(guard.catalog_triggers)};
    target jsonb; fn jsonb; current_row public.tutorial_catalog%rowtype;
    other_before text; drafts_before text; history_before text; history_limit bigint;
    history_count bigint; catalog_count bigint; actual_triggers jsonb;
BEGIN
    IF auth.uid() IS NOT NULL OR NOT pg_catalog.pg_has_role(
        (SELECT relowner FROM pg_catalog.pg_class WHERE oid='public.tutorial_catalog'::regclass),'USAGE') THEN
        RAISE EXCEPTION 'An existing database owner context, without app-user impersonation, is required';
    END IF;
    PERFORM pg_catalog.pg_advisory_xact_lock(72483161);
    FOR fn IN SELECT value FROM jsonb_array_elements(functions) LOOP
        IF md5(pg_catalog.pg_get_functiondef(to_regprocedure(fn->>'signature'))) IS DISTINCT FROM fn->>'definition_md5'
           OR (SELECT proacl::text FROM pg_catalog.pg_proc WHERE oid=to_regprocedure(fn->>'signature')) IS DISTINCT FROM fn->>'acl' THEN
            RAISE EXCEPTION 'Function or ACL drift: %',fn->>'signature';
        END IF;
    END LOOP;
    SELECT jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgname) INTO actual_triggers
      FROM pg_catalog.pg_trigger WHERE tgrelid='public.tutorial_catalog'::regclass AND NOT tgisinternal;
    IF actual_triggers IS DISTINCT FROM triggers THEN RAISE EXCEPTION 'Publication trigger drift'; END IF;
    SELECT count(*) INTO catalog_count FROM public.tutorial_catalog;
    IF catalog_count<>56 THEN RAISE EXCEPTION 'Tutorial inventory drift'; END IF;
    SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) INTO drafts_before
      FROM public.tutorial_drafts d WHERE tutorial_id IN ('binary-search','dynamic-programming','greedy');
    IF drafts_before IS DISTINCT FROM ${literal(guard.draft_fingerprint)} THEN RAISE EXCEPTION 'Private draft changed; reconcile before publication'; END IF;
    SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) INTO other_before FROM public.tutorial_catalog t
      WHERE id NOT IN ('binary-search','dynamic-programming','greedy');
    SELECT coalesce(max(change_id),0),count(*),md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id)::text,'[]'))
      INTO history_limit,history_count,history_before FROM public.tutorial_changes h;
    -- Lock and validate every target before changing any target.
    FOR target IN SELECT value FROM jsonb_array_elements(approved) ORDER BY value->>'id' LOOP
        SELECT * INTO current_row FROM public.tutorial_catalog WHERE id=target->>'id' FOR UPDATE;
        IF NOT FOUND OR current_row.revision<>(target->>'expected_revision')::integer OR NOT current_row.published
           OR md5(current_row.body::text) IS DISTINCT FROM target->>'expected_body_md5' THEN
            RAISE EXCEPTION 'CAS/body/status drift: %',target->>'id';
        END IF;
        PERFORM public.validate_tutorial_body(target->>'id',target->'body');
        PERFORM public.validate_tutorial_publication(target->>'id',target->'body');
    END LOOP;
    FOR target IN SELECT value FROM jsonb_array_elements(approved) ORDER BY value->>'id' LOOP
        SELECT * INTO current_row FROM public.tutorial_catalog WHERE id=target->>'id';
        UPDATE public.tutorial_catalog SET body=target->'body',revision=current_row.revision+1,
            updated_at=now(),published_at=now(),updated_by=NULL
          WHERE id=current_row.id AND revision=current_row.revision AND body=current_row.body;
        IF NOT FOUND THEN RAISE EXCEPTION 'Concurrent tutorial change: %',current_row.id; END IF;
        INSERT INTO public.tutorial_changes(tutorial_id,actor_id,revision,previous_body,new_body)
          VALUES(current_row.id,NULL,current_row.revision+1,current_row.body,target->'body');
        -- Atomic boundary: one target and its history are complete.
    END LOOP;
    IF (SELECT count(*) FROM public.tutorial_catalog)<>catalog_count
       OR (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t
            WHERE id NOT IN ('binary-search','dynamic-programming','greedy')) IS DISTINCT FROM other_before
       OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d
            WHERE tutorial_id IN ('binary-search','dynamic-programming','greedy')) IS DISTINCT FROM drafts_before THEN
        RAISE EXCEPTION 'Unrelated tutorial or private draft preservation failed';
    END IF;
    IF (SELECT count(*) FROM public.tutorial_changes)<>history_count+3
       OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id)::text,'[]')) FROM public.tutorial_changes h WHERE change_id<=history_limit)
            IS DISTINCT FROM history_before THEN RAISE EXCEPTION 'History preservation failed'; END IF;
    FOR target IN SELECT value FROM jsonb_array_elements(approved) LOOP
        IF NOT EXISTS(SELECT 1 FROM public.tutorial_catalog WHERE id=target->>'id' AND revision=6 AND published AND body=target->'body')
           OR NOT EXISTS(SELECT 1 FROM public.tutorial_changes WHERE change_id>history_limit AND tutorial_id=target->>'id'
                         AND revision=6 AND actor_id IS NULL AND new_body=target->'body') THEN
            RAISE EXCEPTION 'Post-publication verification failed: %',target->>'id';
        END IF;
    END LOOP;
END
$package02_owner_publish$;
`;
    // A body cannot terminate the outer DO dollar-quoted block.
    if (statement.split('$package02_owner_publish$').length !== 3) throw Error('Unsafe SQL delimiter in content');
    return statement;
}
