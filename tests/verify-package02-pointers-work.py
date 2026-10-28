"""Independent pair existence oracle for upcoming lesson; not semantic readiness."""
from pathlib import Path
import json,random,subprocess,tempfile,hashlib
root=Path(__file__).resolve().parents[1];source=root/'audit/package02-work/two-pointers.cpp';rng=random.Random(20261028);cases=[]
for a in [[],[0],[3,3],[-10**9,10**9],[8,1,4,6],[-5,-2,0,2,8],[0]*20]:
 for target in [-2*10**9,-10,-1,0,6,10,2*10**9]:cases.append((a,target))
for _ in range(350):cases.append(([rng.randrange(-40,41)for _ in range(rng.randrange(60))],rng.randrange(-90,91)))
with tempfile.TemporaryDirectory()as tmp:
 exe=Path(tmp)/'pair';r=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(source),'-o',str(exe)],capture_output=True,text=True,check=True);assert not r.stderr,r.stderr
 def run(a,target,expected):
  result=subprocess.run([str(exe)],input=f'{len(a)} {target}\n'+' '.join(map(str,a))+'\n',capture_output=True,text=True,check=True,timeout=8).stdout.split()
  if result==['IMPOSSIBLE']:assert not expected
  else:
   assert expected and len(result)==2;i,j=map(int,result);assert 1<=i<=len(a)and 1<=j<=len(a)and i!=j and a[i-1]+a[j-1]==target
 for a,target in cases:run(a,target,any(a[i]+a[j]==target for i in range(len(a))for j in range(i+1,len(a))))
 for a,target,expected in [([7]*200000,14,True),([7]*200000,15,False),(list(range(200000)),399997,True),(list(range(199999,-1,-1)),-1,False)]:run(a,target,expected)
report={'status':'program verified; lesson incomplete','cases':len(cases)+4,'max_elements':200000,'compile_warnings':0,'oracle':'Independent quadratic enumeration on small signed/repeated-value arrays; original-index validation; four maximum-size closed-form cases','program_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'publication':False,'numeric_contract':'abs(values)<=1e9, abs(target)<=2e9; long long sums. This does not claim safe addition of arbitrary signed-64-bit extremes.'}
(root/'audit/PACKAGE02-POINTERS-WORK-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
