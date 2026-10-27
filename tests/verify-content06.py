"""Compile original programs and compare with source samples and independent small oracles."""
import hashlib,json,random,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'))
records=json.load(open(root/'audit/PART04-CONTENT06-SAMPLES.json'))
rng=random.Random(61027)
def longest(values,limit):
 return max(right-left for left in range(len(values))for right in range(left+1,len(values)+1)if len(set(values[left:right]))<=limit)
def distances(points,queries):
 return '\n'.join(str(max(abs(x-a)+abs(y-b)for a,b in points))for q in queries for x,y in[points[q]])
def update_array(values,updates):
 heights=values[:];answers=[]
 for left,right,delta in updates:
  for i in range(left-1,right):heights[i]+=delta
  answers.append(str(sum(abs(a-b)for a,b in zip(heights,heights[1:]))))
 return '\n'.join(answers)
def interval_count(text):
 return sum(set(text[left:right])=={'o','x'}for left in range(len(text))for right in range(left+1,len(text)+1))
results=[]
with tempfile.TemporaryDirectory()as tmp:
 for record in records:
  suffix=record['ref'].split('_')[-1];row=next(r for r in rows if r['ref']==record['ref'])
  code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code')
  src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code)
  built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True)
  assert built.returncode==0 and not built.stderr,built.stderr
  cases=[(s['input'],s['output'])for s in record['samples']]
  for _ in range(50):
   if suffix=='ah':
    n=rng.randint(1,16);limit=rng.randint(1,n);a=[rng.randint(1,7)for i in range(n)]
    inp=f'{n} {limit}\n'+' '.join(map(str,a))+'\n';expected=str(longest(a,limit))
   elif suffix=='aj':
    points=rng.sample([(x,y)for x in range(-6,7)for y in range(-6,7)],rng.randint(2,15));queries=rng.sample(range(len(points)),rng.randint(1,len(points)))
    inp=f'{len(points)} {len(queries)}\n'+'\n'.join(f'{x} {y}'for x,y in points)+'\n'+'\n'.join(str(q+1)for q in queries)+'\n';expected=distances(points,queries)
   elif suffix=='bl':
    n=rng.randint(1,12);a=[rng.randint(-10,10)for i in range(n)];updates=[]
    for q in range(rng.randint(1,15)):
     left=rng.randint(1,n);updates.append((left,rng.randint(left,n),rng.randint(-20,20)))
    inp=f'{n} {len(updates)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(' '.join(map(str,q))for q in updates)+'\n';expected=update_array(a,updates)
   else:
    n=rng.randint(1,25);text=''.join(rng.choice('ox')for i in range(n));inp=f'{n}\n{text}\n';expected=str(interval_count(text))
   cases.append((inp,expected))
  if suffix=='ah':
   focused=[('100000 1\n'+'7 '*100000+'\n','100000'),('100000 100000\n'+' '.join(map(str,range(1,100001)))+'\n','100000'),('8 2\n1 2 1 3 3 2 2 2\n','5')]
  elif suffix=='aj':
   focused=[('3 3\n-1000000000 1000000000\n1000000000 -1000000000\n0 0\n1\n2\n3\n','4000000000\n4000000000\n2000000000'),('2 2\n-5 -5\n-4 -3\n2\n1\n','3\n3')]
   points=[(i,0)for i in range(100000)];queries=[0,99999];focused.append(('100000 2\n'+'\n'.join(f'{x} {y}'for x,y in points)+'\n1\n100000\n','99999\n99999'))
  elif suffix=='bl':
   focused=[('1 3\n-1000000000\n1 1 1000000000\n1 1 -1000000000\n1 1 0\n','0\n0\n0'),('2 3\n0 2\n1 1 3\n2 2 -4\n1 2 7\n','1\n5\n5'),('2 100000\n0 0\n'+'1 1 1000000000\n'*100000,'\n'.join(str(i*10**9)for i in range(1,100001)))]
  else:
   focused=[('1\no\n','0'),('1000000\n'+'ox'*500000+'\n',str(1000000*999999//2)),('1000000\n'+'o'*1000000+'\n','0')]
  cases+=focused
  for inp,out in cases:
   run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=5)
   assert run.returncode==0 and run.stdout.split()==out.split(),(suffix,inp[:300],run.stdout[:300],out[:300])
  results.append({'ref':record['ref'],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'official_samples':len(record['samples']),'independent_oracles':50,'focused_boundary_cases':len(focused),'warnings':0,'status':'passed'})
(root/'audit/PART04-CONTENT06-CPP.json').write_text(json.dumps({'status':'passed','seed':61027,'programs':results,'oracle_methods':['all contiguous intervals with independent distinct-value sets','direct pairwise Manhattan distances','explicit array mutation and adjacent summation','all substrings with two-symbol set predicate'],'limits':'Local executable checks; no judge submission.'},indent=2)+'\n')
print(results)
