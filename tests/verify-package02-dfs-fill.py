"""DFS continuation simulation and grid regions against independent specifications."""
from pathlib import Path
import json,subprocess,tempfile,random,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
def recursive_forest(n,edges):
 graph=[[]for _ in range(n+1)]
 for a,b in edges:graph[a].append(b);graph[b].append(a)
 parent=[0]*(n+1);entry=[0]*(n+1);finish=[0]*(n+1);timer=0
 def visit(v):
  nonlocal timer
  timer+=1;entry[v]=timer
  for nxt in graph[v]:
   if entry[nxt]==0:parent[nxt]=v;visit(nxt)
  timer+=1;finish[v]=timer
 for v in range(1,n+1):
  if entry[v]==0:visit(v)
 return [(v,parent[v],entry[v],finish[v])for v in range(1,n+1)]
def grid_oracle(grid):
 rows=len(grid);cols=len(grid[0]);parent=list(range(rows*cols));size=[1]*len(parent)
 def root(v):
  while parent[v]!=v:parent[v]=parent[parent[v]];v=parent[v]
  return v
 def join(a,b):
  a,b=root(a),root(b)
  if a==b:return
  if size[a]<size[b]:a,b=b,a
  parent[b]=a;size[a]+=size[b]
 for r in range(rows):
  for c in range(cols):
   if grid[r][c]!='.':continue
   if r and grid[r-1][c]=='.':join(r*cols+c,(r-1)*cols+c)
   if c and grid[r][c-1]=='.':join(r*cols+c,r*cols+c-1)
 groups={}
 for r in range(rows):
  for c in range(cols):
   if grid[r][c]!='.':continue
   key=root(r*cols+c)
   if key not in groups:groups[key]=[0,0,r*cols+c]
   groups[key][0]+=1
   # Each unordered open-open shared side removes two from four sides per cell.
   if r and grid[r-1][c]=='.':groups[key][1]+=1
   if c and grid[r][c-1]=='.':groups[key][1]+=1
 return [(area,4*area-2*shared)for area,shared,_ in sorted(groups.values(),key=lambda x:x[2])]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['dfs','flood-fill']:
  body=json.loads((ROOT/f'audit/package02-lessons/{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];source=(ROOT/f'audit/package02-work/{id}.cpp').read_text();pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==(5 if id=='dfs' else 6)and ''.join(pieces[:-1])==pieces[-1]==source;assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
  exe=Path(tmp)/id;build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(ROOT/f'audit/package02-work/{id}.cpp'),'-o',str(exe)],capture_output=True,text=True,check=True);assert not build.stderr,build.stderr
  def run(text):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=15,check=True).stdout.split()
  count=0
  if id=='dfs':
   def check(n,edges,expected=None):
    values=list(map(int,run(f'{n} {len(edges)}\n'+''.join(f'{a} {b}\n'for a,b in edges))));assert len(values)==4*n;actual=list(zip(values[::4],values[1::4],values[2::4],values[3::4]));assert actual==(recursive_forest(n,edges)if expected is None else expected)
    assert sorted([x for _,_,entry,finish in actual for x in(entry,finish)])==list(range(1,2*n+1));links={tuple(sorted(e))for e in edges};records={v:(par,en,fin)for v,par,en,fin in actual}
    for v,parent,en,fin in actual:
     assert en<fin
     if parent:assert tuple(sorted((v,parent)))in links and records[parent][1]<en<fin<records[parent][2]
   for n in range(1,5):
    possible=list(itertools.combinations(range(1,n+1),2))
    for bits in itertools.product([False,True],repeat=len(possible)):check(n,[e for e,b in zip(possible,bits)if b]);count+=1
   for _ in range(180):
    n=rng.randint(1,30);edges=[(a,b)for a,b in itertools.combinations(range(1,n+1),2)if rng.random()<.15];rng.shuffle(edges);check(n,edges);count+=1
   check(4,[(1,1),(1,2),(1,2),(2,3),(3,4),(4,2)]);count+=1
   n=200000
   check(n,[(i,i+1)for i in range(1,n)],[(i,0 if i==1 else i-1,i,2*n-i+1)for i in range(1,n+1)]);count+=1
   check(n,[(1,i)for i in range(2,n+1)],[(1,0,1,2*n)]+[(i,1,2*i-2,2*i-1)for i in range(2,n+1)]);count+=1
   check(n,[],[(i,0,2*i-1,2*i)for i in range(1,n+1)]);count+=1
   extra={'graph_cases':count,'exhaustive_simple_graph_max_vertices':4,'maximum_vertices':n};oracle='Small-graph recursive DFS definition with same input order, independently verified time permutation/parent edges/nested intervals; maximum-chain/star/edgeless closed forms avoid recursive-oracle depth'
  else:
   def check(grid,expected=None):
    expected=grid_oracle(grid)if expected is None else expected;out=list(map(int,run(f'{len(grid)} {len(grid[0])}\n'+'\n'.join(grid)+'\n')));assert out[0]==len(expected)and list(zip(out[1::2],out[2::2]))==expected;assert sum(a for a,_ in expected)==sum(row.count('.')for row in grid)
   for rows in range(1,4):
    for cols in range(1,4):
     for bits in itertools.product('.#',repeat=rows*cols):check([''.join(bits[r*cols:(r+1)*cols])for r in range(rows)]);count+=1
   for _ in range(120):
    rows,cols=rng.randint(1,15),rng.randint(1,16);check([''.join(rng.choice('.#')for _ in range(cols))for _ in range(rows)]);count+=1
   for grid,expected in[(['..#..','.##..','##.#.','...#.'],[(3,8),(6,12),(4,10)]),(['...','.#.','...'],[(8,16)]),(['.#','#.'],[(1,4),(1,4)]),(['..'],[(2,6)])]:check(grid,expected);count+=1
   for grid,expected in[(['.'*1000]*1000,[(10**6,4000)]),(['#'*1000]*1000,[]),([''.join('.'if(r+c)%2==0 else'#'for c in range(1000))for r in range(1000)],[(1,4)]*500000),(['.'*1000],[(1000,2002)]),(['.']*1000,[(1000,2002)])]:check(grid,expected);count+=1
   # A one-cell-wide serpentine region stresses iterative exploration of a deep shape.
   snake=['.'*1000 if r%2==0 else('#'*999+'.'if(r//2)%2==0 else'.'+'#'*999)for r in range(1000)];area=500000+500;check(snake,[(area,2*area+2)]);count+=1
   extra={'grid_cases':count,'exhaustive_binary_grid_max_size':'3x3','maximum_grid':'1000x1000','max_regions_tested':500000};oracle='Independent DSU components ordered by minimum cell; combinatorial perimeter4*area-2*unordered_shared_sides, not queue-side logic; exhaustive small maps, holes/diagonals and million-cell closed forms'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split();reports.append({'lesson':id,**extra,'sample_passed':True,'compile_warnings':0,'undefined_behavior_sanitizer':'passed for all valid executions','program_sha256':hashlib.sha256(source.encode()).hexdigest(),'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Exact local C++17 programs and MN/EN fragments; semantic/native editor/publication gates separate'};(ROOT/'audit/PACKAGE02-DFS-FILL-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
