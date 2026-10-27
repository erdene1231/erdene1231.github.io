"""Independent factorization, simulation/lifting, coloring enumeration and circular-slice checks."""
import hashlib,itertools,json,random,subprocess,tempfile
from array import array
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));records=json.load(open(root/'audit/PART04-CONTENT07-SAMPLES.json'));rng=random.Random(71027);results=[]
def distinct_factors(value):
 count=0;divisor=2
 while divisor*divisor<=value:
  if value%divisor==0:
   count+=1
   while value%divisor==0:value//=divisor
  divisor+=1
 return count+(value>1)
def advance(value):return (value+sum(map(int,str(value))))%100000
def circular_exists(values):
 total=sum(values)
 for left in range(len(values)):
  current=0
  for length in range(1,len(values)+1):
   current+=values[(left+length-1)%len(values)]
   if current*10==total:return 'Yes'
 return 'No'
with tempfile.TemporaryDirectory()as tmp:
 for record in records:
  suffix=record['ref'].split('_')[-1];row=next(p for p in rows if p['ref']==record['ref']);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code)
  built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr
  cases=[(s['input'],s['output'])for s in record['samples']]
  for _ in range(40):
   if suffix=='ad':
    n=rng.randint(2,400);required=rng.randint(1,8);inp=f'{n} {required}\n';expected=str(sum(distinct_factors(v)>=required for v in range(2,n+1)))
   elif suffix=='bf':
    initial=rng.randrange(100000);steps=rng.randint(1,2000);value=initial
    for step in range(steps):value=advance(value)
    inp=f'{initial} {steps}\n';expected=str(value)
   elif suffix=='bq':
    n=rng.randint(1,6);colors=rng.randint(1,5);expected=str(sum(all(c[i]!=c[j]for i in range(n)for j in range(i+1,min(n,i+3)))for c in itertools.product(range(colors),repeat=n)));inp=f'{n} {colors}\n'
   else:
    n=rng.randint(1,14);values=[rng.randint(1,20)for i in range(n)];inp=f'{n}\n'+' '.join(map(str,values))+'\n';expected=circular_exists(values)
   cases.append((inp,expected))
  if suffix=='ad':focused=[('10000000 1\n','9999999'),('10000000 8\n','1'),('2 8\n','0')]
  elif suffix=='bf':
   # Independent transition squaring for a huge step count; no cycle detection/reduction.
   jump=array('I',(advance(v)for v in range(100000)));steps=10**18;state=42;remaining=steps
   while remaining:
    if remaining&1:state=jump[state]
    remaining>>=1
    if remaining:jump=array('I',(jump[jump[v]]for v in range(100000)))
   focused=[('99999 1\n','44'),('0 1000000000000000000\n','0'),(f'42 {steps}\n',str(state))]
  elif suffix=='bq':focused=[('1 1000000000\n','1000000000'),('2 1\n','0'),('2 2\n','2'),('3 2\n','0'),('1000000000000000000 3\n','6')]
  else:focused=[('1\n10\n','No'),('3\n2 36 2\n','Yes'),('4\n2 18 2 18\n','No'),('100000\n'+'1000000000 '*100000+'\n','Yes')]
  cases+=focused
  for inp,out in cases:
   run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=8);assert run.returncode==0 and run.stdout.split()==out.split(),(suffix,inp[:200],run.stdout[:200],out[:200])
  results.append({'ref':record['ref'],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'official_samples':len(record['samples']),'independent_oracles':40,'focused_boundary_cases':len(focused),'warnings':0,'status':'passed'})
(root/'audit/PART04-CONTENT07-CPP.json').write_text(json.dumps({'status':'passed','seed':71027,'programs':results,'oracle_methods':['individual trial-division distinct factor counts','direct decimal-state simulation;huge-K transition squaring without cycle detection','all small color assignments','all circular starting positions and lengths with ten-times-integer equality'],'limits':'Local executable checks; no judge submission.'},indent=2)+'\n');print(results)
