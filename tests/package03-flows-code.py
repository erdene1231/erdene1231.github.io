import collections,hashlib,itertools,json,pathlib,random,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parents[1];rng=random.Random(201029);counts=collections.Counter();names=['flow','disjoint','matching','cover']
def call(name,data):
 p=subprocess.run([str(tmp/name)],input=data,text=True,capture_output=True,timeout=15);assert p.returncode==0 and not p.stderr,(name,p.returncode,p.stderr);counts[name]+=1;return p.stdout.splitlines()
def cut_value(n,edges,s,t):
 return min(sum(c for a,b,c in edges if mask>>a&1 and not(mask>>b&1))for mask in range(1<<n)if mask>>s&1 and not(mask>>t&1))
def paths(n,edges,s,t):
 adj=[[]for _ in range(n)]
 for i,(a,b)in enumerate(edges):adj[a].append((b,i))
 out=[]
 def dfs(u,vis,nodes,ids):
  if u==t:out.append((nodes,ids));return
  for v,i in adj[u]:
   if v not in vis:dfs(v,vis|{v},nodes+[v],ids+[i])
 dfs(s,{s},[s],[]);return out
def packing(masks):
 dp={0:0}
 for path in set(masks):
  for mask,c in list(dp.items()):
   if not mask&path:dp[mask|path]=max(dp.get(mask|path,0),c+1)
 return max(dp.values())
def max_matching(l,r,edges):
 adj=[[]for _ in range(l)]
 for a,b in edges:adj[a].append(b)
 def solve(u,mask):
  if u==l:return 0
  return max([solve(u+1,mask)]+[1+solve(u+1,mask|1<<v)for v in adj[u]if not(mask>>v&1)])
 return solve(0,0)
def covers_oracle(n,edges):
 adj=[[]for _ in range(n)]
 for a,b in edges:adj[a].append(b)
 masks=set()
 def dfs(u,mask):
  masks.add(mask)
  for v in adj[u]:dfs(v,mask|1<<v)
 for u in range(n):dfs(u,1<<u)
 full=(1<<n)-1;dis=[n+1]*(1<<n);general=dis[:];dis[0]=general[0]=0
 for mask in range(1<<n):
  for p in masks:
   if not mask&p:dis[mask|p]=min(dis[mask|p],dis[mask]+1)
   if mask|p!=mask:general[mask|p]=min(general[mask|p],general[mask]+1)
 return dis[full],general[full]
with tempfile.TemporaryDirectory(prefix='flow-code-')as folder:
 tmp=pathlib.Path(folder)
 for name in names:subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all','-Wall','-Wextra',str(R/f'audit/package03-work/flows-{name}.cpp'),'-o',str(tmp/name)],check=True)
 F=[(0,1,5),(0,3,4),(3,1,3),(1,2,6),(2,4,8),(3,4,1),(2,5,5),(4,5,2)]
 cases=[(6,F,0,5),(2,[],0,1),(2,[(0,0,9),(0,1,10**12),(1,0,10**12),(0,1,10**12)],0,1)]
 for _ in range(110):
  n=rng.randrange(2,8);s,t=rng.sample(range(n),2);edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(8))for _ in range(rng.randrange(18))];cases.append((n,edges,s,t))
 for n,edges,s,t in cases:
  expected=cut_value(n,edges,s,t)
  for mode in ['E','S','D']:
   out=call('flow',f'{n} {len(edges)} {s+1} {t+1} {mode}\n'+''.join(f'{a+1} {b+1} {c}\n'for a,b,c in edges));value,cut=map(int,out[0].split());vis=list(map(int,out[1].split()));flow=list(map(int,out[2].split()))if len(out)>2 else[]
   assert value==cut==expected and vis[s]and not vis[t]and len(flow)==len(edges)
   balance=[0]*n
   for(a,b,c),f in zip(edges,flow):assert 0<=f<=c;balance[a]-=f;balance[b]+=f
   assert balance[s]==-value and balance[t]==value and all(balance[u]==0 for u in range(n)if u not in[s,t])
   assert sum(c for(a,b,c)in edges if vis[a]and not vis[b])==cut
 for _ in range(75):
  n=rng.randrange(2,6);s,t=rng.sample(range(n),2);edges=[(a,b)for a in range(n)for b in range(n)if a!=b and rng.random()<0.3]
  if len(edges)>9:edges=edges[:9]
  ps=paths(n,edges,s,t)
  for mode in ['E','V']:
   masks=[sum(1<<i for i in ids)if mode=='E'else(sum(1<<u for u in nodes[1:-1]) or 1<<n)for nodes,ids in ps]
   expected=packing(masks);out=call('disjoint',f'{n} {len(edges)} {s+1} {t+1} {mode}\n'+''.join(f'{a+1} {b+1}\n'for a,b in edges));assert int(out[0])==expected and len(out)==expected+1
   used=collections.Counter();internal=set()
   for line in out[1:]:
    data=list(map(int,line.split()));p=[u-1 for u in data[1:]];assert data[0]==len(p) and p[0]==s and p[-1]==t and len(p)==len(set(p))
    for edge in zip(p,p[1:]):assert edge in edges;used[edge]+=1
    if mode=='V':assert not internal.intersection(p[1:-1]);internal.update(p[1:-1])
   if mode=='E':assert all(c<=collections.Counter(edges)[e]for e,c in used.items())
 out=call('disjoint','2 3 1 2 E\n1 2\n1 2\n1 1\n');assert out==['2','2 1 2','2 1 2']
 for _ in range(100):
  l,r=rng.randrange(6),rng.randrange(6);edges=[(a,b)for a in range(l)for b in range(r)if rng.random()<0.4];out=call('matching',f'{l} {r} {len(edges)}\n'+''.join(f'{a+1} {b+1}\n'for a,b in edges));m=int(out[0]);assert m==max_matching(l,r,edges)
  pairs=[tuple(int(x)-1 for x in row.split())for row in out[1:m+1]];assert len({a for a,b in pairs})==len({b for a,b in pairs})==m and all(p in edges for p in pairs)
  parse=lambda line:[int(x)-1 for x in line.split()[2:]]
  cover=set(parse(out[m+1]));ind=set(parse(out[m+2]));assert len(cover)==m and cover|ind==set(range(l+r)) and not cover&ind;assert all(a in cover or l+b in cover for a,b in edges)
  best=min((mask.bit_count()for mask in range(1<<(l+r))if all(mask>>a&1 or mask>>(l+b)&1 for a,b in edges)),default=0);assert best==m
  if m<l:
   x=set(parse(out[m+3]));nbr=set(parse(out[m+4]));assert len(x)>len(nbr)and nbr=={b for a,b in edges if a in x}
  else:assert out[m+3]=='LEFT SATURATED'
 P=[(0,4),(4,5),(1,5),(5,2),(2,3),(5,6)]
 dags=[(7,P)]
 for _ in range(85):
  n=rng.randrange(1,8);order=list(range(n));rng.shuffle(order);edges=[(order[i],order[j])for i in range(n)for j in range(i+1,n)if rng.random()<0.3];dags.append((n,edges))
 for n,edges in dags:
  d,g=covers_oracle(n,edges);reach=[[False]*n for _ in range(n)]
  for a,b in edges:reach[a][b]=True
  for k in range(n):
   for a in range(n):
    for b in range(n):reach[a][b]|=reach[a][k]and reach[k][b]
  width=max(mask.bit_count()for mask in range(1<<n)if all(not reach[a][b]and not reach[b][a]for a in range(n)for b in range(a+1,n)if mask>>a&1 and mask>>b&1))
  for mode,expected in [('D',d),('G',g)]:
   out=call('cover',f'{n} {len(edges)} {mode}\n'+''.join(f'{a+1} {b+1}\n'for a,b in edges));count=int(out[0]);assert count==expected
   covered=collections.Counter()
   for line in out[1:count+1]:
    row=list(map(int,line.split()));p=[u-1 for u in row[1:]];assert len(p)==row[0]and len(p)==len(set(p))and all(e in edges for e in zip(p,p[1:]));covered.update(p)
   assert set(covered)==set(range(n))
   if mode=='D':assert max(covered.values())==1
   else:
    a=[int(x)-1 for x in out[-1].split()[2:]];assert len(a)==width==g==int(out[-1].split()[1])and all(not reach[x][y]and not reach[y][x]for x,y in itertools.combinations(a,2))
 for mode in ['D','G']:assert call('cover',f'2 2 {mode}\n1 2\n2 1\n')==['NOT A DAG']
 # Large sums and iterative deep path, without plain pseudo-polynomial DFS stress.
 n=2500;edges=[(i,i+1,10**12)for i in range(n-1)]
 for mode in ['E','S']:
  out=call('flow',f'{n} {n-1} 1 {n} {mode}\n'+''.join(f'{a+1} {b+1} {c}\n'for a,b,c in edges));assert out[0]==f'{10**12} {10**12}'
 # The exact source augmentation trace includes reverse 5→3 cancellation.
 flow=[0]*8;source=F
 for path,delta in [([0,1,2,4,5],2),([0,3,1,2,5],3),([0,1,2,5],1),([0,3,4,2,5],1)]:
  for a,b in zip(path,path[1:]):
   i=next((i for i,(u,v,c)in enumerate(source)if(u,v)==(a,b)),None)
   if i is not None:assert source[i][2]-flow[i]>=delta;flow[i]+=delta
   else:i=next(i for i,(u,v,c)in enumerate(source)if(u,v)==(b,a));assert flow[i]>=delta;flow[i]-=delta
 assert flow==[3,4,3,6,1,1,5,2]
report={'status':'passed','seed':201029,'programs':4,'runs':dict(counts),'totalRuns':sum(counts.values()),'sanitizer':'undefined','maxFlowN':2500,'testedCapacity':10**12,'oracle':'all s/t cuts, exhaustive simple-path packing, bipartite assignments/covers, DAG path-mask covers and antichains; output reconstruction and source residual trace','sha256':{name:hashlib.sha256((R/f'audit/package03-work/flows-{name}.cpp').read_bytes()).hexdigest()for name in names}}
(R/'audit/PACKAGE03-FLOWS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
