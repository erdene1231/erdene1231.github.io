import json,random,subprocess,tempfile,itertools,functools,math
from pathlib import Path
root=Path(__file__).resolve().parents[1];rng=random.Random(61029);checks=0
with tempfile.TemporaryDirectory()as tmp:
 exes={}
 for name in ['coins','events','deadlines','sums','huffman']:
  src=root/f'audit/package03-work/greedy-{name}.cpp';exe=Path(tmp)/name
  subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(exe)],check=True);exes[name]=exe
 def run(name,s):
  global checks
  p=subprocess.run([str(exes[name])],input=s,text=True,capture_output=True,check=True);assert not p.stderr,p.stderr;checks+=1;return p.stdout.splitlines()
 coins=[1,2,5,10,20,50,100,200];dp=[0]+[10**9]*5000
 for v in range(1,len(dp)):dp[v]=1+min(dp[v-c]for c in coins if c<=v)
 for n in [0,1,2,4,6,199,200,520,5000]+[rng.randrange(5001)for _ in range(160)]:
  out=run('coins',str(n));pairs=[list(map(int,l.split()))for l in out[:-1]];assert sum(c*k for c,k in pairs)==n;assert int(out[-1])==dp[n]
 out=run('coins',str(10**18));assert sum(c*k for c,k in(map(int,l.split())for l in out[:-1]))==10**18
 for case in range(130):
  a=[(rng.randrange(10),rng.randrange(1,7))for _ in range(rng.randrange(10))];a=[(l,l+d)for l,d in a]
  if case==0:a=[(1,3),(2,5),(3,9),(6,8)]
  out=run('events',str(len(a))+'\n'+'\n'.join(f'{l} {r}'for l,r in a));ids=list(map(int,out[1].split()));assert len(ids)==int(out[0]);chosen=[a[i-1]for i in ids];assert all(chosen[i][1]<=chosen[i+1][0]for i in range(len(chosen)-1))
  best=0
  for mask in range(1<<len(a)):
   b=sorted(a[i]for i in range(len(a))if mask>>i&1)
   if all(b[i][1]<=b[i+1][0]for i in range(len(b)-1)):best=max(best,len(b))
  assert int(out[0])==best,(a,out,best)
 for case in range(90):
  a=[(rng.randrange(0,9),rng.randrange(20))for _ in range(rng.randrange(0,8))]
  if case==0:a=[(4,2),(3,5),(2,7),(4,5)]
  out=run('deadlines',str(len(a))+'\n'+'\n'.join(f'{t} {d}'for t,d in a));ids=list(map(int,out[1].split()));assert sorted(ids)==list(range(1,len(a)+1))
  def score(order):
   t=ans=0
   for i in order:t+=a[i][0];ans+=a[i][1]-t
   return ans
  best=max(score(p)for p in itertools.permutations(range(len(a))));assert int(out[0])==best==score([i-1 for i in ids])
 # Boundary sums require 64 bits for accumulated finish times and rewards.
 n=200000;out=run('deadlines',str(n)+'\n'+('1000000 1000000000\n'*n));assert int(out[0])==n*10**9-10**6*n*(n+1)//2
 for case in range(150):
  a=[rng.randrange(-12,13)for _ in range(rng.randrange(1,11))]
  if case==0:a=[1,2,9,2,6]
  out=run('sums',str(len(a))+'\n'+' '.join(map(str,a)));x,cost=map(int,out[0].split());mean,square=map(float,out[1].split());best=min(sum(abs(v-z)for v in a)for z in range(min(a),max(a)+1));assert cost==best==sum(abs(v-x)for v in a);assert abs(mean-sum(a)/len(a))<1e-8;expected=sum((v-sum(a)/len(a))**2 for v in a);assert math.isclose(square,expected,rel_tol=1e-9,abs_tol=1e-7)
 out=run('sums','2\n-1000000000 1000000000\n');assert int(out[0].split()[1])==2000000000;assert float(out[1].split()[1])==2e18
 @functools.lru_cache(None)
 def merge_cost(a):
  if len(a)<=1:return 0
  return min(a[i]+a[j]+merge_cost(tuple(sorted([a[k]for k in range(len(a))if k not in(i,j)]+[a[i]+a[j]])))for i in range(len(a))for j in range(i+1,len(a)))
 for case in range(110):
  k=rng.randrange(1,7);a=[rng.randrange(1,7)for _ in range(k)];s=''.join(chr(65+i)*v for i,v in enumerate(a));s=''.join(rng.sample(list(s),len(s)))
  if case==0:s='AABACDACA';a=[5,1,2,1]
  out=run('huffman',s);code=dict(line.split()for line in out[:-3]);bits,length,decoded=out[-3:];assert decoded==s;assert bits==''.join(code[c]for c in s);assert int(length)==len(bits);assert all(not code[x].startswith(code[y])for x in code for y in code if x!=y)
  want=merge_cost(tuple(sorted(a)))if len(a)>1 else a[0];assert int(length)==want,(a,out,want)
  if case==0:assert code=={'A':'0','B':'110','C':'10','D':'111'}and int(length)==15
report={'status':'passed','programs':5,'UBSan':True,'checks':checks,'independent_oracles':['Euro-coin dynamic programming','exhaustive interval subsets','all task permutations','integer absolute-cost search and independent real-square evaluation','all pairwise merge trees for small Huffman frequencies'],'boundary_domains':['target 10^18','200000 tasks and 64-bit reward','negative and billion-sized values','single-symbol Huffman, tie weights, encode/decode'],'production_writes':0}
(root/'audit/PACKAGE03-GREEDY-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
