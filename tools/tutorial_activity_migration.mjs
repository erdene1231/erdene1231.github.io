// Scoped040 schema operation; no network, credentials or learner-row writes.
import crypto from'node:crypto';
export const reviewed040Sha='6f4f37dca1169821472f6aa9f3ea1543a819082437f162fd369fbf9fcbd1a98b';
export function activityPreflight(base){
 const end=') AS recovery;';if(!base.endsWith(end))throw Error('Unexpected preflight');
 return base.slice(0,-end.length)+",'policy_fingerprint',(SELECT md5(coalesce(jsonb_agg(to_jsonb(p)ORDER BY schemaname,tablename,policyname)::text,'[]'))FROM pg_policies p WHERE schemaname IN('public','study_private','storage')),'learning_triggers_fingerprint',(SELECT md5(coalesce(jsonb_agg(pg_get_triggerdef(oid)ORDER BY tgname)::text,'[]'))FROM pg_trigger WHERE tgrelid='public.learning_records'::regclass AND NOT tgisinternal)) AS recovery;";
}
const lit=s=>"E'"+String(s).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'";
export function buildActivityMigration(g,preflight,body){
 if(crypto.createHash('sha256').update(body).digest('hex')!==reviewed040Sha)throw Error('Unreviewed040 body');
 if(!g.owner_catalog||g.authenticated_app_user)throw Error('Unimpersonated catalog owner required');
 for(const k of['policy_fingerprint','learning_triggers_fingerprint'])if(!/^[a-f0-9]{32}$/.test(g[k]))throw Error('Fresh040 schema guards required');
 if(!preflight.endsWith(' AS recovery;'))throw Error('Unexpected040 preflight');
 const query=preflight.slice(0,-' AS recovery;'.length)+' INTO state;';
 const keys=['catalog_fingerprint','history_fingerprint','history_count','sequence','protected','source_fingerprint','functions','triggers','policy_fingerprint','learning_triggers_fingerprint'];
 const expected=Object.fromEntries(keys.map(k=>[k,g[k]]));expected.authority_objects=g.authority.objects;expected.authority_functions=g.authority.functions;
 const oldFunctions="SELECT md5(jsonb_agg(jsonb_build_object('signature',p.oid::regprocedure::text,'definition',pg_get_functiondef(p.oid),'acl',p.proacl::text)ORDER BY p.oid::regprocedure::text)::text)FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname IN('public','study_private')AND NOT(n.nspname='public'AND p.proname IN('preserve_tutorial_activity','track_tutorial_activity'))AND p.prokind='f'";
 const oldTriggers="SELECT md5(coalesce(jsonb_agg(pg_get_triggerdef(oid)ORDER BY tgname)::text,'[]'))FROM pg_trigger WHERE tgrelid='public.learning_records'::regclass AND NOT tgisinternal AND tgname NOT IN('erdene_tutorial_activity','erdene_tutorial_activity_preserve')";
 function guard(after){
  const functions=after?'to_jsonb(('+oldFunctions+'))':"state#>'{authority,functions}'",triggers=after?'to_jsonb(('+oldTriggers+'))':"state->'learning_triggers_fingerprint'";
  return `DO $scope$ DECLARE state jsonb;expect jsonb:=${lit(JSON.stringify(expected))}::jsonb;k text;BEGIN ${query}
FOR k IN SELECT jsonb_object_keys(expect)LOOP
 IF k='authority_objects'THEN IF state#>'{authority,objects}'IS DISTINCT FROM expect->k THEN RAISE EXCEPTION '040 object access drift';END IF;
 ELSIF k='authority_functions'THEN IF ${functions}IS DISTINCT FROM expect->k THEN RAISE EXCEPTION '040 unrelated function drift';END IF;
 ELSIF k='learning_triggers_fingerprint'THEN IF ${triggers}IS DISTINCT FROM expect->k THEN RAISE EXCEPTION '040 unrelated learning trigger drift';END IF;
 ELSIF state->k IS DISTINCT FROM expect->k THEN RAISE EXCEPTION '040 data/schema drift: %',k;END IF;
END LOOP;
${after?`IF(SELECT count(*)FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public'AND p.proname IN('preserve_tutorial_activity','track_tutorial_activity')AND NOT p.prosecdef)<>2 THEN RAISE EXCEPTION '040 helpers not invoker';END IF;
IF has_function_privilege('anon','public.track_tutorial_activity()','EXECUTE')OR has_function_privilege('authenticated','public.track_tutorial_activity()','EXECUTE')OR has_function_privilege('anon','public.preserve_tutorial_activity()','EXECUTE')OR has_function_privilege('authenticated','public.preserve_tutorial_activity()','EXECUTE')THEN RAISE EXCEPTION '040 helper access expanded';END IF;
IF(SELECT count(*)FROM pg_trigger WHERE tgrelid='public.learning_records'::regclass AND tgname IN('erdene_tutorial_activity','erdene_tutorial_activity_preserve')AND NOT tgisinternal)<>2 THEN RAISE EXCEPTION '040 intended triggers missing';END IF;`:`IF to_regprocedure('public.preserve_tutorial_activity()')IS NOT NULL OR to_regprocedure('public.track_tutorial_activity()')IS NOT NULL THEN RAISE EXCEPTION '040 already installed or name conflict; inspect';END IF;`}
END $scope$;\n`;
 }
 if(!body.includes('\nbegin;\n')||!body.endsWith('commit;\n'))throw Error('Unexpected040 transaction');
 const inner=body.replace('\nbegin;\n','\n').slice(0,-'commit;\n'.length);
 return "BEGIN;\nSELECT pg_advisory_xact_lock(hashtextextended('erdene-install040-tutorial-activity',0));\nLOCK TABLE public.problem_catalog,public.problem_changes,public.tutorial_catalog,public.tutorial_changes,public.tutorial_drafts,public.progress,public.learning_records,public.profiles IN SHARE MODE;\n"+guard(false)+inner+'--040 guard midpoint: fault injection only in isolated tests.\n'+guard(true)+'COMMIT;\n';
}
