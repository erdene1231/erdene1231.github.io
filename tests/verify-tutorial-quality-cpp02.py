"""Contextual review of six retained tutorials:24blocks, six programs and BFS parent harness."""
import concurrent.futures,hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ids=['bfs','binary-search-answer','prefix-sums-2d','knapsack','lis','sparse-table'];rng=random.Random(101027)
rows=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from'node:fs';import{proposedTutorialRows}from'./tools/part04_tutorial_proposals.mjs';process.stdout.write(JSON.stringify(proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials)));"],cwd=ROOT,text=True));reports=[]
def run(exe,data):return subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=5).stdout.split()
def compile_code(code,src,exe):
 src.write_text(code);result=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert result.returncode==0 and not result.stderr,result.stderr
with tempfile.TemporaryDirectory(prefix='part04-tutorial-cpp02-')as tmp:
 def build(topic):
  doc=next(r['body']for r in rows if r['body']['id']==topic);codes=lambda d:[b['text']for s in d['sections']for b in s['blocks']if b['type']=='code'and b.get('language')=='C++17'];mn,en=codes(doc),codes(doc['translations']['en']);assert mn==en and len(mn)==2,topic;helper,program=mn
  assert program[:program.index('int main(')].strip()==helper.strip();assert '\t'not in program;assert all(not line.startswith(' ')or(len(line)-len(line.lstrip()))%4==0 for line in program.splitlines())
  exe=Path(tmp)/topic;compile_code(program,Path(tmp)/(topic+'.cpp'),exe)
  blocks=[b for s in doc['sections']for b in s['blocks']];sample_input=next(b['text']for b in blocks if b['type']=='code'and b.get('language')=='Input');sample_output=next(b['text']for b in blocks if b['type']=='code'and b.get('language')=='Output');assert run(exe,sample_input)==sample_output.split()
  return topic,exe,helper,{'id':topic,'reviewed_blocks':4,'unique_program_sha256':hashlib.sha256(program.encode()).hexdigest(),'helper_sha256':hashlib.sha256(helper.encode()).hexdigest(),'both_languages_identical':True,'helper_is_exact_program_prefix':True,'compile_warnings':0,'samples':1,'oracle_cases':30}
 with concurrent.futures.ThreadPoolExecutor(2)as pool:built=list(pool.map(build,ids))
 bfs_helper=next(helper for topic,exe,helper,report in built if topic=='bfs');parent_exe=Path(tmp)/'bfs-parents'
 compile_code(bfs_helper+r'''
int main() {
    int n, edgeCount;
    cin >> n >> edgeCount;
    vector<vector<int>> neighbors(n);
    for (int i = 0; i < edgeCount; ++i) {
        int first, second;
        cin >> first >> second;
        neighbors[first].push_back(second);
        neighbors[second].push_back(first);
    }
    int source;
    cin >> source;
    auto result = bfs(neighbors, source);
    for (int value : result.first) cout << value << ' ';
    for (int value : result.second) cout << value << ' ';
}
''',Path(tmp)/'bfs-parents.cpp',parent_exe)
 for topic,exe,helper,report in built:
  for case in range(30):
   if topic=='bfs':
    n=rng.randint(1,10);source=rng.randrange(n);edges=[(rng.randrange(n),rng.randrange(n))for i in range(rng.randint(0,20))];distance=[[0 if i==j else 1000 for j in range(n)]for i in range(n)];adjacent=[[False]*n for i in range(n)]
    for a,b in edges:distance[a][b]=distance[b][a]=min(distance[a][b],1);adjacent[a][b]=adjacent[b][a]=True
    for mid in range(n):
     for a in range(n):
      for b in range(n):distance[a][b]=min(distance[a][b],distance[a][mid]+distance[mid][b])
    expected=[str(d if d<1000 else-1)for d in distance[source]];data=f'{n} {len(edges)}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+f'\n{source}\n'
    witness=list(map(int,run(parent_exe,data)));assert list(map(str,witness[:n]))==expected;parents=witness[n:];assert len(parents)==n
    for vertex in range(n):
     if vertex==source or expected[vertex]=='-1':assert parents[vertex]==-1;continue
     current=vertex;length=0;seen=set()
     while current!=source:
      assert current not in seen;seen.add(current);parent=parents[current];assert 0<=parent<n and adjacent[current][parent];assert int(expected[parent])+1==int(expected[current]);current=parent;length+=1
     assert length==int(expected[vertex])
   elif topic=='binary-search-answer':
    n=rng.randint(1,10);limit=rng.randint(1,n);values=[rng.randint(0,20)for i in range(n)];optimum=sum(values)
    for mask in range(1<<(n-1)):
     if mask.bit_count()+1>limit:continue
     sums=[0]
     for i,value in enumerate(values):
      sums[-1]+=value
      if i<n-1 and mask>>i&1:sums.append(0)
     optimum=min(optimum,max(sums))
    data=f'{n} {limit}\n'+' '.join(map(str,values))+'\n';expected=[str(optimum)]
   elif topic=='prefix-sums-2d':
    n=rng.randint(1,6);m=rng.randint(1,6);grid=[[rng.randint(-100,100)for j in range(m)]for i in range(n)];queries=[];expected=[]
    for i in range(30):
     first,last=sorted([rng.randrange(n),rng.randrange(n)]);left,right=sorted([rng.randrange(m),rng.randrange(m)]);queries.append(f'{first} {left} {last} {right}');expected.append(str(sum(grid[r][c]for r in range(first,last+1)for c in range(left,right+1))))
    data=f'{n} {m} {len(queries)}\n'+'\n'.join(' '.join(map(str,row))for row in grid)+'\n'+'\n'.join(queries)+'\n'
   elif topic=='knapsack':
    n=rng.randint(0,10);capacity=rng.randint(0,20);items=[(rng.randint(1,15),rng.randrange(10**10))for i in range(n)];optimum=0
    for mask in range(1<<n):
     chosen=[item for i,item in enumerate(items)if mask>>i&1]
     if sum(w for w,v in chosen)<=capacity:optimum=max(optimum,sum(v for w,v in chosen))
    data=f'{n} {capacity}\n'+'\n'.join(f'{w} {v}'for w,v in items)+'\n';expected=[str(optimum)]
   elif topic=='lis':
    n=rng.randint(0,12);values=[rng.randint(-5,5)for i in range(n)];optimum=0
    for mask in range(1<<n):
     chosen=[value for i,value in enumerate(values)if mask>>i&1]
     if all(a<b for a,b in zip(chosen,chosen[1:])):optimum=max(optimum,len(chosen))
    data=f'{n}\n'+' '.join(map(str,values))+'\n';expected=[str(optimum)]
   else:
    n=rng.randint(1,20);values=[rng.randint(-10**12,10**12)for i in range(n)];queries=[];expected=[]
    for i in range(30):
     left,right=sorted([rng.randrange(n),rng.randrange(n)]);queries.append(f'{left} {right}');expected.append(str(min(values[left:right+1])))
    data=f'{n} {len(queries)}\n'+' '.join(map(str,values))+'\n'+'\n'.join(queries)+'\n'
   assert run(exe,data)==expected,(topic,case,data,expected)
  if topic=='bfs':boundaries=[('1 0\n0\n',['0']),('3 0\n2\n',['-1','-1','0']),('100000 99999\n'+'\n'.join(f'{i-1} {i}'for i in range(1,100000))+'\n0\n',list(map(str,range(100000))))]
  elif topic=='binary-search-answer':boundaries=[('1 1\n9223372036854775807\n',['9223372036854775807']),('3 1\n1000000000000000000 1000000000000000000 1000000000000000000\n',['3000000000000000000']),('5 5\n0 0 0 0 0\n',['0'])]
  elif topic=='prefix-sums-2d':boundaries=[('0 0 0\n',[]),('1 1 1\n-4000000000000000000\n0 0 0 0\n',['-4000000000000000000']),('2 2 1\n1000000000 1000000000\n1000000000 1000000000\n0 0 1 1\n',['4000000000'])]
  elif topic=='knapsack':boundaries=[('0 0\n',['0']),('1 0\n1 10\n',['0']),('3 3\n1 1000000000000000\n1 1000000000000000\n1 1000000000000000\n',['3000000000000000']),('1 3\n1 5\n',['5'])]
  elif topic=='lis':boundaries=[('0\n',['0']),('1\n-9223372036854775808\n',['1']),('1000\n'+'7 '*1000+'\n',['1']),('1000\n'+' '.join(map(str,range(1000)))+'\n',['1000'])]
  else:boundaries=[('1 1\n-9223372036854775808\n0 0\n',['-9223372036854775808']),('1 0\n0\n',[]),('100000 1\n'+'1 '*99999+'-1000000000000\n0 99999\n',['-1000000000000'])]
  for data,expected in boundaries:assert run(exe,data)==expected,(topic,'boundary')
  report['boundary_cases']=len(boundaries);reports.append(report)
report={'status':'passed','local_proposals_only':True,'seed':101027,'reviewed_blocks':24,'unique_programs':6,'samples':6,'oracle_cases':180,'boundary_cases':sum(r['boundary_cases']for r in reports),'programs':reports,'oracle_methods':['Floyd-Warshall distances plus parent-path certificate','all contiguous partitions','direct rectangle-cell summation','all item subsets','all increasing subsequences','direct range minima'],'extra_harness':'BFS helper parent reconstruction compiled separately and checked on each random graph;not an additional published program.','limits':'Retained tutorial references tested locally;no publication or production edit.'};(ROOT/'audit/PART04-TUTORIAL-CPP-TESTS02.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='programs'})
