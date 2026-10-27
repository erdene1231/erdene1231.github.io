import json,subprocess,tempfile,hashlib,random,itertools,math
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));records=json.load(open(root/'audit/PART04-CONTENT05-SAMPLES.json'));rng=random.Random(51027);results=[]
with tempfile.TemporaryDirectory()as tmp:
 for record in records:
  suffix=record['ref'].split('_')[-1];row=next(p for p in rows if p['ref']==record['ref']);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code);built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr
  cases=[(s['input'],s['output'])for s in record['samples']]
  for _ in range(30):
   if suffix=='ax':
    n=rng.randint(2,35);length=rng.randint(2,40);expected=sum(math.comb(n-(length-1)*b,b)for b in range(n//length+1))%1000000007;inp=f'{n} {length}\n'
   elif suffix=='at':
    n=rng.randint(1,7);a=[[rng.randrange(100)for i in range(n)]for j in range(3)];expected=sum((x+y+z)%46==0 for x in a[0]for y in a[1]for z in a[2]);inp=str(n)+'\n'+'\n'.join(' '.join(map(str,v))for v in a)+'\n'
   elif suffix=='az':
    n=rng.randint(1,4);a=[sorted(rng.sample(range(1,101),6))for i in range(n)];expected=sum(math.prod(v)for v in itertools.product(*a))%1000000007;inp=str(n)+'\n'+'\n'.join(' '.join(map(str,v))for v in a)+'\n'
   else:
    n=rng.randint(1,8);points=[(rng.randint(-3,3),rng.randint(-3,3))for i in range(n)];expected=min(sum(abs(x-a)+abs(y-b)for a,b in points)for x in range(-3,4)for y in range(-3,4));inp=str(n)+'\n'+'\n'.join(f'{x} {y}'for x,y in points)+'\n'
   cases.append((inp,str(expected)))
  if suffix=='ax':cases.append(('100000 100000\n','2'))
  elif suffix=='at':cases.append(('100000\n'+('0 '*99999+'0\n')*3,str(100000**3)))
  elif suffix=='az':cases.append(('100\n'+'1 2 3 4 5 6\n'*100,str(pow(21,100,1000000007))))
  else:cases.append(('2\n-1000000000 -1000000000\n1000000000 1000000000\n','4000000000'))
  for inp,out in cases:
   run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=3);assert run.returncode==0 and run.stdout.split()==out.split(),(suffix,inp,run.stdout,out)
  results.append({'ref':record['ref'],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'official_samples':len(record['samples']),'independent_oracles':30,'boundary_cases':1,'warnings':0,'status':'passed'})
(root/'audit/PART04-CONTENT05-CPP.json').write_text(json.dumps({'status':'passed','seed':51027,'programs':results,'oracle_methods':['binomial count of long-jump positions','direct index triple enumeration','all die outcomes','all integer locations in small coordinate hull; median proof covers real optimum'],'limits':'Local executable checks; no judge submission.'},indent=2)+'\n');print(results)
