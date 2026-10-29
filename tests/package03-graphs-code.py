import json,random,subprocess,tempfile,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];random.seed(110116);runs=0
names=['list','weighted-list','matrix','weighted-matrix','edges','weighted-edges'];fixtures=json.loads((R/'audit/package03-work/graphs-fixtures.json').read_text())
with tempfile.TemporaryDirectory()as tmp:
 for name in names:
  exe=tmp+'/'+name;subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-Wconversion','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/graphs-{name}.cpp'),'-o',exe],check=True)
  weighted=name.startswith('weighted-');kind=name.removeprefix('weighted-');cases=[(f['n'],int(f['directed']),f['edges'])for f in fixtures.values()if bool(f['edges']and len(f['edges'][0])==3)==weighted]
  for _ in range(110):
   n=random.randint(1,10);dr=random.randrange(2);edges=[]
   for i in range(random.randrange(35)):
    e=[random.randint(1,n),random.randint(1,n)]
    if weighted:e.append(random.choice([0,-1,1,5,2**40,-2**40,10**18,-10**18]))
    edges.append(e)
   cases.append((n,dr,edges))
  for n,dr,edges in cases:
   queries=list(range(1,n+1));inp=f'{n} {len(edges)} {dr}'+(f' {len(queries)}'if kind=='edges'else'')+'\n'+'\n'.join(' '.join(map(str,e))for e in edges)+'\n'+(' '.join(map(str,queries))if kind=='edges'else'')+'\n';expected=[]
   if kind=='matrix':
    mat=[[None if weighted else 0 for _ in range(n)]for _ in range(n)]
    for e in edges:
     a,b=e[:2];pairs=[(a,b)]+([]if dr else[(b,a)])
     for u,v in pairs:
      prev=mat[u-1][v-1];mat[u-1][v-1]=min(prev,e[2])if weighted and prev is not None else e[2]if weighted else 1
    expected=[' '.join('.'if v is None else str(v)for v in row)for row in mat]
   else:
    if kind=='edges':expected=[' '.join(map(str,e))for e in edges]
    incoming=[0]*n;out=[0]*n
    for u in range(1,n+1):
     ns=[]
     for e in edges:
      a,b=e[:2]
      if a==u:ns.append(str(b)+(':'+str(e[2])if weighted else''));out[u-1]+=1
      if b==u:incoming[u-1]+=1
      if not dr:
       if b==u:ns.append(str(a)+(':'+str(e[2])if weighted else''));out[u-1]+=1
       if a==u:incoming[u-1]+=1
     expected.append(str(u)+':' +(' '+' '.join(ns)if ns else''))
    if kind=='list'and not weighted:expected+=[' '.join(map(str,incoming)),' '.join(map(str,out))]
   result=subprocess.run([exe],input=inp,text=True,capture_output=True,check=True);assert not result.stderr,result.stderr;assert result.stdout.splitlines()==expected,(name,inp,result.stdout,expected);runs+=1
# Independent source-graph claims: components by set merging; shortest simple paths by permutation.
g=fixtures['initial'];deg=[sum(a==u for a,b in g['edges'])+sum(b==u for a,b in g['edges'])for u in range(1,6)];assert deg==[3,3,2,4,2]
f=fixtures['components'];groups=[{i}for i in range(1,9)]
for a,b in f['edges']:
 x=next(s for s in groups if a in s);y=next(s for s in groups if b in s)
 if x is not y:x.update(y);groups.remove(y)
assert sorted(map(sorted,groups))==[[1,2,3],[4,5,6,7],[8]]
f=fixtures['weighted'];weights={frozenset([a,b]):w for a,b,w in f['edges']};paths=[]
for k in range(4):
 for mid in itertools.permutations([2,3,4],k):
  seq=(1,)+mid+(5,);pairs=[frozenset([a,b])for a,b in zip(seq,seq[1:])]
  if all(e in weights for e in pairs):paths.append((sum(weights[e]for e in pairs),seq))
assert min(paths)==(11,(1,3,4,5))
A={1,2,6};assert all((a in A)!=(b in A)for a,b in fixtures['bipartite']['edges']);assert all(frozenset(e)in{frozenset([1,2]),frozenset([2,5]),frozenset([5,1])}for e in[(1,2),(2,5),(5,1)])
# The directed reachability source has no outgoing edge from5.
assert all(a!=5 for a,b in fixtures['directed']['edges']);assert [(3,1),(1,2),(2,5)]==[tuple(e)for e in fixtures['directed']['edges']if tuple(e)in[(3,1),(1,2),(2,5)]]
report={'status':'passed','programs':6,'ubsan_oracle_runs':runs,'cases':'All retained source fixtures plus110 deterministic random multigraphs per program; loops, duplicates, directed/undirected, isolated nodes, zero/negative/64-bit weights','source_checks':['degree14','three components','shortest simple path11','two-color partition','directed sink5']};(R/'audit/PACKAGE03-GRAPHS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
