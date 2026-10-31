"""Original first-three programs: source samples, independent naive cases and limit stresses."""
import json,subprocess,itertools,random,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch01-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_a','typical90_d','typical90_g'];samples=json.loads((ROOT/'audit/PART04-STATEMENT-REFERENCE-SAMPLES.json').read_text())['records'];rng=random.Random(391);counts={r:0 for r in refs};report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref
 subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True)
 def run(text):
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=15);assert p.returncode==0,(ref,p.stderr);assert not p.stderr,(ref,p.stderr);counts[ref]+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 naive=0
 if ref=='typical90_a':
  for _ in range(300):
   l=rng.randint(3,45);n=rng.randint(1,min(8,l-1));k=rng.randint(1,n);a=sorted(rng.sample(range(1,l),n));best=max(min(y-x for x,y in zip((0,)+cuts,cuts+(l,)))for cuts in itertools.combinations(a,k));assert run(f'{n} {l}\n{k}\n'+ ' '.join(map(str,a))+'\n')==[str(best)];naive+=1
  stress=f'100000 1000000000\n100000\n'+' '.join(str(9999*i)for i in range(1,100001))+'\n';expected=['9999']
 elif ref=='typical90_d':
  for _ in range(200):
   h=rng.randint(2,6);w=rng.randint(2,6);a=[[rng.randint(1,99)for _ in range(w)]for _ in range(h)];expected=[]
   for i in range(h):
    for j in range(w):expected.append(str(sum(a[x][y]for x in range(h)for y in range(w)if x==i or y==j)))
   assert run(f'{h} {w}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n')==expected;naive+=1
  # Full2000x2000 source domain. Read output by row, without storing millions of ints.
  h=w=2000;stress=f'{h} {w}\n'+(('99 '*1999+'99\n')*2000);expected=None
 elif ref=='typical90_g':
  for _ in range(250):
   n=rng.randint(1,20);q=rng.randint(1,20);a=[rng.choice([0,1000000000,rng.randrange(1000000001)])for _ in range(n)];b=[rng.choice([0,1000000000,rng.randrange(1000000001)])for _ in range(q)];expected=[str(min(abs(x-y)for x in a))for y in b];text=f'{n}\n'+ ' '.join(map(str,a))+f'\n{q}\n'+'\n'.join(map(str,b))+'\n';assert run(text)==expected;naive+=1
  stress='300000\n'+'0 '*150000+'1000000000 '*150000+'\n300000\n'+'500000000\n'*300000;expected=['500000000']*300000
 start=time.monotonic()
 if ref=='typical90_d':
  p=subprocess.run([str(exe)],input=stress,text=True,capture_output=True,timeout=20);assert p.returncode==0 and not p.stderr;lines=p.stdout.splitlines();assert len(lines)==2000;wanted=('395901 '*1999+'395901');assert all(line==wanted for line in lines);counts[ref]+=1
 else:assert run(stress)==expected
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'limit_stress_passed':True,'stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':counts[ref]})
result={'status':'passed','records':report,'total_program_runs':sum(counts.values()),'limits':'Independent correctness checks are for these three unchanged source task contracts; not proof of prose/bilingual/native-editor completeness or actual judge runtime.'};(ROOT/'audit/native-problem-editorials/batch01-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
