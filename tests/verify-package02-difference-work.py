"""Reference implementation for the next lesson; not whole-lesson readiness."""
from pathlib import Path
import json,random,subprocess,tempfile,hashlib
root=Path(__file__).resolve().parents[1];source=root/'audit/package02-work/difference-array.cpp';rng=random.Random(20261028);cases=0
with tempfile.TemporaryDirectory()as tmp:
 exe=Path(tmp)/'difference';r=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(source),'-o',str(exe)],capture_output=True,text=True,check=True);assert not r.stderr,r.stderr
 def run(values,updates):
  text=f'{len(values)} {len(updates)}\n'+' '.join(map(str,values))+'\n'+''.join(f'{l+1} {r} {v}\n'for l,r,v in updates)
  return list(map(int,subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=8,check=True).stdout.split()))
 arrays=[[],[0],[10**9],[-10**9],[4,-2,7,0,3]]+[[rng.randrange(-10**9,10**9+1)for _ in range(rng.randrange(1,70))]for _ in range(180)]
 for values in arrays:
  n=len(values);updates=[]if not n else[(0,n,3),(n-1,n,-5),(0,1,0)]+[(lambda l,r,v:(min(l,r),max(l,r)+1,v))(rng.randrange(n),rng.randrange(n),rng.randrange(-10**9,10**9+1))for _ in range(100)]
  expected=values.copy()
  for l,r,v in updates:
   for i in range(l,r):expected[i]+=v
  assert run(values,updates)==expected;cases+=1
 n=200000;updates=[(0,n,10**9)]*200000;assert run([-10**9]*n,updates)==[199999*10**9]*n;cases+=1
 # Internal contract also permits empty half-open updates, including the sentinel boundary.
 harness=Path(tmp)/'helper.cpp';harness.write_text('#define main lesson_main\n'+source.read_text()+'\n#undef main\nint main(){vector<long long>a={4,-2,7,0,3};auto d=build_difference(a);if(d!=vector<long long>{4,-6,9,-7,3,-3})return 1;for(int i=0;i<=5;++i)add_range(d,i,i,100);if(restore_values(d)!=a)return 2;add_range(d,1,4,3);add_range(d,3,5,-2);if(restore_values(d)!=vector<long long>{4,1,10,1,1})return 3;return 0;}');helper=Path(tmp)/'helper';subprocess.run(['g++','-std=c++17','-O2',str(harness),'-o',str(helper)],check=True);subprocess.run([str(helper)],check=True)
report={'status':'program verified; lesson incomplete','cases':cases,'max_elements':200000,'max_updates':200000,'compile_warnings':0,'oracle':'Direct element-by-element updates on small signed arrays; independent closed form on maximum case; empty helper/sentinel and full difference trace','program_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'publication':False,'remaining':'Author and review native MN/EN fifteen-section teaching document, exact fragments, practice, editor/render and publication guards'}
(root/'audit/PACKAGE02-DIFFERENCE-WORK-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
