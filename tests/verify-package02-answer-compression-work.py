"""Implementation groundwork only; full lesson/editor/publication review remains pending."""
from pathlib import Path
import subprocess,tempfile,random,json,heapq,hashlib
root=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['binary-search-answer','hash-compression']:
  source=root/f'audit/package02-work/{id}.cpp';exe=Path(tmp)/id
  p=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(source),'-o',str(exe)],capture_output=True,text=True,check=True);assert not p.stderr,p.stderr
  def run(s):return list(map(int,subprocess.run([str(exe)],input=s,capture_output=True,text=True,timeout=15,check=True).stdout.split()))
  if id=='binary-search-answer':
   cases=[([3,2,5],7),([1],0),([10**9],10**9)]+[([rng.randint(1,20)for _ in range(rng.randint(1,10))],rng.randrange(100))for _ in range(200)]
   for times,target in cases:
    if target<=100:
     events=[(t,i)for i,t in enumerate(times)];heapq.heapify(events);answer=0
     for _ in range(target):answer,i=heapq.heappop(events);heapq.heappush(events,(answer+times[i],i))
    else:answer=10**18
    assert run(f'{len(times)} {target}\n'+' '.join(map(str,times))+'\n')==[answer]
   for times,target,answer in [([1]*200000,10**9,5000),([10**9]*200000,10**9,5000000000000),([10**9]*200000,0,0)]:assert run(f'{len(times)} {target}\n'+' '.join(map(str,times))+'\n')==[answer]
   count=len(cases)+3;oracle='Independent event-heap simulation for small targets; maximum-bound closed forms, including zero target and1e18answer'
  else:
   cases=[[],[100,-5,100,7],[0]*100,[-10**18,10**18]]+[[rng.randint(-20,20)for _ in range(rng.randrange(100))]for _ in range(200)]+[list(range(200000,0,-1))]
   for values in cases:
    out=run(str(len(values))+'\n'+' '.join(map(str,values))+'\n');size=out[0];ordered=out[1:1+size];ranks=out[1+size:];assert ordered==sorted(set(values));assert len(ranks)==len(values);assert [ordered[r-1]for r in ranks]==values
    if len(values)<1000:
     expected=[1+sum(other<value for other in set(values))for value in values];assert ranks==expected
   count=len(cases);oracle='Direct count-of-distinct-smaller rank oracle, exact inverse reconstruction and200000descending values'
  reports.append({'id':id,'cases':count,'warnings':0,'sanitizer':'passed','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'oracle':oracle})
report={'status':'Implementation groundwork passed; NOT full lesson completion','programs':reports,'remaining':['Full MN/EN15-section native documents','Practice/priority semantic review','Explained fragments then complete code','Native editor/reader checks','Fresh guarded publication']};(root/'audit/PACKAGE02-ANSWER-COMPRESSION-WORK-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
