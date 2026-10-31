"""Six sequence/structure programs: strictness, boundaries, bases and huge exponents."""
import json,subprocess,random,time,hashlib,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch07-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_bh','typical90_bi','typical90_bl','typical90_bo','typical90_bq','typical90_br'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(397);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0;edge_checks=[]
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='typical90_bh':
  def bitonic(a):
   falling=False
   for x,y in zip(a,a[1:]):
    if x==y:return False
    if x>y:falling=True
    elif falling:return False
   return True
  for _ in range(180):
   n=rng.randint(1,12);a=[rng.randint(1,n)for __ in range(n)];best=max(len(sub)for mask in range(1,1<<n)if bitonic(sub:=[a[i]for i in range(n)if mask>>i&1]));assert run(f'{n}\n'+' '.join(map(str,a))+'\n')==[str(best)];naive+=1
  n=300000
  for a,expected in [(range(1,n+1),n),(range(n,0,-1),n),([1]*n,1)]:assert run(f'{n}\n'+' '.join(map(str,a))+'\n')==[str(expected)]
  edge_checks.append('strict duplicates, peak at first/last;all subsequences oracle;N300000 monotone/reversed/equal')
 elif ref=='typical90_bi':
  for _ in range(200):
   q=rng.randint(2,100);x=rng.randint(1,10**9);deck=[x];ops=[f'1 {x}'];expected=[]
   for __ in range(q-2):
    t=rng.randint(1,3)
    if t==1:x=rng.randint(1,10**9);deck.insert(0,x);ops.append(f'1 {x}')
    elif t==2:x=rng.randint(1,10**9);deck.append(x);ops.append(f'2 {x}')
    else:k=rng.randint(1,len(deck));ops.append(f'3 {k}');expected.append(str(deck[k-1]))
   k=rng.randint(1,len(deck));ops.append(f'3 {k}');expected.append(str(deck[k-1]));assert run(f'{q}\n'+'\n'.join(ops)+'\n')==expected;naive+=1
  q=100000;assert run(f'{q}\n'+'\n'.join(f'2 {i}'for i in range(1,q))+f'\n3 {q-1}\n')==[str(q-1)];edge_checks.append('atleastone insertion/read;top/bottom and nondestructive reads;Q100000 indexed access')
 elif ref=='typical90_bl':
  for _ in range(200):
   n=rng.randint(1,30);q=rng.randint(1,50);a=[rng.choice([-10**9,0,10**9,rng.randint(-20,20)])for __ in range(n)];current=a[:];ops=[];expected=[]
   for __ in range(q):
    l=rng.randint(1,n);r=rng.randint(l,n);v=rng.choice([-10**9,0,10**9,rng.randint(-20,20)]);ops.append(f'{l} {r} {v}')
    for i in range(l-1,r):current[i]+=v
    expected.append(str(sum(abs(x-y)for x,y in zip(current,current[1:]))))
   assert run(f'{n} {q}\n'+' '.join(map(str,a))+'\n'+'\n'.join(ops)+'\n')==expected;naive+=1
  assert run('1 3\n1\n1 1 1000000000\n1 1 -1000000000\n1 1 0\n')==['0']*3;n=q=100000;assert run(f'{n} {q}\n'+'0 '*n+'\n'+f'1 {n} 1000000000\n'*q)==['0']*q;assert run('3 100000\n0 0 0\n'+'2 2 1000000000\n'*100000)==[str(2*i*10**9)for i in range(1,100001)];edge_checks.append('N1,negative/zero updates,full range,two boundary signs;N/Q1e5 and2e14 accumulated variation')
 elif ref=='typical90_bo':
  def convert(s):
   value=int(s,8);digits=[]
   while value:value,digit=divmod(value,9);digits.append(str(digit))
   return(''.join(reversed(digits))or'0').replace('8','5')
  for _ in range(180):
   value=rng.randrange(8**20);s=format(value,'o');k=rng.randint(1,100);expected=s
   for __ in range(k):
    previous=int(expected,8);expected=convert(expected);assert int(expected,8)<=previous and set(expected)<=set('01234567')
   assert run(f'{s} {k}\n')==[expected];naive+=1
  for s,k,expected in [('0',100,'0'),('10',1,'5'),('100',2,'63'),('7',100,'7')]:assert run(f'{s} {k}\n')==[expected]
  s='7'*20;expected=s
  for _ in range(100):expected=convert(expected)
  assert run(f'{s} 100\n')==[expected];edge_checks.append('source octal numeric value<8^20=2^60;zero,all8->5 replacement,reparse asbase8;arbitrary-integer reference')
 elif ref=='typical90_bq':
  mod=1000000007
  for n in range(1,8):
   for k in range(1,5):
    expected=sum(all(a[i]!=a[j]for i in range(n)for j in[i+1,i+2]if j<n)for a in itertools.product(range(k),repeat=n));assert run(f'{n} {k}\n')==[str(expected%mod)];naive+=1
  states=[(a,b)for a in range(4)for b in range(4)if a!=b];index={s:i for i,s in enumerate(states)};m=len(states);matrix=[[0]*m for _ in range(m)]
  for i,(a,b)in enumerate(states):
   for c in range(4):
    if c not in[a,b]:matrix[i][index[b,c]]+=1
  def mul(a,b):return[[sum(a[i][k]*b[k][j]for k in range(m))%mod for j in range(m)]for i in range(m)]
  def vecmul(v,a):return[sum(v[i]*a[i][j]for i in range(m))%mod for j in range(m)]
  n=10**18;e=n-2;v=[1]*m
  while e:
   if e&1:v=vecmul(v,matrix)
   matrix=mul(matrix,matrix);e//=2
  assert run(f'{n} 4\n')==[str(sum(v)%mod)]
  for k,expected in [(1,0),(2,0),(3,6),(10**9,(10**9*(10**9-1)*pow(10**9-2,n-2,mod))%mod)]:assert run(f'{n} {k}\n')==[str(expected)]
  assert run('1 1000000000\n')==['1000000000'];assert run('2 1000000000\n')==[str(10**9*(10**9-1)%mod)];edge_checks.append('N1/N2,K1/K2;all small colourings;independent12-state transfer matrix atN1e18;largeK products')
 else:
  for _ in range(180):
   n=rng.randint(1,12);points=[(rng.randint(-8,8),rng.randint(-8,8))for __ in range(n)];expected=min(sum(abs(x-a)+abs(y-b)for a,b in points)for x in range(min(a for a,b in points),max(a for a,b in points)+1)for y in range(min(b for a,b in points),max(b for a,b in points)+1));assert run(f'{n}\n'+'\n'.join(f'{x} {y}'for x,y in points)+'\n')==[str(expected)];naive+=1
  assert run('3\n0 4\n2 0\n4 2\n')==['8'];n=100000;assert run(f'{n}\n'+'-1000000000 -1000000000\n'*(n//2)+'1000000000 1000000000\n'*(n//2))==[str(2*10**14)];edge_checks.append('negative/repeated points,N1/evenN;facility neednot be input point;brute integer-grid oracle;2e14 total')
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'source_edge_contract_checks':edge_checks,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Code checks only; bilingual/native content reviewed separately. Oracles use full subsequences, naive lists/height updates, arbitrary-integer source base conversion, full colour assignments/transfer matrix and facility-grid enumeration. Host timing is not a judge-runtime claim.'};(ROOT/'audit/native-problem-editorials/batch07-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
