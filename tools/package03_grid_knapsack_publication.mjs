// Existing reviewed publication contract, narrowed to two stable grid/knapsack lesson IDs.
// Preparation only: no SQL submission, new RPC, migration or permission change.
import{ownerReviewedLessonsSql}from'./package02_reviewed_publication.mjs';
export function gridKnapsackPublicationSql(batch,guard){
 const ids=batch.targets.map(r=>r.id).sort();
 if(JSON.stringify(ids)!==JSON.stringify(['grid-dp','knapsack']))throw Error('Exact grid and knapsack lesson pair required');
 for(const k of['catalog_fingerprint','all_drafts_fingerprint'])if(!/^[a-f0-9]{32}$/.test(guard[k]))throw Error('Fresh complete state guards required');
 const sql=ownerReviewedLessonsSql(batch,guard),lock='    PERFORM pg_catalog.pg_advisory_xact_lock(72483161);',end='END\n$package02_owner_publish$;';
 if(sql.split(lock).length!==2||sql.split(end).length!==2)throw Error('Publication contract changed; review required');
 return sql.replace(lock,`${lock}
    LOCK TABLE public.tutorial_catalog IN SHARE ROW EXCLUSIVE MODE;
    IF (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t) IS DISTINCT FROM '${guard.catalog_fingerprint}' THEN RAISE EXCEPTION 'Catalog drift'; END IF;
    IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM '${guard.all_drafts_fingerprint}' THEN RAISE EXCEPTION 'All private draft drift'; END IF;`).replace(end,`    IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM '${guard.all_drafts_fingerprint}' THEN RAISE EXCEPTION 'All private draft preservation failed'; END IF;
${end}`);
}
