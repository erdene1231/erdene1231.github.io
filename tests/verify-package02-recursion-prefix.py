"""Two lesson programs, physical Hanoi simulation/BFS and direct range sums."""
import collections,hashlib,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
def minimum_hanoi(n):
 start=(0,)*n;goal=(2,)*n;queue=collections.deque([(start,0)]);seen={start}
 while queue:
  state,distance=queue.popleft()
  if state==goal:return distance
  tops=[next((i for i,p in enumerate(state)if p==peg),n)for peg in range(3)]
  for source in range(3):
   for target in range(3):
    if source!=target and tops[source]<tops[target]:
     nxt=list(state);nxt[tops[source]]=target;nxt=tuple(nxt)
     if nxt not in seen:seen.add(nxt);queue.append((nxt,distance+1))
with tempfile.TemporaryDirectory()as tmp:
 for id in ['recursion','prefix-sums']:
  body=json.loads((ROOT/'audit/package02-lessons'/f'{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]
  assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17'];code=pieces[-1]
  src=Path(tmp)/(id+'.cpp');exe=Path(tmp)/id;src.write_text(code)
  result=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(src),'-o',str(exe)],capture_output=True,text=True,check=True);assert not result.stderr,result.stderr
  def run(text,path=exe):return subprocess.run([str(path)],input=text,capture_output=True,text=True,timeout=8,check=True).stdout.split()
  cases=0
  if id=='recursion':
   bfs=[]
   for n in range(17):
    output=list(map(int,run(str(n)+'\n')));count=output[0];assert count==2**n-1 and len(output)==1+2*count
    pegs=[list(range(n,0,-1)),[],[]]
    for source,target in zip(output[1::2],output[2::2]):
     assert 1<=source<=3 and 1<=target<=3 and source!=target
     assert pegs[source-1];disk=pegs[source-1].pop();assert not pegs[target-1]or pegs[target-1][-1]>disk;pegs[target-1].append(disk)
    assert pegs==[[],[],list(range(n,0,-1))]
    if n<=6:assert count==minimum_hanoi(n);bfs.append(n)
    cases+=1
   oracle='Every move physically simulated for n=0..16; independent shortest-path BFS on legal configurations for n=0..6'
  else:
   arrays=[[],[0],[10**9],[-10**9],[4,-2,7,0,3],[10**9]*200000,[-10**9]*200000,[-10**9,10**9]*100000]+[[rng.randrange(-10**9,10**9+1)for _ in range(rng.randrange(1,70))]for _ in range(100)]
   for values in arrays:
    n=len(values)
    queries=[(l,r)for l in range(n)for r in range(l+1,n+1)]if n<70 else [(0,n),(0,1),(n-1,n)]+[(lambda a,b:(min(a,b),max(a,b)+1))(rng.randrange(n),rng.randrange(n))for _ in range(100)]
    text=f'{n} {len(queries)}\n'+' '.join(map(str,values))+'\n'+''.join(f'{l+1} {r}\n'for l,r in queries)
    assert list(map(int,run(text)))==[sum(values[l:r])for l,r in queries];cases+=len(queries)
   # Maximum query count: independently derived alternating +/- array sums.
   n=200000;values=[-10**9,10**9]*(n//2);queries=[(i%n,n)for i in range(200000)]
   text=f'{n} {len(queries)}\n'+' '.join(map(str,values))+'\n'+''.join(f'{l+1} {r}\n'for l,r in queries)
   assert list(map(int,run(text)))==[0 if l%2==0 else 10**9 for l,r in queries];cases+=len(queries)
   harness=Path(tmp)/'prefix-helper.cpp';helper=Path(tmp)/'prefix-helper';harness.write_text('#define main lesson_main\n'+code+'\n#undef main\nint main() { vector<long long> a={4,-2,7,0,3}; auto p=build_prefix(a); if (p!=vector<long long>{0,4,2,9,9,12}) return 1; for (int i=0;i<=5;++i) if(range_sum(p,i,i)!=0) return 2; return 0; }\n');subprocess.run(['g++','-std=c++17','-Wall','-Wextra','-pedantic',str(harness),'-o',str(helper)],capture_output=True,text=True,check=True);subprocess.run([str(helper)],check=True)
   oracle='Direct Python addition over all intervals of small signed arrays; large full/first/last/random ranges; 200000-query independent alternating-array formula; empty helper ranges'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split()
  reports.append({'lesson':id,'program_sha256':hashlib.sha256(code.encode()).hexdigest(),'compile_warnings':0,'cases':cases,'sample_passed':True,'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Programs, exact fragment concatenation and declared bounds; semantic/editor/publication gates separate'}
(ROOT/'audit/PACKAGE02-RECURSION-PREFIX-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
