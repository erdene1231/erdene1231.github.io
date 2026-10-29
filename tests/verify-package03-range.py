"""Independent elementary array/matrix oracles for each published C++ program."""
import json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(9037);names=['static','prefix2d','fenwick','recursive','iterative','minimum','compression','difference'];cases={k:0 for k in names};queries=0
with tempfile.TemporaryDirectory() as tmp:
 bins={}
 for name in names:
  exe=str(Path(tmp)/name);subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(ROOT/f'audit/package03-work/range-{name}.cpp'),'-o',exe],check=True,capture_output=True);bins[name]=exe
 def check(name,text,expected):
  r=subprocess.run([bins[name]],input=text,text=True,capture_output=True,timeout=8);assert r.returncode==0,(name,r.stderr);assert r.stdout.split()==list(map(str,expected)),(name,text[:500],r.stdout,expected);cases[name]+=1
 for n in [1,2,3,7,8,9,31]+[rng.randint(1,40) for _ in range(36)]:
  a=[rng.randint(-10**9,10**9) for _ in range(n)];qs=[];out=[]
  for _ in range(40):
   l=rng.randrange(n);r=rng.randrange(l,n);t=rng.randint(1,3);qs.append(f'{t} {l+1} {r+1}');out.append(sum(a[l:r+1]) if t!=2 else min(a[l:r+1]));queries+=1
  check('static',f'{n} {len(qs)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(qs)+'\n',out)
  current=a[:];qs=[];out=[]
  for step in range(70):
   if step%3:
    l=rng.randrange(n);r=rng.randrange(l,n);qs.append(f'2 {l+1} {r+1}');out.append(sum(current[l:r+1]));queries+=1
   else:
    k=rng.randrange(n);x=rng.choice([-10**9,10**9,0]);current[k]+=x;qs.append(f'1 {k+1} {x}')
  text=f'{n} {len(qs)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(qs)+'\n'
  for name in ['fenwick','recursive','iterative']:check(name,text,out)
  current=a[:];qs=[];out=[]
  for step in range(70):
   if step%3==0:
    k=rng.randrange(n);x=rng.randint(-10**9,10**9);current[k]=x;qs.append(f'1 {k+1} {x}')
   elif step%3==1:
    l=rng.randrange(n);r=rng.randrange(l,n);qs.append(f'2 {l+1} {r+1}');out.append(min(current[l:r+1]));queries+=1
   else:qs.append('3');out.append(current.index(min(current))+1);queries+=1
  check('minimum',f'{n} {len(qs)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(qs)+'\n',out)
  current=a[:];qs=[];out=[]
  for step in range(60):
   if step%2:
    k=rng.randrange(n);qs.append(f'2 {k+1}');out.append(current[k]);queries+=1
   else:
    l=rng.randrange(n);r=rng.randrange(l,n);x=rng.choice([-10**9,10**9,0]);qs.append(f'1 {l+1} {r+1} {x}')
    for i in range(l,r+1):current[i]+=x
  check('difference',f'{n} {len(qs)}\n'+' '.join(map(str,a))+'\n'+'\n'.join(qs)+'\n',out)
  coords=[rng.choice([-10**18,8,555,10**9,10**18]) for _ in range(n)];xs=sorted(set(coords));check('compression',str(n)+'\n'+' '.join(map(str,coords))+'\n',[xs.index(x)+1 for x in coords])
 for n,m in [(1,1),(1,7),(7,1),(3,5),(8,8)]+[(rng.randint(1,9),rng.randint(1,9)) for _ in range(35)]:
  a=[[rng.randint(-10**9,10**9) for _ in range(m)] for _ in range(n)];qs=[];out=[]
  for _ in range(40):
   x1=rng.randrange(n);x2=rng.randrange(x1,n);y1=rng.randrange(m);y2=rng.randrange(y1,m);qs.append(f'{x1+1} {y1+1} {x2+1} {y2+1}');out.append(sum(a[i][j] for i in range(x1,x2+1) for j in range(y1,y2+1)));queries+=1
  check('prefix2d',f'{n} {m} {len(qs)}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n'+'\n'.join(qs)+'\n',out)
 # Large sums, non-power-of-two n, full/last/singleton ranges, repeated negative updates.
 n=200000;a=[10**9]*n;text=f'{n} 4\n'+' '.join(map(str,a))+'\n2 1 200000\n1 200000 -1000000000\n2 1 200000\n2 200000 200000\n'
 for name in ['fenwick','recursive','iterative']:check(name,text,[2*10**14,2*10**14-10**9,0])
 check('compression','3\n555 1000000000 8\n',[2,3,1])
report={'status':'passed','programs':8,'UBSan_oracle_cases':sum(cases.values()),'per_program':cases,'independent_query_answers':queries,'large_sum_and_boundary_checks':True};(ROOT/'audit/PACKAGE03-RANGE-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
