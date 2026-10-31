// Read-only preparation and verification for the focused conventional-name pass.
// SQL submission is deliberately separate; each publication uses the existing 1–3 lesson contract.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {bodyHash} from './package02_tutorial_proposals.mjs';
import {ownerReviewedLessonsSql} from './package02_reviewed_publication.mjs';
const dir=new URL('../audit/conventional-names/',import.meta.url);
export const ledger=()=>JSON.parse(fs.readFileSync(new URL('ledger.json',dir)));
export const changes=()=>JSON.parse(fs.readFileSync(new URL('changes.json',dir)));
export const candidate=id=>JSON.parse(fs.readFileSync(new URL(id+'.json',dir))).body;
export function field(object,path){const parts=path.match(/[^.\[\]]+/g);const key=parts.pop();for(const part of parts)object=object[part];return [object,key];}
export function baseline(id){const body=structuredClone(candidate(id));for(const change of changes().filter(x=>x.id===id)){const [o,k]=field(body,change.path);assert.equal(o[k],change.after);o[k]=change.before;}return body;}
export function editorialPublicationSql(batch,guard){
 const reviewed=new Map(ledger().lessons.filter(x=>x.status==='reviewed-changed').map(x=>[x.id,x]));
 for(const t of batch.targets){const entry=reviewed.get(t.id);if(!entry||t.expected_revision!==entry.baseline_revision||t.expected_body_sha256!==entry.baseline_body_sha256||bodyHash(t.body)!==entry.candidate_body_sha256)throw Error('Exact conventional-name review guard failed: '+t.id);}
 for(const k of ['catalog_fingerprint','all_drafts_fingerprint'])if(!/^[a-f0-9]{32}$/.test(guard[k]))throw Error('Fresh complete state guards required');
 const sql=ownerReviewedLessonsSql(batch,guard),lock='    PERFORM pg_catalog.pg_advisory_xact_lock(72483161);',end='END\n$package02_owner_publish$;';
 if(sql.split(lock).length!==2||sql.split(end).length!==2)throw Error('Publication contract changed; review required');
 return sql.replace(lock,`${lock}
    LOCK TABLE public.tutorial_catalog IN SHARE ROW EXCLUSIVE MODE;
    IF (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text) FROM public.tutorial_catalog t) IS DISTINCT FROM '${guard.catalog_fingerprint}' THEN RAISE EXCEPTION 'Catalog drift'; END IF;
    IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM '${guard.all_drafts_fingerprint}' THEN RAISE EXCEPTION 'All private draft drift'; END IF;`).replace(end,`    IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]')) FROM public.tutorial_drafts d) IS DISTINCT FROM '${guard.all_drafts_fingerprint}' THEN RAISE EXCEPTION 'All private draft preservation failed'; END IF;
${end}`);
}
