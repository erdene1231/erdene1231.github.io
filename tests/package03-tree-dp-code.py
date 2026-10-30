"""Independent subset enumeration and BFS tree metrics; compiles actual lesson programs."""
import collections,itertools,json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(37281);MOD=1000000007

def prufer(n,s):
 deg=[0]+[1]*n
 for x in s:deg[x]+=1
 e=[]
 for x in s:
  v=next(v for v in range(1,n+1)if deg[v]==1);e.append((v,x));deg[v]-=1;deg[x]-=1
 last=[v for v in range(1,n+1)if deg[v]==1]
 if n>1:e.append(tuple(last))
 return e

def metrics(n,e):
 a=[[]for _ in range(n+1)]
 for u,v in e:a[u].append(v);a[v].append(u)
 dist=[]
 for s in range(1,n+1):
  d=[-1]*(n+1);d[s]=0;q=collections.deque([s])
  while q:
   u=q.popleft()
   for v in a[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
  dist.append(d[1:])
 par=[0]*(n+1);par[1]=-1;q=collections.deque([1])
 while q:
  u=q.popleft()
  for v in a[u]:
   if not par[v]:par[v]=u;q.append(v)
 result=[]
 for u in range(1,n+1):
  sub=set()
  for v in range(1,n+1):
   x=v
   while x!=-1 and x!=u:x=par[x]
   if x==u:sub.add(v)
  row=dist[u-1];result.append([len(sub),max(row[v-1]for v in sub),max([0]+[row[v-1]for v in range(1,n+1)if v not in sub]),max(row),sum(row)])
 return result

with tempfile.TemporaryDirectory()as t:
 t=Path(t);bins={}
 for name in ['count','reroot']:
  b=t/name;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/tree-dp-{name}.cpp'),'-o',str(b)],check=True);bins[name]=b
 def run(name,n,e):
  data=str(n)+'\n'+''.join(f'{u} {v}\n'for u,v in e);p=subprocess.run([str(bins[name])],input=data,text=True,capture_output=True,timeout=20);assert p.returncode==0,p.stderr;assert not p.stderr,p.stderr;return p.stdout
 cases=[]
 for n in range(1,6):
  for s in itertools.product(range(1,n+1),repeat=max(0,n-2)):cases.append((n,prufer(n,s)))
 for _ in range(180):
  n=rng.randrange(2,13);e=prufer(n,[rng.randrange(1,n+1)for _ in range(n-2)]);rng.shuffle(e);e=[(v,u)if rng.randrange(2)else(u,v)for u,v in e];cases.append((n,e))
 examples=json.loads((R/'audit/PACKAGE03-TREE-DP-EXAMPLES.json').read_text())
 cases.extend([(5,examples['old_edges']),(6,examples['source_edges'])])
 source_rows=metrics(6,examples['source_edges'])
 for i,key in enumerate(['source_sz','source_down','source_up','source_ecc','source_sum']):assert [r[i]for r in source_rows]==examples[key]
 for n,e in cases:
  count=sum(all(not(mask>>(u-1)&1 and mask>>(v-1)&1)for u,v in e)for mask in range(1<<n))
  assert int(run('count',n,e))==count%MOD,(n,e,count)
  got=[list(map(int,line.split()))for line in run('reroot',n,e).splitlines()];assert got==metrics(n,e),(n,e,got,metrics(n,e))
 # Root changes and repeated calls on the same reusable object are tested separately.
 for name in ['count','reroot']:
  src=(R/f'audit/package03-work/tree-dp-{name}.cpp').read_text().split('int main() {')[0];src+='\nint main() { int n; cin >> n; TreeDP g(n); for(int i=1,a,b;i<n;i++){cin>>a>>b;g.add(a,b);} for(int r=1;r<=n;r++){'
  src+= 'cout << g.run(r) << "\\n";' if name=='count' else 'g.run(r); for(int u=1;u<=n;u++) cout << g.ecc[u] << " " << g.sum[u] << "\\n";'
  src+='}}\n';f=t/(name+'-roots.cpp');f.write_text(src);b=t/(name+'-roots');subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(f),'-o',str(b)],check=True)
  for n,e in cases[::9]:
   data=str(n)+'\n'+''.join(f'{u} {v}\n'for u,v in e);p=subprocess.run([str(b)],input=data,text=True,capture_output=True,check=True);got=list(map(int,p.stdout.split()));assert not p.stderr
   if name=='count':assert got==[int(run(name,n,e))]*n
   else:assert got==[x for _ in range(n)for row in metrics(n,e)for x in row[3:]]
 n=200000
 for kind in ['chain','star']:
  e=[(v-1,v)if kind=='chain'else(1,v)for v in range(2,n+1)]
  if kind=='chain':
   x,y=1,2
   for _ in range(n):x,y=y,(x+y)%MOD
   expected=x
  else:expected=(pow(2,n-1,MOD)+1)%MOD
  assert int(run('count',n,e))==expected
  got=[list(map(int,line.split()))for line in run('reroot',n,e).splitlines()];assert len(got)==n
  for u,row in enumerate(got,1):
   if kind=='chain':expectedrow=[n-u+1,n-u,u-1,max(u-1,n-u),u*(u-1)//2+(n-u)*(n-u+1)//2]
   elif u==1:expectedrow=[n,1,0,1,n-1]
   else:expectedrow=[1,0,2,2,2*n-3]
   assert row==expectedrow,(kind,u,row,expectedrow)
 out={'status':'passed','CXX17_UBSan_programs':2,'exhaustive_labeled_trees_through_n':5,'small_exhaustive_and_random_trees':len(cases),'independent_subset_oracle_max_n':12,'independent_all_source_BFS_and_ancestor_membership':True,'every_sz_down_up_ecc_sum_checked':True,'root_invariance_and_repeated_run_checked':True,'chain_and_star_max_n':200000,'every_large_tree_output_checked':True,'large_sum_uses_64bit':True,'modular_counts_checked':True}
 (R/'audit/PACKAGE03-TREE-DP-CODE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
