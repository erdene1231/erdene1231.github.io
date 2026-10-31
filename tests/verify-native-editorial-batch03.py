"""Six original programs: frozen source samples, independent oracles and source-bound stresses."""
import json,subprocess,itertools,random,time,hashlib,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch03-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_c','typical90_n','typical90_p','typical90_z','typical90_aa','typical90_ad'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(393);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=20);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 def independent(text,tokens):
  parts=list(map(int,text.split()));n=parts[0];edges=list(zip(parts[1::2],parts[2::2]));chosen=list(map(int,tokens));assert len(chosen)==n//2 and len(set(chosen))==len(chosen)and all(1<=v<=n for v in chosen);s=set(chosen);assert all(a not in s or b not in s for a,b in edges)
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:
  got=run(s['input'])
  if ref=='typical90_z':independent(s['input'],got)
  else:assert got==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref in ['typical90_c','typical90_z']:
  for _ in range(250):
   n=rng.randint(3,24)if ref=='typical90_c'else 2*rng.randint(1,12);edges=[(rng.randrange(v),v)for v in range(1,n)];rng.shuffle(edges);text=f'{n}\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n';got=run(text)
   if ref=='typical90_z':independent(text,got)
   else:
    g=[[]for _ in range(n)]
    for a,b in edges:g[a].append(b);g[b].append(a)
    best=0
    for s in range(n):
     dist=[-1]*n;dist[s]=0;q=collections.deque([s])
     while q:
      u=q.popleft()
      for v in g[u]:
       if dist[v]<0:dist[v]=dist[u]+1;q.append(v)
     best=max(best,max(dist)+1)
    assert got==[str(best)]
   naive+=1
  for shape in ['path','star']:
   n=100000;edges=[(v-1,v)if shape=='path'else(0,v)for v in range(1,n)];text=f'{n}\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n';got=run(text)
   if ref=='typical90_z':independent(text,got)
   else:assert got==[str(n if shape=='path'else 3)]
 elif ref=='typical90_n':
  for _ in range(180):
   n=rng.randint(1,7);a=rng.sample(range(30),n);b=rng.sample(range(30),n);expected=min(sum(abs(x-y)for x,y in zip(a,perm))for perm in itertools.permutations(b));assert run(f'{n}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n')==[str(expected)];naive+=1
  n=100000;a=range(n-1,-1,-1);b=range(10**9-n+1,10**9+1);assert run(f'{n}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n')==[str(n*(10**9-n+1))]
 elif ref=='typical90_p':
  for _ in range(180):
   n=rng.randint(1,300);coins=[1]+rng.sample(range(2,45),2);rng.shuffle(coins);dp=[0]+[10000]*n
   for value in range(1,n+1):dp[value]=1+min(dp[value-c]for c in coins if c<=value)
   assert run(f'{n}\n'+' '.join(map(str,coins))+'\n')==[str(dp[n])];naive+=1
  # Lower bound ceil(N/maxcoin)=9998;4998*10000+5000*10002=N attains it.
  assert run('99990000\n10000 10001 10002\n')==['9998']
 elif ref=='typical90_aa':
  for _ in range(220):
   n=rng.randint(1,100);pool=[''.join(rng.choice('abc012')for _ in range(rng.randint(1,15)))for __ in range(12)];names=[rng.choice(pool)for __ in range(n)];expected=[str(i+1)for i,s in enumerate(names)if s not in names[:i]];assert run(f'{n}\n'+'\n'.join(names)+'\n')==expected;naive+=1
  n=100000;assert run(f'{n}\n'+'\n'.join(f'u{i}'for i in range(n))+'\n')==list(map(str,range(1,n+1)))
 else:
  def factors(x):
   count=0;p=2
   while p*p<=x:
    if x%p==0:
     count+=1
     while x%p==0:x//=p
    p+=1
   return count+(x>1)
  for _ in range(180):
   n=rng.randint(2,600);k=rng.randint(1,8);expected=sum(factors(x)>=k for x in range(2,n+1));assert run(f'{n} {k}\n')==[str(expected)];naive+=1
  # The smallest8-prime product9699690 is valid; the next possible product exceeds1e7.
  assert 2*3*5*7*11*13*17*19==9699690 and 2*3*5*7*11*13*17*23>10**7
  assert run('10000000 8\n')==['1']
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'sample_comparison':'valid independent-set property, nonunique output'if ref=='typical90_z'else'exact output tokens','independent_naive_cases':naive,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Code correctness evidence only; original bilingual/native content reviewed separately. Independent-set outputs validated by cardinality, distinct/in-range vertices and every input edge, not one canonical answer.'};(ROOT/'audit/native-problem-editorials/batch03-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
