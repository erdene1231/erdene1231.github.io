import json,random,subprocess,tempfile,collections,itertools,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];src=ROOT/'audit/package03-work/centroid.cpp';rng=random.Random(314159)
def distances(n,edges):
 adj=[[]for _ in range(n+1)]
 for u,v in edges:adj[u].append(v);adj[v].append(u)
 out=[]
 for s in range(n+1):
  d=[-1]*(n+1);d[s]=0;q=collections.deque([s])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
  out.append(d)
 return out
with tempfile.TemporaryDirectory()as tmp:
 exe=Path(tmp)/'centroid';subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(exe)],check=True)
 cases=queries=0
 def run(n,edges,ops):
  global cases,queries
  ds=distances(n,edges);marked={1};expected=[]
  for t,u in ops:
   if t==1:marked.add(u)
   else:expected.append(min(ds[u][v]for v in marked))
  data=f'{n} {len(ops)}\n'+''.join(f'{u} {v}\n'for u,v in edges)+''.join(f'{t} {u}\n'for t,u in ops)
  p=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True,timeout=15);assert not p.stderr;assert list(map(int,p.stdout.split()))==expected,(n,edges,ops,p.stdout,expected);cases+=1;queries+=len(expected)
 for n in range(1,31):
  for shape in ['path','star','random']:
   for rep in range(2):
    edges=[(v-1 if shape=='path'else 1 if shape=='star'else rng.randrange(1,v),v)for v in range(2,n+1)];rng.shuffle(edges)
    ops=[(2,1),(2,n),(1,n),(1,n),(2,n)]+[(rng.choice([1,2,2]),rng.randrange(1,n+1))for _ in range(100)]
    run(n,edges,ops)
 # Enumerate all labelled trees through n=5 by Prüfer sequences.
 exhaustive=0
 for n in range(2,6):
  for code in itertools.product(range(1,n+1),repeat=n-2):
   deg=[0]+[1]*n
   for u in code:deg[u]+=1
   edges=[]
   for u in code:
    v=next(v for v in range(1,n+1)if deg[v]==1);edges.append((u,v));deg[u]-=1;deg[v]-=1
   a,b=[v for v in range(1,n+1)if deg[v]==1];edges.append((a,b))
   ops=[]
   for u in range(1,n+1):ops.extend([(2,v)for v in range(1,n+1)]);ops.append((1,u))
   run(n,edges,ops);exhaustive+=1
 for shape in ['path','star']:
  n=200000;edges=[(v-1 if shape=='path'else 1,v)for v in range(2,n+1)];ops=[(2,n),(1,n),(2,n),(2,n//2),(1,n//2),(2,n//2),(2,1)]
  expected=[n-1 if shape=='path'else 1,0,min(n//2-1,n-n//2)if shape=='path'else 1,0,0]
  data=f'{n} {len(ops)}\n'+''.join(f'{u} {v}\n'for u,v in edges)+''.join(f'{t} {u}\n'for t,u in ops)
  p=subprocess.run([str(exe)],input=data,text=True,capture_output=True,check=True,timeout=25);assert not p.stderr;assert list(map(int,p.stdout.split()))==expected
 # Instrument the actual decomposition: removed-component balance, true distances,
 # ancestor lists, empty active set, repeats, and independent rebuild reset.
 code=src.read_text();code=code[:code.index('int main() {')]+'''int main() {
 for (int n=1;n<=60;n++) {
  Centroid cd(n);for(int v=2;v<=n;v++)cd.add(v/2,v);cd.build();
  vector<int> roots;for(int u=1;u<=n;u++){if(!cd.cdpar[u])roots.push_back(u);assert(cd.query(u)==-1);}
  assert(roots.size()==1);
  for(int s=1;s<=n;s++) {
   vector<int>d(n+1,-1);queue<int>q;d[s]=0;q.push(s);while(!q.empty()){int u=q.front();q.pop();for(int v:cd.adj[u])if(d[v]<0){d[v]=d[u]+1;q.push(v);}}
   vector<int>chain;for(int c=s;c;c=cd.cdpar[c])chain.push_back(c);reverse(chain.begin(),chain.end());assert(chain.size()==cd.path[s].size());
   for(int i=0;i<(int)chain.size();i++){assert(cd.path[s][i].first==chain[i]);assert(cd.path[s][i].second==d[chain[i]]);}
   assert(chain.size()<=1+(int)log2(n));
  }
  for(int c=1;c<=n;c++) {
   vector<int>part;for(int u=1;u<=n;u++){int x=u;while(x&&x!=c)x=cd.cdpar[x];if(x==c)part.push_back(u);}
   vector<char>allowed(n+1),seen(n+1);for(int u:part)allowed[u]=true;seen[c]=true;
   for(int u:part)if(!seen[u]){int count=0;queue<int>q;q.push(u);seen[u]=true;while(!q.empty()){int v=q.front();q.pop();count++;for(int w:cd.adj[v])if(allowed[w]&&!seen[w]){seen[w]=true;q.push(w);}}assert(count<=(int)part.size()/2);}
  }
  auto path=cd.path;cd.mark(n);assert(cd.query(n)==0);cd.mark(n);cd.build();assert(cd.path==path);assert(cd.query(1)==-1);
 }
 Centroid b(10);for(auto[u,v]:vector<pair<int,int>>{{1,2},{2,3},{3,4},{4,5},{5,6},{2,7},{2,8},{2,9},{2,10}})b.add(u,v);b.build();assert(b.cdpar[2]==0&&b.cdpar[4]==2&&b.cdpar[5]==4&&b.cdpar[6]==5);assert((b.path[6]==vector<pair<int,int>>{{2,4},{4,2},{5,1},{6,0}}));b.mark(1);assert(b.query(6)==5);b.mark(3);assert(b.query(6)==3);b.mark(6);assert(b.query(6)==0&&b.query(8)==2);
}\n'''
 h=Path(tmp)/'invariants.cpp';h.write_text(code);subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(h),'-o',str(exe)],check=True);subprocess.run([str(exe)],check=True)
report={'status':'passed','Cpp17_UBSan':True,'small_tree_cases':cases,'exhaustive_labelled_trees_through5':exhaustive,'naive_BFS_nearest_mark_queries':queries,'singletons_paths_stars_random':True,'repeat_marks_and_unmarked_query':True,'balanced_component_removal_oracle':True,'centroid_chain_depth_and_original_distances':True,'rebuild_resets_marks_and_paths':True,'max_vertices':200000,'deep_path_star_stress':True,'worked_broom_mapping_and_query_trace':True}
(ROOT/'audit/PACKAGE03-CENTROID-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
