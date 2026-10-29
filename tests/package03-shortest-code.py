import json,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];random.seed(131231);runs=0
BF=[(1,2,5),(1,3,3),(1,4,7),(2,4,3),(2,5,2),(3,4,1),(4,5,2)];DJ=[(1,2,5),(2,3,2),(3,4,6),(1,4,9),(1,5,1),(4,5,2)];FW=[(a,b,7 if(a,b)==(3,4)else w)for a,b,w in DJ];NEG=[(1,2,3),(1,3,5),(2,3,2),(3,4,-7),(4,2,1)];COUNTER=[(1,2,2),(2,4,3),(1,3,6),(3,4,-5)]
fixtures={'bellman-ford':{'n':5,'edges':BF,'directed':False,'states':[[0,'INF','INF','INF','INF'],[0,5,3,7,'INF'],[0,5,3,4,7],[0,5,3,4,6]],'path':[1,3,4,5]},'negative-cycle':{'n':4,'edges':NEG,'directed':True,'cycle':[2,3,4,2],'cycle_weight':-4},'dijkstra':{'n':5,'edges':DJ,'directed':False,'states':[[0,'INF','INF','INF','INF'],[0,5,'INF',9,1],[0,5,'INF',3,1],[0,5,9,3,1],[0,5,7,3,1]],'selected':[1,5,4,2,3]},'negative-edge':{'n':4,'edges':COUNTER,'directed':True,'path':[1,3,4],'distance':1},'floyd':{'n':5,'edges':FW,'directed':False,'matrices':[
[[0,5,'INF',9,1],[5,0,2,'INF','INF'],['INF',2,0,7,'INF'],[9,'INF',7,0,2],[1,'INF','INF',2,0]],
[[0,5,'INF',9,1],[5,0,2,14,6],['INF',2,0,7,'INF'],[9,14,7,0,2],[1,6,'INF',2,0]],
[[0,5,7,9,1],[5,0,2,14,6],[7,2,0,7,8],[9,14,7,0,2],[1,6,8,2,0]],
[[0,5,7,9,1],[5,0,2,9,6],[7,2,0,7,8],[9,9,7,0,2],[1,6,8,2,0]],
[[0,5,7,3,1],[5,0,2,8,6],[7,2,0,7,8],[3,8,7,0,2],[1,6,8,2,0]]],'path':[2,1,5,4],'distance':8}}
(R/'audit/package03-work/shortest-fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
def arcs(edges,dr):return edges if dr else edges+[(v,u,w)for u,v,w in edges]
def oracle(n,edges,s=None):
 d=[None]*(n+1)if s is not None else[0]*(n+1)
 if s is not None:d[s]=0
 improved=[]
 for step in range(1,n+1):
  nd=d[:];improved=[]
  for u,v,w in edges:
   if d[u]is not None and(nd[v]is None or d[u]+w<nd[v]):nd[v]=d[u]+w
  for v in range(1,n+1):
   if nd[v]is not None and(d[v]is None or nd[v]<d[v]):improved.append(v)
  d=nd
 bad=set(improved);changed=True
 while changed:
  changed=False
  for u,v,w in edges:
   if u in bad and v not in bad:bad.add(v);changed=True
 return ['-INF'if v in bad else'INF'if d[v]is None else str(d[v])for v in range(1,n+1)],bool(improved)
with tempfile.TemporaryDirectory()as tmp:
 exes={}
 for name in['bellman-ford','spfa','dijkstra','floyd']:
  exe=tmp+'/'+name;exes[name]=exe;subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wconversion','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/shortest-{name}.cpp'),'-o',exe],check=True)
 def run(name,inp):
  global runs
  r=subprocess.run([exes[name]],input=inp,text=True,capture_output=True,check=True,timeout=25);assert not r.stderr,r.stderr;runs+=1;return r.stdout.splitlines()
 cases=[(f['n'],int(f['directed']),f['edges'])for f in fixtures.values()]
 cases += [(1,1,[]),(1,1,[(1,1,-1)]),(5,1,[(1,2,3),(3,3,-1),(3,4,0)]),(2,1,[(1,2,w)for w in range(40,-1,-1)]),(4,1,[(1,2,10**9),(2,3,10**9),(3,4,10**9)]),(3,1,[(2,3,-10**9)])]
 for _ in range(180):
  n=random.randint(1,8);dr=random.randrange(2);edges=[(random.randint(1,n),random.randint(1,n),random.choice([-10**9,-5,-1,0,1,2,7,10**9]))for _ in range(random.randrange(22))];cases.append((n,dr,edges))
 for n,dr,edges in cases:
  aa=arcs(edges,dr);s=1;t=n;text='\n'.join(f'{a} {b} {w}'for a,b,w in edges)+'\n';expected,neg=oracle(n,aa,s);_,global_neg=oracle(n,aa)
  out=run('bellman-ford',f'{n} {len(edges)} {dr} {s}\n'+text);assert out[0].split()==expected,(edges,out,expected);assert out[1]==('GLOBAL_NEGATIVE_CYCLE'if global_neg else'NO_NEGATIVE_CYCLE')
  out=run('spfa',f'{n} {len(edges)} {dr} {s}\n'+text);assert out==['REACHABLE_NEGATIVE_CYCLE']if neg else out[0].split()==expected,(edges,out,expected)
  out=run('floyd',f'{n} {len(edges)} {dr}\n'+text);assert len(out)==n
  for u in range(1,n+1):assert out[u-1].split()==oracle(n,aa,u)[0],(u,edges,out[u-1],oracle(n,aa,u))
  out=run('dijkstra',f'{n} {len(edges)} {dr} {s} {t}\n'+text)
  if any(w<0 for a,b,w in edges):assert out==['NEGATIVE_EDGE']
  else:
   assert out[0].split()==expected
   if expected[t-1]=='INF':assert out[1]=='IMPOSSIBLE'
   else:
    path=list(map(int,out[1].split()));assert path[0]==s and path[-1]==t and len(path)<=n;cost=0
    for a,b in zip(path,path[1:]):cost+=min(w for u,v,w in aa if(u,v)==(a,b))
    assert cost==int(expected[t-1])
 # Nonnegative random graphs exercise stale entries and reconstruction, not merely rejection.
 for _ in range(100):
  n=random.randint(1,10);dr=random.randrange(2);edges=[(random.randint(1,n),random.randint(1,n),random.choice([0,1,5,10**12]))for i in range(random.randrange(30))];s=random.randint(1,n);t=random.randint(1,n);out=run('dijkstra',f'{n} {len(edges)} {dr} {s} {t}\n'+'\n'.join(f'{a} {b} {w}'for a,b,w in edges)+'\n');expected,_=oracle(n,arcs(edges,dr),s);assert out[0].split()==expected
  if expected[t-1]!='INF':
   path=list(map(int,out[1].split()));assert path[0]==s and path[-1]==t and len(path)<=n;assert sum(min(w for a,b,w in arcs(edges,dr)if a==u and b==v)for u,v in zip(path,path[1:]))==int(expected[t-1])
 # Source intermediate Floyd matrices checked by snapshot DP, distinct from final program.
 mat=[[10**30 if v=='INF'else v for v in row]for row in fixtures['floyd']['matrices'][0]]
 for k in range(5):
  old=[row[:]for row in mat];mat=[[min(old[i][j],old[i][k]+old[k][j])for j in range(5)]for i in range(5)]
  if k in[0,1,2,4]:assert mat==[[10**30 if v=='INF'else v for v in row]for row in fixtures['floyd']['matrices'][{0:1,1:2,2:3,4:4}[k]]]
 # Negative-cycle numeric growth: floor must prevent signed overflow without contaminating unreachable pairs.
 n=80;edges=[(1,1,-1)]+[(i,i+1,0)for i in range(1,n)]+[(i+1,i,0)for i in range(1,n)];out=run('floyd',f'{n} {len(edges)} 1\n'+'\n'.join(f'{a} {b} {w}'for a,b,w in edges)+'\n');assert all(row.split()==['-INF']*n for row in out)
 # Sparse large Dijkstra graph with64-bit answers.
 n=200000;out=run('dijkstra',f'{n} {n-1} 1 1 {n}\n'+'\n'.join(f'{i} {i+1} {10**12}'for i in range(1,n))+'\n');assert out[0].split()[-1]==str((n-1)*10**12);assert len(out[1].split())==n
report={'status':'passed','programs':4,'UBSan_oracle_runs':runs,'oracles':'Snapshot n-round bounded-walk DP and reachability closure, all-pairs from independent per-source oracle; exact source Floyd stage matrices; reconstructed path weight checks','cases':'negative reachable/unreachable cycles, self-loops, parallel/zero edges, n=1, disconnected,64-bit distances, stale heap entries,80-node negative saturation and200000-node Dijkstra chain','source_corrections':'Bellman-Ford example distance6 (not3); finite negative-edge counterexample explicitly directed; distinct Dijkstra6 versus Floyd7 top edge'};(R/'audit/PACKAGE03-SHORTEST-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
