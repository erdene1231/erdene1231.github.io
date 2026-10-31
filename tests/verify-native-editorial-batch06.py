"""Six greedy/DP/counting programs: prerequisite, witness and large-step oracles."""
import json,subprocess,random,time,hashlib,math,itertools
from array import array
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch06-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_av','typical90_ax','typical90_az','typical90_bc','typical90_bd','typical90_bf'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(396);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0;edge_checks=[]
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 def witness(text,tokens,possible=None):
  nums=list(map(int,text.split()));n,s=nums[:2];pairs=list(zip(nums[2::2],nums[3::2]));assert len(tokens)==1
  if possible is None:
   bits=1;mask=(1<<(s+1))-1
   for a,b in pairs:bits=((bits<<a)|(bits<<b))&mask
   possible=bool(bits>>s&1)
  if tokens==['Impossible']:assert not possible
  else:
   answer=tokens[0];assert possible and len(answer)==n and set(answer)<=set('AB');assert sum(pairs[i][int(c=='B')]for i,c in enumerate(answer))==s
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:
  got=run(s['input'])
  if ref=='typical90_bd':witness(s['input'],got)
  else:assert got==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='typical90_av':
  for _ in range(180):
   n=rng.randint(1,8);k=rng.randint(1,2*n);pairs=[]
   for __ in range(n):a=rng.randint(3,100);pairs.append((a,rng.randint(a//2+1,a-1)))
   best=max(sum(0 if state==0 else pairs[i][1]if state==1 else pairs[i][0]for i,state in enumerate(plan))for plan in itertools.product(range(3),repeat=n)if sum(plan)<=k);assert run(f'{n} {k}\n'+'\n'.join(f'{a} {b}'for a,b in pairs)+'\n')==[str(best)];naive+=1
  n=200000;rows='1000000000 999999999\n'*n;assert run(f'{n} {2*n}\n'+rows)==[str(n*10**9)];assert run(f'{n} {n}\n'+rows)==[str(n*999999999)];edge_checks.append('strict A/2<B<A;3-state-per-task prerequisite oracle;fullN/K and2e14 total')
 elif ref=='typical90_ax':
  mod=1000000007
  for _ in range(200):
   n=rng.randint(2,150);l=rng.randint(2,200);expected=sum(math.comb(n-(l-1)*j,j)for j in range(n//l+1))%mod;assert run(f'{n} {l}\n')==[str(expected)];naive+=1
  def fib(n):
   if n==0:return(0,1)
   a,b=fib(n//2);c=a*((2*b-a)%mod)%mod;d=(a*a+b*b)%mod;return(d,(c+d)%mod)if n%2 else(c,d)
  assert run('100000 2\n')==[str(fib(100001)[0])];assert run('100000 100000\n')==['2'];assert run('2 100000\n')==['1'];edge_checks.append('L>=2;L>N andL=N;independent composition binomials and fast-doubling Fibonacci stress')
 elif ref=='typical90_az':
  mod=1000000007
  for _ in range(100):
   n=rng.randint(1,5);dice=[sorted(rng.sample(range(1,101),6))for __ in range(n)];expected=sum(math.prod(outcome)for outcome in itertools.product(*dice))%mod;assert run(f'{n}\n'+'\n'.join(' '.join(map(str,row))for row in dice)+'\n')==[str(expected)];naive+=1
  assert run('100\n'+'95 96 97 98 99 100\n'*100)==[str(pow(585,100,mod))];edge_checks.append('sum over6^N products, no averaging;source-valid strictly increasing six-face rows<=100;N100 stress')
 elif ref=='typical90_bc':
  for _ in range(180):
   n=rng.randint(5,12);p=rng.choice([1,4,6,8,9,10,12,1000,999999999,10**9]);q=rng.randrange(p);a=[rng.choice([0,10**9,rng.randint(0,100)])for __ in range(n)];expected=sum(math.prod(a[i]for i in choice)%p==q for choice in itertools.combinations(range(n),5));assert run(f'{n} {p} {q}\n'+' '.join(map(str,a))+'\n')==[str(expected)];naive+=1
  assert run('100 1 0\n'+'0 '*100+'\n')==[str(math.comb(100,5))];edge_checks.append('composite modulus andP1;zero/repeated values;arbitrary-integer raw products;all75287520 five-index choices')
 elif ref=='typical90_bd':
  for _ in range(180):
   n=rng.randint(1,12);s=rng.randint(1,200);pairs=[(rng.randint(1,30),rng.randint(1,30))for __ in range(n)];possible=any(sum(pairs[i][(mask>>i)&1]for i in range(n))==s for mask in range(1<<n));text=f'{n} {s}\n'+'\n'.join(f'{a} {b}'for a,b in pairs)+'\n';witness(text,run(text),possible);naive+=1
  for s,possible in [(100000,True),(99999,False)]:
   text=f'100 {s}\n'+'1000 1001\n'*100;witness(text,run(text),possible)
  edge_checks.append('nonunique witness property,exactlyone option/day;S1e5 table;impossible case;sample feasibility via independent bitset')
 else:
  def step(x):return(x+sum(map(int,str(x))))%100000
  for _ in range(180):
   n=rng.randrange(100000);k=rng.randint(1,1000);expected=n
   for __ in range(k):expected=step(expected)
   assert run(f'{n} {k}\n')==[str(expected)];naive+=1
  lift=[array('I',(step(x)for x in range(100000)))]
  for _ in range(59):prev=lift[-1];lift.append(array('I',(prev[prev[x]]for x in range(100000))))
  for n,k in [(0,10**18),(99999,10**18),(1,10**18),(12345,999999999999999999),(54321,1<<59)]:
   expected=n;bits=k;level=0
   while bits:
    if bits&1:expected=lift[level][expected]
    bits//=2;level+=1
   assert run(f'{n} {k}\n')==[str(expected)]
  assert run('99999 1\n')==['44'];assert run('5 3\n')==['13'];edge_checks.append('exactK step indexing;zero fixed point and99999 wrap;independent60-level binary lifting toK1e18')
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'sample_comparison':'valid plan/feasibility property, nonunique output'if ref=='typical90_bd'else'exact output tokens','independent_naive_cases':naive,'source_edge_contract_checks':edge_checks,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Code checks only; original bilingual/native content verified separately. Oracles use3-state prerequisite enumeration, composition binomials, raw dice outcomes/products, subset witnesses and binary lifting independently of the submitted implementations.'};(ROOT/'audit/native-problem-editorials/batch06-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
