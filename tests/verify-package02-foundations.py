"""Three lesson references; independent exhaustive/counting oracles, local only."""
import json,subprocess,tempfile,random,itertools,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
rows=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import fs from'node:fs';import{proposedTutorialRows}from'./tools/package02_tutorial_proposals.mjs';console.log(JSON.stringify(proposedTutorialRows(JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).tutorials)))"],cwd=ROOT,text=True))
with tempfile.TemporaryDirectory()as tmp:
 for name in['binary-search','greedy','dynamic-programming']:
  b=next(r['body']for r in rows if r['id']==name);code=next(x['text']for x in b['sections'][12]['blocks']if x.get('language')=='C++17');en=next(x['text']for x in b['translations']['en']['sections'][12]['blocks']if x.get('language')=='C++17');assert code==en
  src=Path(tmp)/(name+'.cpp');exe=Path(tmp)/name;src.write_text(code);built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(src),'-o',str(exe)],capture_output=True,text=True,check=True);assert not built.stderr,built.stderr
  def run(data):return subprocess.run([str(exe)],input=data,capture_output=True,text=True,check=True,timeout=5).stdout.split()
  cases=0
  if name=='binary-search':
   for values in[[],[-2**63,0,2**63-1],[4]*10]+[sorted(rng.randrange(-20,21)for _ in range(rng.randrange(40)))for _ in range(80)]:
    queries=[-2**63,2**63-1]+[rng.randrange(-25,26)for _ in range(20)];expected=[str(next((i for i,v in enumerate(values)if v>=x),len(values)))for x in queries];assert run(str(len(values))+'\n'+' '.join(map(str,values))+'\n'+str(len(queries))+'\n'+' '.join(map(str,queries)))==expected;cases+=1
  elif name=='greedy':
   for intervals in[[],[(-2**63,-2**63+1),(0,1),(1,2**63-1)],[(1,2),(1,2),(2,3)]]+[[tuple(sorted(rng.sample(range(-5,12),2)))for _ in range(rng.randrange(10))]for _ in range(80)]:
    best=0
    for mask in range(1<<len(intervals)):
     chosen=[v for i,v in enumerate(intervals)if mask>>i&1]
     if all(a[1]<=b[0]or b[1]<=a[0]for a,b in itertools.combinations(chosen,2)):best=max(best,len(chosen))
    assert run(str(len(intervals))+'\n'+'\n'.join(f'{a} {b}'for a,b in intervals))==[str(best)];cases+=1
  else:
   # Distinct oracle: choose positions of two-steps among all steps, not a DP recurrence.
   import math
   for n in list(range(30))+[100,1000,1000000]:
    if n==1000000:
     # Fast doubling Fibonacci as an independent large-bound oracle.
     def fib(k):
      if k==0:return(0,1)
      a,b=fib(k//2);c=a*((2*b-a)%1000000007)%1000000007;d=(a*a+b*b)%1000000007;return(d,(c+d)%1000000007)if k%2 else(c,d)
     value=fib(n+1)[0]
    else:value=sum(math.comb(n-t,t)for t in range(n//2+1))%1000000007
    assert run(str(n))==[str(value)];cases+=1
  reports.append({'lesson':name,'program_sha256':hashlib.sha256(code.encode()).hexdigest(),'both_languages_identical':True,'compile_warnings':0,'independent_cases':cases})
report={'status':'passed','scope':'Local reference code contracts only;not full semantic/mastery/browser completion','programs':reports};(ROOT/'audit/PACKAGE02-FOUNDATIONS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
