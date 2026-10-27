"""Six retained tutorial programs: independent oracles, semantic orders, sentinel repro."""
import concurrent.futures,hashlib,itertools,json,math,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ids=['binary-search','bitmask-dp','grid-dp','monotonic-stack','prefix-sums','topological-sort'];rng=random.Random(111027)
rows=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from'node:fs';import{proposedTutorialRows}from'./tools/part04_tutorial_proposals.mjs';process.stdout.write(JSON.stringify(proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials)));"],cwd=ROOT,text=True));reports=[]
def run(exe,data):return subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=6).stdout.split()
def compile_code(code,src,exe,extra=()):
 src.write_text(code);result=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',*extra,str(src),'-o',str(exe)],capture_output=True,text=True);assert result.returncode==0 and not result.stderr,result.stderr

def has_order(n,edges):
 for permutation in itertools.permutations(range(n)):
  position=[0]*n
  for i,v in enumerate(permutation):position[v]=i
  if all(position[a]<position[b]for a,b in edges):return True
 return False

def check_order(tokens,n,edges,possible):
 if not possible:assert tokens==['CYCLE'],tokens;return
 order=list(map(int,tokens));assert len(order)==n and sorted(order)==list(range(n)),tokens;position=[0]*n
 for i,v in enumerate(order):position[v]=i
 assert all(position[a]<position[b]for a,b in edges)
def graph_input(n,edges):return f'{n} {len(edges)}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+'\n'
with tempfile.TemporaryDirectory(prefix='part04-tutorial-cpp03-')as tmp:
 def build(topic):
  doc=next(r['body']for r in rows if r['body']['id']==topic);codes=lambda d:[b['text']for s in d['sections']for b in s['blocks']if b['type']=='code'and b.get('language')=='C++17'];mn,en=codes(doc),codes(doc['translations']['en']);assert mn==en and len(mn)==2,topic;helper,program=mn
  assert program[:program.index('int main(')].strip()==helper.strip();assert '\t'not in program;assert all(not line.startswith(' ')or(len(line)-len(line.lstrip()))%4==0 for line in program.splitlines())
  exe=Path(tmp)/topic;compile_code(program,Path(tmp)/(topic+'.cpp'),exe)
  blocks=[b for s in doc['sections']for b in s['blocks']];sample_input=next(b['text']for b in blocks if b['type']=='code'and b.get('language')=='Input');sample_output=next(b['text']for b in blocks if b['type']=='code'and b.get('language')=='Output');assert run(exe,sample_input)==sample_output.split()
  return topic,exe,helper,{'id':topic,'reviewed_blocks':4,'unique_program_sha256':hashlib.sha256(program.encode()).hexdigest(),'helper_sha256':hashlib.sha256(helper.encode()).hexdigest(),'both_languages_identical':True,'helper_is_exact_program_prefix':True,'compile_warnings':0,'samples':1,'oracle_cases':30}
 with concurrent.futures.ThreadPoolExecutor(2)as pool:built=list(pool.map(build,ids))
 topo_helper=next(h for t,e,h,r in built if t=='topological-sort');topo_exe=Path(tmp)/'topo-contract'
 compile_code(topo_helper+r'''
int main() {
    int n, edgeCount;
    cin >> n >> edgeCount;
    vector<vector<int>> neighbors(n);
    for (int i = 0; i < edgeCount; ++i) {
        int from, to;
        cin >> from >> to;
        neighbors[from].push_back(to);
    }
    vector<int> order{12345};
    bool valid = topological(neighbors, order);
    cout << valid << ' ' << order.size() << ' ';
    for (int vertex : order) cout << vertex << ' ';
}
''',Path(tmp)/'topo-contract.cpp',topo_exe)
 grid_helper=next(h for t,e,h,r in built if t=='grid-dp');grid_exe=Path(tmp)/'grid-contract';compile_code(grid_helper+'\nint main() { cout << grid_paths({}) << " " << grid_paths(vector<string>{""}); }\n',Path(tmp)/'grid-contract.cpp',grid_exe);assert run(grid_exe,'')==['0','0']
 old_doc=next(r['body']for r in json.load(open(ROOT/'audit/PART04-BASELINE.json'))['tutorials']if r['body']['id']=='bitmask-dp');old_code=next(b['text']for s in old_doc['sections']for b in s['blocks']if b['type']=='code'and b.get('language')=='C++17'and 'int main('in b['text']);old_exe=Path(tmp)/'assignment-original';compile_code(old_code,Path(tmp)/'assignment-original.cpp',old_exe,('-fsanitize=undefined','-fno-sanitize-recover=undefined'))
 overflow_input='2\n0 9223372036854775807\n9223372036854775807 0\n';old_run=subprocess.run([str(old_exe)],input=overflow_input,capture_output=True,text=True);assert old_run.returncode!=0 and 'signed integer overflow'in old_run.stderr
 assert run(next(e for t,e,h,r in built if t=='bitmask-dp'),overflow_input)==['0']
 for topic,exe,helper,report in built:
  for case in range(30):
   if topic=='binary-search':
    n=rng.randint(0,30);values=sorted(rng.randint(-10,10)for i in range(n));queries=[rng.randint(-12,12)for i in range(30)];expected=[str(next((i for i,v in enumerate(values)if v>=target),n))for target in queries];data=f'{n}\n'+' '.join(map(str,values))+f'\n{len(queries)}\n'+' '.join(map(str,queries))+'\n'
   elif topic=='bitmask-dp':
    n=rng.randint(0,7);cost=[[rng.choice([rng.randint(0,100),9223372036854775807])for j in range(n)]for i in range(n)]
    for i in range(n):cost[i][i]=rng.randint(0,100)
    optimum=min((sum(cost[i][job]for i,job in enumerate(permutation))for permutation in itertools.permutations(range(n))),default=0);expected=[str(optimum)];data=f'{n}\n'+'\n'.join(' '.join(map(str,row))for row in cost)+'\n'
   elif topic=='grid-dp':
    n=rng.randint(1,6);m=rng.randint(1,6);grid=[''.join(rng.choice('...#')for c in range(m))for r in range(n)];count=0
    for down_positions in itertools.combinations(range(n+m-2),n-1):
     down=set(down_positions);row=column=0;valid=grid[0][0]!='#'
     for step in range(n+m-2):
      if step in down:row+=1
      else:column+=1
      valid=valid and grid[row][column]!='#'
     count+=valid
    expected=[str(count%1000000007)];data=f'{n} {m}\n'+'\n'.join(grid)+'\n'
   elif topic=='monotonic-stack':
    n=rng.randint(0,30);values=[rng.randint(-10,10)for i in range(n)];expected=[str(next((j for j in range(i+1,n)if values[j]>values[i]),-1))for i in range(n)];data=f'{n}\n'+' '.join(map(str,values))+'\n'
   elif topic=='prefix-sums':
    n=rng.randint(1,30);values=[rng.randint(-10**10,10**10)for i in range(n)];queries=[];expected=[]
    for i in range(30):
     left,right=sorted([rng.randrange(n),rng.randrange(n)]);queries.append(f'{left} {right}');expected.append(str(sum(values[left:right+1])))
    data=f'{n} {len(queries)}\n'+' '.join(map(str,values))+'\n'+'\n'.join(queries)+'\n'
   else:
    n=rng.randint(0,7);edges=[(a,b)for a in range(n)for b in range(n)if rng.randrange(5)==0]
    if edges and rng.randrange(2):edges.append(rng.choice(edges))
    possible=has_order(n,edges);data=graph_input(n,edges);check_order(run(exe,data),n,edges,possible);certificate=run(topo_exe,data);assert certificate[0]==str(int(possible));size=int(certificate[1]);assert size==len(certificate[2:])
    if possible:check_order(certificate[2:],n,edges,True)
    else:assert size==0
    continue
   assert run(exe,data)==expected,(topic,case,data,expected)
  if topic=='binary-search':boundaries=[('0\n3\n-1 0 9223372036854775807\n',['0']*3),('5\n4 4 4 4 4\n3\n4 3 5\n',['0','0','5']),('2\n-9223372036854775808 9223372036854775807\n3\n-9223372036854775808 0 9223372036854775807\n',['0','1','1']),('100000\n'+' '.join(map(str,range(100000)))+'\n3\n99999 100000 50000\n',['99999','100000','50000'])]
  elif topic=='bitmask-dp':boundaries=[('0\n',['0']),(overflow_input,['0']),('1\n3999999999999999999\n',['3999999999999999999']),('20\n'+'\n'.join(' '.join('0'if i==j else'9223372036854775807'for j in range(20))for i in range(20))+'\n',['0'])]
  elif topic=='grid-dp':boundaries=[('1 1\n.\n',['1']),('1 1\n#\n',['0']),('2 2\n..\n.#\n',['0']),('1 1000\n'+'.'*1000+'\n',['1']),('100 100\n'+('.'*100+'\n')*100,[str(math.comb(198,99)%1000000007)])]
  elif topic=='monotonic-stack':boundaries=[('0\n',[]),('5\n7 7 7 7 7\n',['-1']*5),('100000\n'+' '.join(map(str,[*range(99999,0,-1),100000]))+'\n',['99999']*99999+['-1']),('4\n-9223372036854775808 9223372036854775807 9223372036854775807 -9223372036854775808\n',['1','-1','-1','-1'])]
  elif topic=='prefix-sums':boundaries=[('0 0\n',[]),('1 1\n-9223372036854775808\n0 0\n',['-9223372036854775808']),('2 3\n9223372036854775807 -9223372036854775807\n0 0\n1 1\n0 1\n',['9223372036854775807','-9223372036854775807','0']),('100000 1\n'+'1000000000 '*100000+'\n0 99999\n',['100000000000000'])]
  else:
   graphs=[(0,[],True),(1,[(0,0)],False),(3,[(0,1),(0,1),(1,2)],True),(3,[(0,1),(1,0),(1,2)],False),(100000,[(i-1,i)for i in range(1,100000)],True)]
   for n,edges,possible in graphs:check_order(run(exe,graph_input(n,edges)),n,edges,possible)
   report['boundary_cases']=len(graphs);reports.append(report);continue
  for data,expected in boundaries:assert run(exe,data)==expected,(topic,'boundary')
  report['boundary_cases']=len(boundaries);reports.append(report)
report={'status':'passed','local_proposals_only':True,'seed':111027,'reviewed_blocks':24,'unique_programs':6,'samples':6,'oracle_cases':180,'boundary_cases':sum(p['boundary_cases']for p in reports),'helper_contract_cases':2,'programs':reports,'oracle_methods':['linear first-qualifying scan','all job permutations using arbitrary-precision sums','all right/down step sequences','direct first-greater scan','direct interval sums','all vertex permutations plus semantic edge-order validation'],'helper_harnesses':['Topological bool result,preseeded output replacement and cleared partial order checked on random graphs','Grid empty/zero-width helper guards checked independently of positive-dimension public driver'],'sentinel_repro':{'original_baseline_program_sha256':hashlib.sha256(old_code.encode()).hexdigest(),'input':overflow_input,'original_result':'UBSan signed integer overflow','proposal_result':'0;minimum remains below4e18 despite expensive unused edges','contract_note':'Clarifies ambiguous original cost bound to minimum<sentinel;does not claim this input satisfies an interpretation requiring every possible assignment total<sentinel.'},'limits':'Retained tutorial code tested locally;no publication/production edit. Extra harnesses are not additional published programs.'};(ROOT/'audit/PART04-TUTORIAL-CPP-TESTS03.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='programs'})
