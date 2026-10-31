"""Six numeric/query programs with independent exact oracles and boundary checks."""
import json,subprocess,random,time,hashlib,math,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch05-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_aj','typical90_al','typical90_am','typical90_ap','typical90_ar','typical90_at'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(395);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0;edge_checks=[]
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=20);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='typical90_aj':
  pool=[(x,y)for x in range(-12,13)for y in range(-12,13)]
  for _ in range(200):
   n=rng.randint(2,30);points=rng.sample(pool,n);q=rng.randint(1,n);queries=rng.sample(range(n),q);expected=[str(max(abs(points[k][0]-x)+abs(points[k][1]-y)for x,y in points))for k in queries];text=f'{n} {q}\n'+'\n'.join(f'{x} {y}'for x,y in points)+'\n'+'\n'.join(str(k+1)for k in queries)+'\n';assert run(text)==expected;naive+=1
  assert run('2 2\n-1000000000 -1000000000\n1000000000 1000000000\n1\n2\n')==['4000000000','4000000000'];n=100000;assert run(f'{n} {n}\n'+'\n'.join(f'{i} {-i}'for i in range(n))+'\n'+'\n'.join(str(i+1)for i in range(n))+'\n')==[str(2*max(i,n-1-i))for i in range(n)];edge_checks.append('distinct points and query indices; negative coordinates;4e9 distance; fullN/Q')
 elif ref=='typical90_al':
  pairs=[(10**18,1),(10**18,10**18),(10**18,2),(10**18,10**18-1),(10**9,10**9-1),(10**9,10**9+1),(10**18,5*10**17)]
  for a,b in pairs+[(rng.choice([1,rng.randint(1,10**9),rng.randint(1,10**18)]),rng.choice([1,rng.randint(1,10**9),rng.randint(1,10**18)]))for _ in range(300)]:
   value=math.lcm(a,b);assert run(f'{a} {b}\n')==['Large'if value>10**18 else str(value)];naive+=1
  edge_checks.append('LCM exactly1e18 is numeric; just-over threshold; raw product can exceed64bits; Python arbitrary integers')
 elif ref=='typical90_am':
  for _ in range(220):
   n=rng.randint(2,30);edges=[(rng.randrange(v),v)for v in range(1,n)];g=[[]for __ in range(n)]
   for a,b in edges:g[a].append(b);g[b].append(a)
   answer=0
   for s in range(n):
    d=[-1]*n;d[s]=0;q=collections.deque([s])
    while q:
     u=q.popleft()
     for v in g[u]:
      if d[v]<0:d[v]=d[u]+1;q.append(v)
    answer+=sum(d[s+1:])
   assert run(f'{n}\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n')==[str(answer)];naive+=1
  n=100000
  for shape,expected in [('path',n*(n*n-1)//6),('star',(n-1)**2)]:
   edges=[(i-1,i)if shape=='path'else(0,i)for i in range(1,n)];assert run(f'{n}\n'+'\n'.join(f'{a+1} {b+1}'for a,b in edges)+'\n')==[str(expected)]
  edge_checks.append('unordered all-pairs BFS oracle;100000-vertex path/star formulas; iterative traversal and promoted pair contribution')
 elif ref=='typical90_ap':
  mod=1000000007
  def formula(k):
   if k%9:return 0
   total=0
   for length in range(1,k+1):
    for j in range(min(length,(k-length)//9)+1):total+=(-1)**j*math.comb(length,j)*math.comb(k-9*j-1,length-1)
   return total%mod
  for k in range(1,91):assert run(f'{k}\n')==[str(formula(k))];naive+=1
  def mul(a,b):return[[sum(a[i][k]*b[k][j]for k in range(9))%mod for j in range(9)]for i in range(9)]
  def matrix(k):
   a=[[1]*9]+[[int(j==i-1)for j in range(9)]for i in range(1,9)];result=[[int(i==j)for j in range(9)]for i in range(9)]
   while k:
    if k&1:result=mul(result,a)
    a=mul(a,a);k//=2
   return result[0][0]
  assert run('99999\n')==[str(matrix(99999))];assert run('100000\n')==['0'];edge_checks.append('bounded-positive-composition inclusion/exclusion oracle; nozero digits; modulo9 gate; independent9x9 matrix stress')
 elif ref=='typical90_ar':
  for _ in range(220):
   n=rng.randint(2,40);q=rng.randint(1,100);a=[rng.randint(1,10**9)for __ in range(n)];state=a[:];ops=[];expected=[]
   for __ in range(q):
    t=rng.randint(1,3)
    if t==1:
     x,y=rng.sample(range(n),2);state[x],state[y]=state[y],state[x];ops.append(f'1 {x+1} {y+1}')
    elif t==2:state=state[-1:]+state[:-1];ops.append('2 0 0')
    else:x=rng.randrange(n);ops.append(f'3 {x+1} 0');expected.append(str(state[x]))
   assert run(f'{n} {q}\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n')==expected;naive+=1
  n=200000;assert run(f'{n} {n}\n'+' '.join(map(str,range(1,n+1)))+'\n'+'2 0 0\n'*(n-1)+'3 1 0\n')==['2'];edge_checks.append('type2 zero dummy coordinates ignored; type3 y0; right rotation/wraparound; fullN/Q')
 else:
  for _ in range(220):
   n=rng.randint(1,15);a=[[rng.choice([0,10**9,rng.randint(0,100)])for __ in range(n)]for ___ in range(3)];expected=sum((x+y+z)%46==0 for x in a[0]for y in a[1]for z in a[2]);assert run(f'{n}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n')==[str(expected)];naive+=1
  n=100000;assert run(f'{n}\n'+('0 '*n+'\n')*3)==[str(n**3)];edge_checks.append('index triples with duplicate/zero values; independent raw triple enumeration;1e15 product promoted before multiplication')
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'source_edge_contract_checks':edge_checks,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Correctness checks for these source contracts; not prose/native completeness or judge timing. Large-count oracles use arbitrary integers, matrix exponentiation and closed-form tree sums independently of the submitted implementations.'};(ROOT/'audit/native-problem-editorials/batch05-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
