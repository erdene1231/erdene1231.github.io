import json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];src=ROOT/'audit/package03-work/hld.cpp';rng=random.Random(271828)
with tempfile.TemporaryDirectory()as tmp:
 exe=Path(tmp)/'hld';subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(exe)],check=True)
 def run(n,edges,mode,a,ops):
  adj=[[]for _ in range(n+1)]
  for u,v in edges:adj[u].append(v);adj[v].append(u)
  par=[0]*(n+1);dep=[0]*(n+1);order=[1]
  for u in order:
   for v in adj[u]:
    if v!=par[u]:par[v]=u;dep[v]=dep[u]+1;order.append(v)
  values=a[:];ans=[]
  for op in ops:
   t,u,*rest=op
   if t==1:values[u]=rest[0];continue
   if t==2:
    v=rest[0];left=[];right=[]
    while u!=v:
     if dep[u]>=dep[v]:left.append(u);u=par[u]
     else:right.append(v);v=par[v]
    path=left+[u]+right[::-1]
    ans.append(sum(values[w]for w in path if mode=='V' or w!=u))
   else:
    total=0
    for w in range(1,n+1):
     x=w
     while x and x!=u:x=par[x]
     if x==u and(mode=='V'or w!=u):total+=values[w]
    ans.append(total)
  data=f'{n} {len(ops)} {mode}\n'+ ' '.join(map(str,a[1:]))+'\n'+''.join(f'{u} {v}\n'for u,v in edges)+''.join(' '.join(map(str,op))+'\n'for op in ops)
  p=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True,timeout=15);assert not p.stderr,p.stderr;assert list(map(int,p.stdout.split()))==ans,(n,edges,mode,ops,p.stdout,ans)
  return len(ans)
 cases=queries=0
 for n in range(1,26):
  for shape in ['path','star','random']:
   for mode in ['V','E']:
    edges=[(v-1 if shape=='path'else 1 if shape=='star'else rng.randrange(1,v),v)for v in range(2,n+1)];rng.shuffle(edges)
    a=[0]+[rng.choice([-10**9,10**9,0,rng.randrange(-100,101)])for _ in range(n)]
    ops=[(2,1,1),(2,1,n),(2,n,n),(3,1),(3,n),(1,1,-10**9),(2,1,n),(1,n,10**9),(2,n,1)]
    for _ in range(100):
     t=rng.randrange(1,4);u=rng.randrange(1,n+1);ops.append((t,u,rng.randrange(-10**9,10**9+1))if t==1 else(t,u,rng.randrange(1,n+1))if t==2 else(t,u))
    queries+=run(n,edges,mode,a,ops);cases+=1
 # Large trees: model only a handful of queries, includes sums well above int32.
 for shape in ['path','star']:
  n=200000;edges=[(v-1 if shape=='path'else 1,v)for v in range(2,n+1)]
  # Build stress expected outputs directly to avoid quadratic naive subtree walks.
  for mode in ['V','E']:
   ops=[(2,1,n),(3,1),(2,n,n),(1,n,-10**9),(2,1,n),(3,n)]
   full=n*10**9 if mode=='V'else(n-1)*10**9
   path=(n if shape=='path'else 2)*10**9 if mode=='V'else(n-1 if shape=='path'else 1)*10**9
   expected=[path,full,10**9 if mode=='V'else 0,path-2*10**9,-10**9 if mode=='V'else 0]
   data=f'{n} {len(ops)} {mode}\n'+' '.join(['1000000000']*n)+'\n'+''.join(f'{u} {v}\n'for u,v in edges)+''.join(' '.join(map(str,o))+'\n'for o in ops)
   p=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True,timeout=15);assert not p.stderr;assert list(map(int,p.stdout.split()))==expected
 # Instrument actual mapping: subtree-contiguity, heavy chains, reproducible tie handling and repeated build.
 text=src.read_text().replace('int main() {','int demo_main() {')
 harness='''\nint main() {
 HLD h(9); for (auto [u, v] : vector<pair<int,int>>{{1,2},{1,3},{2,4},{2,5},{4,6},{4,7},{3,8},{8,9}}) h.add(u,v);
 h.build(); auto p=h.pos; h.build(); assert(p==h.pos);
 vector<int> want={0,1,2,7,3,6,4,5,8,9}; assert(h.pos==want);
 for(int u=1;u<=9;u++) for(int v=1;v<=9;v++) {int x=v;while(x&&x!=u)x=h.par[x];assert((x==u)==(h.pos[u]<=h.pos[v]&&h.pos[v]<h.pos[u]+h.sz[u]));}
}\n'''
 h=Path(tmp)/'mapping.cpp';h.write_text(text+harness);subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(h),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True)
report={'status':'passed','Cpp17_UBSan':True,'naive_parent_path_and_subtree_oracles':True,'small_tree_cases':cases,'verified_queries':queries,'vertex_and_edge_modes':True,'point_assignment_negative_and_64bit_sums':True,'max_vertices':200000,'path_star_stress_runs':4,'deep_tree_preprocessing_iterative':True,'mapping_subtree_contiguity_and_repeated_build':True}
(ROOT/'audit/PACKAGE03-HLD-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
