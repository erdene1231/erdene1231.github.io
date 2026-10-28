// Generates SQL only for explicitly named, reviewed core-practice promotions per batch; no imports/access changes.
import {bodyHash} from './package02_tutorial_proposals.mjs';
const literal=v=>"E'"+String(v).replace(/\\/g,'\\\\').replace(/'/g,"''")+"'";
const json=v=>literal(JSON.stringify(v))+'::jsonb';
export function complexityPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1083','cses-1094']);}
export function maskPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['atcoder-dp_o']);}
export function methodologyPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1628','task-106']);}
export function combinatoricsPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1715']);}
export function monotonicPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1142']);}
export function boundsPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1073']);}
export function sparsePrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1647']);}
export function intervalHeapPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['atcoder-dp_n','cses-1164']);}
export function treeGridPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1638','cses-1674']);}
export function answerPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['task-95']);}
export function powerPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1095']);}
export function bitsPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-2205']);}
export function stackPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['task-101']);}
export function windowPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1660']);}
export function differencePointersPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1619','cses-1640']);}
export function recursionPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-2165']);}
export function searchSortPrioritySql(plan,guard){return buildPrioritySql(plan,guard,['cses-1621','cses-1623']);}
function buildPrioritySql(plan,guard,allowedIds){
 const ids=plan.patches.map(p=>p.id).sort();
 if(JSON.stringify(ids)!==JSON.stringify(allowedIds))throw Error('Only the reviewed core practice allowlist is allowed');
 const scope='('+ids.map(literal).join(',')+')';
 const rows=plan.patches.map(p=>{
  const old=guard.problems.find(r=>r.problem_id===p.id);
  if(!old||old.archived||old.number!==p.number||old.revision!==p.expected_revision||bodyHash(old.body)!==p.expected_body_sha256||!/^[a-f0-9]{32}$/.test(old.body_md5))throw Error('Fresh priority body/revision guard mismatch');
  if(JSON.stringify(Object.keys(p.changes).sort())!==JSON.stringify(['priority','priorityLevel','priorityReason'])||p.changes.priority!==true||p.changes.priorityLevel!=='high'||typeof p.changes.priorityReason!=='string'||p.changes.priorityReason.length<60||p.changes.priorityReason.length>1000)throw Error('Only justified priority metadata may change');
  return{...p,expected_body_md5:old.body_md5};
 });
 if(guard.problem_count!==993||guard.sequence.last_value!==993||guard.sequence.is_called!==true||guard.functions.length!==2||guard.catalog_triggers!==null||!/^[a-f0-9]{32}$/.test(guard.non_target_fingerprint)||!/^[a-f0-9]{32}$/.test(guard.history_fingerprint))throw Error('Fresh scoped priority guards required');
 if(JSON.stringify(guard.functions.map(f=>f.signature).sort())!==JSON.stringify(['validate_learning_problem(jsonb)','validate_priority_metadata(jsonb)']))throw Error('Exact installed metadata validators required');
 const sql=`-- Package 2 C13/C14: ${ids.length} existing core-practice priority promotion(s) only.
DO $package02_complexity_priority$
DECLARE
 targets jsonb := ${json(rows)};
 functions jsonb := ${json(guard.functions)};
 item jsonb; fn jsonb; current_row public.problem_catalog%rowtype; next_body jsonb;
 history_before text; history_count bigint; old_sequence bigint; old_called boolean;
 new_ids text[] := '{}'; new_id text;
BEGIN
 IF auth.uid() IS NOT NULL OR NOT pg_catalog.pg_has_role((SELECT relowner FROM pg_class WHERE oid='public.problem_catalog'::regclass),'USAGE') THEN
  RAISE EXCEPTION 'Existing database owner context without app impersonation required';
 END IF;
 PERFORM pg_advisory_xact_lock(72483160);
 FOR fn IN SELECT value FROM jsonb_array_elements(functions) LOOP
  IF md5(pg_get_functiondef(to_regprocedure('public.'||(fn->>'signature')))) IS DISTINCT FROM fn->>'definition_md5'
   OR (SELECT proacl::text FROM pg_proc WHERE oid=to_regprocedure('public.'||(fn->>'signature'))) IS DISTINCT FROM fn->>'acl' THEN RAISE EXCEPTION 'Metadata function/ACL drift'; END IF;
 END LOOP;
 IF (SELECT count(*) FROM public.problem_catalog)<>993
  OR (SELECT jsonb_agg(pg_get_triggerdef(oid) ORDER BY tgname) FROM pg_trigger WHERE tgrelid='public.problem_catalog'::regclass AND NOT tgisinternal) IS NOT NULL
  OR (SELECT md5(jsonb_agg(to_jsonb(p) ORDER BY problem_id)::text) FROM public.problem_catalog p WHERE problem_id NOT IN${scope}) IS DISTINCT FROM ${literal(guard.non_target_fingerprint)} THEN RAISE EXCEPTION 'Catalog drift'; END IF;
 SELECT last_value,is_called INTO old_sequence,old_called FROM public.problem_number_seq;
 IF old_sequence<>993 OR NOT old_called THEN RAISE EXCEPTION 'Problem sequence drift'; END IF;
 SELECT count(*),md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) INTO history_count,history_before FROM public.problem_changes h;
 IF history_before IS DISTINCT FROM ${literal(guard.history_fingerprint)} THEN RAISE EXCEPTION 'Problem history drift'; END IF;
 FOR item IN SELECT value FROM jsonb_array_elements(targets) ORDER BY value->>'id' LOOP
  SELECT * INTO current_row FROM public.problem_catalog WHERE problem_id=item->>'id' FOR UPDATE;
  IF NOT FOUND OR current_row.archived OR current_row.number<>(item->>'number')::bigint OR current_row.revision<>(item->>'expected_revision')::integer OR md5(current_row.body::text) IS DISTINCT FROM item->>'expected_body_md5' THEN RAISE EXCEPTION 'Priority CAS/body drift'; END IF;
  PERFORM public.validate_learning_problem(current_row.body||(item->'changes'));
 END LOOP;
 FOR item IN SELECT value FROM jsonb_array_elements(targets) ORDER BY value->>'id' LOOP
  SELECT * INTO current_row FROM public.problem_catalog WHERE problem_id=item->>'id';
  next_body:=current_row.body||(item->'changes');
  UPDATE public.problem_catalog SET body=next_body,revision=revision+1,updated_at=now() WHERE problem_id=current_row.problem_id AND revision=current_row.revision AND body=current_row.body;
  IF NOT FOUND THEN RAISE EXCEPTION 'Concurrent priority change'; END IF;
  INSERT INTO public.problem_changes(problem_id,actor_id,action,previous_body,next_body) VALUES(current_row.problem_id,NULL,'edit',current_row.body,next_body) RETURNING change_id::text INTO new_id;
  new_ids:=array_append(new_ids,new_id);
  -- Atomic priority target and edit history complete.
 END LOOP;
 IF (SELECT count(*) FROM public.problem_catalog)<>993
  OR (SELECT md5(jsonb_agg(to_jsonb(p) ORDER BY problem_id)::text) FROM public.problem_catalog p WHERE problem_id NOT IN${scope}) IS DISTINCT FROM ${literal(guard.non_target_fingerprint)}
  OR (SELECT last_value FROM public.problem_number_seq)<>old_sequence OR (SELECT is_called FROM public.problem_number_seq) IS DISTINCT FROM old_called
  OR (SELECT count(*) FROM public.problem_changes)<>history_count+${ids.length}
  OR (SELECT md5(coalesce(jsonb_agg(to_jsonb(h) ORDER BY change_id::text)::text,'[]')) FROM public.problem_changes h WHERE change_id::text<>ALL(new_ids)) IS DISTINCT FROM history_before THEN RAISE EXCEPTION 'Priority preservation failed'; END IF;
 FOR item IN SELECT value FROM jsonb_array_elements(targets) LOOP
  IF NOT EXISTS(SELECT 1 FROM public.problem_catalog WHERE problem_id=item->>'id' AND number=(item->>'number')::bigint AND revision=(item->>'expected_revision')::integer+1 AND NOT archived AND body->>'priorityLevel'='high' AND body->'priority'='true'::jsonb AND body->>'priorityReason'=item->'changes'->>'priorityReason') THEN RAISE EXCEPTION 'Priority verification failed'; END IF;
 END LOOP;
END
$package02_complexity_priority$;
`;
 if(sql.split('$package02_complexity_priority$').length!==3)throw Error('Unsafe priority SQL delimiter');
 return sql;
}
