import json,random,subprocess,tempfile,itertools
from pathlib import Path
root=Path(__file__).resolve().parents[1];rng=random.Random(81029);checks=0
with tempfile.TemporaryDirectory()as tmp:
 exes={}
 for name in ['subarray','two-sum','three-sum','smaller','window']:
  exe=Path(tmp)/name;subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(root/f'audit/package03-work/amortized-{name}.cpp'),'-o',str(exe)],check=True);exes[name]=exe
 def run(name,s):
  global checks
  p=subprocess.run([str(exes[name])],input=s,text=True,capture_output=True,check=True);assert not p.stderr,p.stderr;checks+=1;return p.stdout.splitlines()
 for case in range(160):
  a=[rng.randrange(1,20)for _ in range(rng.randrange(12))];target=rng.randrange(1,70)
  if case==0:a=[1,3,2,5,1,1,2,3];target=8
  if case==1:a=[100,1,2];target=3
  want=[(i,j)for i in range(len(a))for j in range(i,len(a))if sum(a[i:j+1])==target];out=run('subarray',f'{len(a)} {target}\n'+' '.join(map(str,a)))[0]
  if not want:assert out=='IMPOSSIBLE'
  else:l,r=map(int,out.split());assert(l-1,r-1)in want
 for size,name in [(2,'two-sum'),(3,'three-sum')]:
  for case in range(170):
   a=[rng.randrange(-10,11)for _ in range(rng.randrange(12))];target=rng.randrange(-30,31)
   if case==0:a=[1,4,5,6,7,9,9,10];target=12
   if case==1:a=[2000000000]*size;target=2000000000*size
   if case==2:a=[-2000000000]*size;target=-2000000000*size
   want=any(sum(a[i]for i in ids)==target for ids in itertools.combinations(range(len(a)),size));out=run(name,f'{len(a)} {target}\n'+' '.join(map(str,a)))
   assert len(out)==(2 if size==2 else 1)
   for line in out:
    ids=list(map(int,line.split()))
    if not want:assert ids==[-1]*size
    else:assert len(ids)==len(set(ids))==size and all(1<=i<=len(a)for i in ids)and sum(a[i-1]for i in ids)==target
 for case in range(150):
  a=[rng.randrange(-5,6)for _ in range(rng.randrange(16))]
  if case==0:a=[1,3,4,2,5,3,4,2]
  if case==1:a=[4]*10
  out=run('smaller',str(len(a))+'\n'+' '.join(map(str,a)));want=[next((j for j in range(i-1,-1,-1)if a[j]<a[i]),-1)for i in range(len(a))];assert list(map(int,out[0].split()))==[i+1 for i in want];assert out[1].split()==['NONE'if i==-1 else str(a[i])for i in want]
 for case in range(180):
  n=rng.randrange(1,30);k=rng.randrange(1,n+1);a=[rng.randrange(-10,11)for _ in range(n)]
  if case==0:a=[2,1,4,5,3,4,1,2];n=8;k=4
  if case==1:a=[7]*n
  out=run('window',f'{n} {k}\n'+' '.join(map(str,a)));assert list(map(int,out[0].split()))==[min(a[i:i+k])for i in range(n-k+1)]
 n=200000;a=list(range(n));out=run('smaller',str(n)+'\n'+' '.join(map(str,a)));assert list(map(int,out[0].split()))==list(range(n))
 a=list(range(n,0,-1));out=run('window',f'{n} {n//2}\n'+' '.join(map(str,a)));assert list(map(int,out[0].split()))==[n//2+1-i for i in range(n//2+1)]
report={'status':'passed','programs':5,'UBSan':True,'checks':checks,'oracles':['all nonempty positive subarrays','all distinct pairs/triples with original indices','linear backward nearest-strictly-smaller scan','every window via direct min'],'adversarial':['too-large first element','empty/short arrays','duplicate equal values','negative pairs/triples','64-bit sums at ±4/6billion','k=1/k=n','200000 increasing/decreasing sequences'],'production_writes':0};(root/'audit/PACKAGE03-AMORTIZED-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
