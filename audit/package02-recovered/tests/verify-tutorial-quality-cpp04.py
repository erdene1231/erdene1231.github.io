"""Retained weighted-graph, grid and rooted-tree references; independent local checks."""
import collections,hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ids=['dijkstra','floyd-warshall','flood-fill','tree-basics','kruskal','lca'];rng=random.Random(121027)
rows=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from'node:fs';import{proposedTutorialRows}from'./tools/part04_tutorial_proposals.mjs';process.stdout.write(JSON.stringify(proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials)));"],cwd=ROOT,text=True));reports=[]
def run(exe,data):return subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=8).stdout.split()
def components(n,edges):
 labels=list(range(n))
 for a,b,*_ in edges:
  old,new=labels[b],labels[a];labels=[new if label==old else label for label in labels]
 return len(set(labels))
def rooted(n,edges,root):
 adj=[[]for i in range(n)]
 for a,b in edges:adj[a].append(b);adj[b].append(a)
 parent=[-1]*n;depth=[-1]*n;depth[root]=0;q=collections.deque([root])
 while q:
  v=q.popleft()
  for u in adj[v]:
   if depth[u]<0:depth[u]=depth[v]+1;parent[u]=v;q.append(u)
 size=[0]*n
 for v in range(n):
  u=v
  while u!=-1:size[u]+=1;u=parent[u]
 return parent,depth,size
with tempfile.TemporaryDirectory()as tmp:
 for topic in ids:
  doc=next(r['body']for r in rows if r['body']['id']==topic);codes=lambda d:[b['text']for s in d['sections']for b in s['blocks']if b['type']=='code'and b.get('language')=='C++17'];mn,en=codes(doc),codes(doc['translations']['en']);assert mn==en and len(mn)==2;helper,program=mn;assert program[:program.index('int main(')].strip()==helper.strip();assert '\t'not in program;assert all(not l.startswith(' ')or(len(l)-len(l.lstrip()))%4==0 for l in program.splitlines())
  src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(program);built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr
  blocks=[b for s in doc['sections']for b in s['blocks']];sample=lambda lang:next(b['text']for b in blocks if b['type']=='code'and b.get('language')==lang);assert run(exe,sample('Input'))==sample('Output').split()
  for case in range(20):
   if topic in ['dijkstra','floyd-warshall']:
    n=rng.randint(1,6);edges=[(rng.randrange(n),rng.randrange(n),rng.randrange(21))for i in range(rng.randrange(16))];source=rng.randrange(n);answers=[]
    if topic=='dijkstra':
     distance=[10**30]*n;distance[source]=0
     for step in range(n-1):
      previous=distance[:]
      for a,b,w in edges:distance[b]=min(distance[b],previous[a]+w)
     answers=distance;data=f'{n} {len(edges)} {source}\n'
    else:
     adj=[[]for i in range(n)]
     for a,b,w in edges:adj[a].append((b,w))
     for start in range(n):
      best=[10**30]*n
      def visit(v,mask,cost):
       best[v]=min(best[v],cost)
       for u,w in adj[v]:
        if not mask>>u&1:visit(u,mask|1<<u,cost+w)
      visit(start,1<<start,0);answers+=best
     data=f'{n} {len(edges)}\n'
    data+='\n'.join(f'{a} {b} {w}'for a,b,w in edges)+'\n';expected=[str(x if x<10**30 else-1)for x in answers]
   elif topic=='flood-fill':
    n=rng.randint(1,6);m=rng.randint(1,6);grid=[''.join(rng.choice('.#')for c in range(m))for r in range(n)];labels={r*m+c:r*m+c for r in range(n)for c in range(m)if grid[r][c]=='.'}
    for cell in list(labels):
     r,c=divmod(cell,m)
     for rr,cc in [(r+1,c),(r,c+1)]:
      other=rr*m+cc
      if rr<n and cc<m and other in labels:
       old,new=labels[other],labels[cell];labels={k:new if v==old else v for k,v in labels.items()}
    expected=[str(len(set(labels.values())))];data=f'{n} {m}\n'+'\n'.join(grid)+'\n'
   elif topic=='kruskal':
    n=rng.randint(1,6);edges=[(rng.randrange(n),rng.randrange(n),rng.randint(-10,20))for i in range(rng.randrange(10))];best=None
    for chosen in itertools.combinations(edges,n-1):
     if components(n,chosen)==1:best=min(best if best is not None else 10**30,sum(w for a,b,w in chosen))
    expected=['IMPOSSIBLE']if best is None else[str(best)];data=f'{n} {len(edges)}\n'+'\n'.join(f'{a} {b} {w}'for a,b,w in edges)+'\n'
   else:
    n=rng.randint(1,25);labels=rng.sample(range(n),n);edges=[(labels[i],labels[rng.randrange(i)])for i in range(1,n)];root=rng.randrange(n);parent,depth,size=rooted(n,edges,root)
    if topic=='tree-basics':expected=[str(x)for v in range(n)for x in[parent[v],depth[v],size[v]]];data=f'{n} {root}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+'\n'
    else:
     queries=[(rng.randrange(n),rng.randrange(n))for i in range(30)];expected=[]
     for a,b in queries:
      ancestors=set();u=a
      while u!=-1:ancestors.add(u);u=parent[u]
      u=b
      while u not in ancestors:u=parent[u]
      # Distance independently counts edges on both parent paths to their intersection.
      length=0
      for v in [a,b]:
       while v!=u:length+=1;v=parent[v]
      expected +=[str(u),str(length)]
     data=f'{n} {root} {len(queries)}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+'\n'+'\n'.join(f'{a} {b}'for a,b in queries)+'\n'
   assert run(exe,data)==expected,(topic,case,data,expected)
  if topic=='dijkstra':boundary=[('1 0 0\n',['0']),('2 2 0\n0 1 0\n1 0 0\n',['0','0']),('3 3 0\n0 1 3000000000000000000\n1 2 3000000000000000000\n0 2 1\n',['0','3000000000000000000','1']),('2 0 1\n',['-1','0'])]
  elif topic=='floyd-warshall':boundary=[('1 1\n0 0 5\n',['0']),('2 2\n0 1 9\n0 1 3\n',['0','3','-1','0']),('3 3\n0 1 3000000000000000000\n1 2 3000000000000000000\n0 2 1\n',['0','3000000000000000000','1','-1','0','3000000000000000000','-1','-1','0'])]
  elif topic=='flood-fill':boundary=[('1 1\n.\n',['1']),('1 1\n#\n',['0']),('2 2\n.#\n#.\n',['2']),('1000 1000\n'+('.'*1000+'\n')*1000,['1'])]
  elif topic=='kruskal':boundary=[('1 1\n0 0 -10\n',['0']),('3 1\n0 1 -5\n',['IMPOSSIBLE']),('2 2\n0 1 9223372036854775807\n0 1 -9223372036854775808\n',['-9223372036854775808']),('3 2\n0 1 -9223372036854775808\n1 2 9223372036854775807\n',['-1'])]
  elif topic=='tree-basics':boundary=[('1 0\n',['-1','0','1']),('100000 0\n'+'\n'.join(f'{i-1} {i}'for i in range(1,100000))+'\n',[str(x)for i in range(100000)for x in[i-1,i,100000-i]])]
  else:boundary=[('1 0 1\n0 0\n',['0','0']),('100000 99999 3\n'+'\n'.join(f'{i-1} {i}'for i in range(1,100000))+'\n0 99999\n12345 54321\n65536 65536\n',['99999','99999','54321','41976','65536','0'])]
  for data,expected in boundary:assert run(exe,data)==expected,(topic,'boundary')
  reports.append({'id':topic,'reviewed_blocks':4,'unique_program_sha256':hashlib.sha256(program.encode()).hexdigest(),'helper_sha256':hashlib.sha256(helper.encode()).hexdigest(),'both_languages_identical':True,'helper_is_exact_program_prefix':True,'compile_warnings':0,'samples':1,'oracle_cases':20,'boundary_cases':len(boundary)})
report={'status':'passed','local_proposals_only':True,'seed':121027,'reviewed_blocks':24,'unique_programs':6,'samples':6,'oracle_cases':120,'boundary_cases':sum(p['boundary_cases']for p in reports),'programs':reports,'oracle_methods':['bounded-edge Bellman relaxation','all simple directed paths','naive grid component-label merging','all spanning-tree edge subsets','BFS rooting and ancestor-membership subtree counts','parent-chain LCA intersection and path length'],'limits':'Retained contracts only;nonnegative weighted shortest paths,valid trees,and bounded64-bit sums. No production calls or publication.'};(ROOT/'audit/PART04-TUTORIAL-CPP-TESTS04.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='programs'})
