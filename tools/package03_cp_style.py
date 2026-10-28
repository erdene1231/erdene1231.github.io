"""Local, scope-limited identifier refactoring; never submits SQL or accesses credentials."""
import copy, hashlib, json, re
from pathlib import Path

# Strings, comments and preprocessor lines are opaque. No regex changes to C++ literals.
TOKEN = re.compile(r'^[ \t]*\#[^\n]*|//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\b[A-Za-z_]\w*\b', re.M)
IDENT = re.compile(r'^[A-Za-z_]\w*$')
COMMON = [
 ('vertex_count','n'),('edge_count','m'),('query_count','q'),('queryCount','q'),
 ('item_count','n'),('value_count','n'),('student_count','n'),('machine_count','n'),
 ('command_count','q'),('update_count','q'),('state_count','states'),('used_count','used'),
 ('values','a'),('graph','adj'),('distance','dist'),('parent','par'),('middle','mid'),
 ('low','l'),('high','r'),('left','l'),('right','r'),('index','i'),('count','n'),
 ('frequency','freq'),('difference','diff'),('representatives','reps'),
 ('current_distance','d'),('destination','to'),('weight','w'),('candidate','nd'),
 ('DisjointSets','DSU'),('component_size','get_size'),('AncestorTable','LCA'),
 ('SparseMinimum','SparseTable'),('SegmentTree','SegTree'),('original_index','pos'),
 ('query_left','ql'),('query_right','qr'),('pending_add','add'),('pending_set','set'),
 ('next_index','pos'),('start_column','start_col'),('next_column','next_col'),
 ('column_step','dc'),('row_step','dr'),('current','cur'),('predecessor','prev'),
 ('shortest_distances','dijkstra'),('shortest_paths','bellman_ford'),
 ('all_pairs_distances','floyd_warshall'),('depth_first_forest','dfs_forest'),
 ('count_independent_sets','count_sets'),('minimum_merge_cost','merge_cost'),
 ('minimum_difference','min_diff'),('minimum_tree','mst'),('increasing_length','lis'),
 ('greatest_divisor','gcd'),('least_multiple','lcm'),('modular_power','mod_pow'),
 ('inverse_factorial','inv_fact'),('factorial','fact'),('build_smallest_factor','build_spf'),
 ('smallest_factor','spf'),('count_divisors','divisors'),('count_members','popcount'),
 ('required_moves','moves'),('move_tower','hanoi'),('last_finish','last_end'),
 ('ends_earlier','by_end'),('max_sessions','max_movies'),('best_value','knapsack'),
 ('smallest_missing_sum','missing_sum'),('count_target_windows','count_windows'),
 ('count_assignments','count_matchings'),('nearest_smaller_left','nearest_smaller'),
 ('counterexample','example'),('random_cases','tests'),('possibilities','cases'),
 ('count_buggy_demo','buggy'),('check_case','check'),('count_brute','brute'),
 ('count_fast','fast'),('selected_sum','sum'),('inspect_subsets','search'),
 ('first_at_least','lower_bound_pos'),('first_not_less','lower_bound_pos'),
 ('first_greater','upper_bound_pos'),('can_produce','enough'),('minimum_time','min_time'),
 ('left_values','left_a'),('right_values','right_a'),('left_sums','left_sum'),
 ('right_sums','right_sum'),('component_representatives','find_reps'),
]

def rename(code, mapping):
    return TOKEN.sub(lambda m: mapping.get(m[0], m[0]) if IDENT.fullmatch(m[0]) else m[0], code)

def identifiers(code):
    return {m[0] for m in TOKEN.finditer(code) if IDENT.fullmatch(m[0])}

def stable_hash(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def code_blocks(doc):
    return [b for s in doc.get('sections',[]) for b in s.get('blocks',[]) if b.get('type')=='code' and b.get('language')=='C++17']

def mapping_for(doc):
    tokens=set().union(*(identifiers(b['text']) for b in code_blocks(doc)))
    out={};used=set()
    for old,new in COMMON:
        if old in tokens and new not in tokens and new not in used:
            out[old]=new;used.add(new)
    # If n/i already have a different role, use readable short alternatives.
    for old,new in [('query_count','queries'),('queryCount','queries'),('index','idx'),('count','cnt')]:
        if old in tokens and old not in out and new not in tokens and new not in used:
            out[old]=new;used.add(new)
    return out

def transform(body,mapping):
    out=copy.deepcopy(body)
    def walk_doc(doc):
        for sec in doc.get('sections',[]):
            for block in sec.get('blocks',[]):
                if block.get('type')=='code':
                    if block.get('language')=='C++17':block['text']=rename(block['text'],mapping)
                    continue  # Input/output are literal test data.
                def walk(value,code=False):
                    if isinstance(value,list):return [walk(x,code) for x in value]
                    if isinstance(value,dict):
                        marked='code' in value.get('marks',[])
                        return {k:walk(v,marked if k=='text' else False) if k not in ['marks','url','path','href','id','key','problemKey'] else v for k,v in value.items()}
                    if isinstance(value,str):
                        if code:return rename(value,mapping)
                        # Preserve ordinary English words. Synchronize explicit math/code
                        # references and unmistakable snake_case/camelCase C++ names only.
                        value=re.sub(r'`[^`\n]+`',lambda m:rename(m[0],mapping),value)
                        value=re.sub(r'\$[^$\n]+\$',lambda m:rename(m[0],mapping),value)
                        safe={k:v for k,v in mapping.items() if '_' in k or any(c.isupper()for c in k)}
                        return re.sub(r'\b[A-Za-z_]\w*\b',lambda m:safe.get(m[0],m[0]),value)
                    return value
                new=walk(block)
                # Three unmarked implementation references in current Mongolian prose.
                def refs(v):
                    if isinstance(v,str):
                        if body['id']=='set-map':v=v.replace('frequency[value]','freq[value]').replace('frequency холбоосууд','freq холбоосууд')
                        if body['id']=='floyd-warshall':v=v.replace('Кодод middle,','Кодод mid,')
                        return v
                    if isinstance(v,list):return [refs(x)for x in v]
                    if isinstance(v,dict):return {k:refs(x)for k,x in v.items()}
                    return v
                new=refs(new);block.clear();block.update(new)
    walk_doc(out)
    if 'en' in out.get('translations',{}):walk_doc(out['translations']['en'])
    return out

def prepare(snapshot,out_dir):
    rows=json.loads(Path(snapshot).read_text())['tutorials'];out_dir=Path(out_dir);out_dir.mkdir(parents=True,exist_ok=True);audit=[]
    for row in rows:
        if row['id']=='mongolia':continue
        mapping=mapping_for(row['body']);body=transform(row['body'],mapping)
        # Metadata, relationships and all other top-level content remain unchanged.
        assert {k:v for k,v in body.items()if k not in ['sections','translations']}=={k:v for k,v in row['body'].items()if k not in ['sections','translations']}
        entry={'id':row['id'],'expected_revision':row['revision'],'expected_published':row['published'],'expected_body_md5':row['body_md5'],'expected_body_sha256':stable_hash(row['body']),'body':body,'mapping':mapping,'changed':body!=row['body']}
        entry['reviewed_body_sha256']=entry['proposed_body_sha256']=stable_hash(body)
        (out_dir/(row['id']+'.json')).write_text(json.dumps(entry,ensure_ascii=False,indent=2)+'\n')
        audit.append({k:entry[k]for k in ['id','expected_revision','mapping','changed']})
    return audit

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--snapshot',required=True);p.add_argument('--out',required=True);args=p.parse_args()
    print(json.dumps(prepare(args.snapshot,args.out),ensure_ascii=False,indent=2))
