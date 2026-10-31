"""Six exact original programs: captured source samples, independent oracles and source-bound stresses."""
import json,subprocess,itertools,random,time,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch02-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_b','typical90_f','typical90_h','typical90_j','typical90_v','typical90_x'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(392);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=15);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='typical90_b':
  for n in range(1,21):
   expected=[]
   def rec(s,opened,closed):
    if len(s)==n:
     if opened==closed:expected.append(s)
     return
    if opened<n//2:rec(s+'(',opened+1,closed)
    if closed<opened:rec(s+')',opened,closed+1)
   rec('',0,0);assert run(str(n)+'\n')==expected;naive+=1
  stress='20\n';expected=None # n20 already exhaustively checked above.
 elif ref=='typical90_f':
  for _ in range(250):
   n=rng.randint(1,14);k=rng.randint(1,n);s=''.join(rng.choice('abcdez')for _ in range(n));expected=min(''.join(s[i]for i in idx)for idx in itertools.combinations(range(n),k));assert run(f'{n} {k}\n{s}\n')==[expected];naive+=1
  stress='100000 50000\n'+'z'*100000+'\n';expected=['z'*50000]
 elif ref=='typical90_h':
  for _ in range(250):
   n=rng.randint(1,18);s=''.join(rng.choice('atcoder')for _ in range(n));expected=sum(''.join(s[i]for i in idx)=='atcoder'for idx in itertools.combinations(range(n),7));assert run(f'{n}\n{s}\n')==[str(expected)];naive+=1
  m=14285;s=''.join(c*m for c in 'atcoder')+'z'*5;stress=f'{len(s)}\n{s}\n';expected=[str(pow(m,7,1000000007))]
 elif ref=='typical90_j':
  for _ in range(200):
   n=rng.randint(1,60);q=rng.randint(1,20);a=[(rng.randint(1,2),rng.randint(0,100))for _ in range(n)];queries=[];expected=[]
   for __ in range(q):
    l=rng.randint(1,n);r=rng.randint(l,n);queries.append((l,r));expected.extend(str(sum(p for c,p in a[l-1:r]if c==group))for group in [1,2])
   text=f'{n}\n'+'\n'.join(f'{c} {p}'for c,p in a)+f'\n{q}\n'+'\n'.join(f'{l} {r}'for l,r in queries)+'\n';assert run(text)==expected;naive+=1
  stress='100000\n'+'1 100\n'*100000+'100000\n'+'1 100000\n'*100000;expected=['10000000','0']*100000
 elif ref=='typical90_v':
  for _ in range(300):
   a,b,c=[rng.randint(1,80)for _ in range(3)];expected=min(a//d+b//d+c//d-3 for d in range(1,min(a,b,c)+1)if a%d==b%d==c%d==0);assert run(f'{a} {b} {c}\n')==[str(expected)];naive+=1
  stress='1000000000000000000 999999999999999999 999999999999999998\n';expected=['2999999999999999994']
 else:
  for _ in range(250):
   n=rng.randint(1,3);k=rng.randint(1,7);a=tuple(rng.randint(1,4)for _ in range(n));b=tuple(rng.randint(1,4)for _ in range(n));states={a}
   for __ in range(k):
    nxt=set()
    for s in states:
     for i in range(n):
      for d in [-1,1]:t=list(s);t[i]+=d;nxt.add(tuple(t))
    states=nxt
   text=f'{n} {k}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n';assert run(text)==['Yes'if b in states else'No'];naive+=1
  stress='1000 1000000000\n'+'1 '*1000+'\n'+'1000000 '*1000+'\n';expected=['Yes']
 if expected is not None:assert run(stress)==expected
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Correctness evidence for these six source contracts, not prose/native completeness or actual judge timing. Parentheses n20 fully enumerated; AtCounter repeated ordered character blocks use independent m^7 formula.'};(ROOT/'audit/native-problem-editorials/batch02-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
