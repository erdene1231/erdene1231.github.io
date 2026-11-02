// Narrow owner-requested MN terminology edit; executable content is immutable.
import {ownerReviewedLessonsSql} from './package02_reviewed_publication.mjs';
import {bodyHash} from './package02_tutorial_proposals.mjs';
export const introductionTermPaths=[['title'],['sections',0,'blocks',0,'text'],['sections',4,'blocks',0,'text'],['sections',5,'blocks',10,'text']];
const get=(x,path)=>path.reduce((v,k)=>v[k],x);
export function correctIntroduction(before){
 if(before.id!=='introduction')throw Error('Introduction only');
 const after=structuredClone(before);
 for(const path of introductionTermPaths){const old=get(before,path);if(typeof old!=='string'||!/тэмцээний программчлал/i.test(old))throw Error('Expected exact terminology context changed');const parent=get(after,path.slice(0,-1));parent[path.at(-1)]=old.replace(/тэмцээний программчлал/g,'өрсөлдөөнт программчлал').replace(/Тэмцээний программчлал/g,'Өрсөлдөөнт программчлал');}
 return after;
}
export function introductionTermSql(target,before,g){
 const after=correctIntroduction(before);
 if(target.id!=='introduction'||bodyHash(after)!==target.reviewed_body_sha256||bodyHash(target.body)!==bodyHash(after))throw Error('Exact four-field reviewed introduction required');
 if(!/^[a-f0-9]{32}$/.test(g.catalog_fingerprint)||!/^[a-f0-9]{32}$/.test(g.all_drafts_fingerprint)||!/^[a-f0-9]{32}$/.test(g.protected_fingerprint))throw Error('Fresh preservation guards required');
 let sql=ownerReviewedLessonsSql({targets:[target]},{...g,scope_ids:['introduction']});
 const lock='    PERFORM pg_catalog.pg_advisory_xact_lock(72483161);',end='END\n$package02_owner_publish$;';
 const check=`    IF (SELECT md5(jsonb_agg(to_jsonb(t) ORDER BY id)::text)FROM public.tutorial_catalog t) IS DISTINCT FROM '${g.catalog_fingerprint}' THEN RAISE EXCEPTION 'Complete catalog drift';END IF;\n`;
 const preserve=`    IF (SELECT md5(coalesce(jsonb_agg(to_jsonb(d) ORDER BY tutorial_id,editor_id)::text,'[]'))FROM public.tutorial_drafts d)IS DISTINCT FROM '${g.all_drafts_fingerprint}' OR (${g.protected_sql})IS DISTINCT FROM '${g.protected_fingerprint}' THEN RAISE EXCEPTION 'Protected state changed';END IF;\n`;
 if(sql.split(lock).length!==2||sql.split(end).length!==2)throw Error('Reviewed publication contract changed');
 return sql.replace(lock,lock+'\n    LOCK TABLE public.tutorial_catalog IN SHARE ROW EXCLUSIVE MODE;\n'+check+preserve).replace(end,preserve+end);
}
