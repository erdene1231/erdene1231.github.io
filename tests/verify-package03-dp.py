import json,random,subprocess,tempfile,itertools,collections,math,functools
from pathlib import Path
root=Path(__file__).resolve().parents[1];rng=random.Random(71029);checks=0;MOD=1000000007
with tempfile.TemporaryDirectory()as tmp:
 exes={}
 for name in ['min-coins','count-coins','lis','grid','knapsack','edit','tilings','tiling-formula']:
  exe=Path(tmp)/name;subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(root/f'audit/package03-work/dp-{name}.cpp'),'-o',str(exe)],check=True);exes[name]=exe
 def run(name,s):
  global checks
  p=subprocess.run([str(exes[name])],input=s,text=True,capture_output=True,check=True);assert not p.stderr,p.stderr;checks+=1;return p.stdout.splitlines()
 def mincoins(c,n):
  q=collections.deque([(0,0)]);seen={0}
  while q:
   x,d=q.popleft()
   if x==n:return d
   for coin in c:
    if x+coin<=n and x+coin not in seen:seen.add(x+coin);q.append((x+coin,d+1))
  return -1
 for case in range(100):
  c=rng.sample(range(1,9),rng.randrange(1,5));n=rng.randrange(16)
  if case==0:c=[1,3,4];n=10
  want=mincoins(c,n)
  for mode in range(3):
   out=run('min-coins',f'{mode} {len(c)} {n}\n'+' '.join(map(str,c)));assert int(out[0])==want
   if mode==2:
    path=list(map(int,out[1].split()));assert all(x in c for x in path)
    if want>=0:assert len(path)==want and sum(path)==n
    else:assert not path
 def ways(c,n):
  if n==0:return 1
  return sum(ways(c,n-v)for v in c if v<=n)
 for _ in range(75):
  c=rng.sample(range(1,6),rng.randrange(1,5));n=rng.randrange(11);assert int(run('count-coins',f'{len(c)} {n}\n'+' '.join(map(str,c)))[0])==ways(c,n)
 assert int(run('count-coins','3 5\n1 3 4\n')[0])==6
 assert int(run('count-coins','2 1000\n1 2\n')[0])==sum(math.comb(1000-j,j)for j in range(501))%MOD
 for case in range(100):
  a=[rng.randrange(-5,6)for _ in range(rng.randrange(11))]
  if case==0:a=[6,2,5,1,7,4,8,3]
  out=run('lis',str(len(a))+'\n'+' '.join(map(str,a)));path=list(map(int,out[1].split()));assert len(path)==int(out[0]);it=iter(a);assert all(any(v==x for v in it)for x in path);assert all(x<y for x,y in zip(path,path[1:]));best=0
  for mask in range(1<<len(a)):
   b=[v for i,v in enumerate(a)if mask>>i&1]
   if all(x<y for x,y in zip(b,b[1:])):best=max(best,len(b))
  assert len(path)==best
 grid=[[3,7,9,2,7],[9,8,3,5,5],[1,7,9,8,5],[3,8,6,4,10],[6,3,9,7,8]]
 def grid_oracle(a,r=0,c=0):
  if r==len(a)-1 and c==len(a)-1:return a[r][c]
  options=[]
  if r+1<len(a):options.append(grid_oracle(a,r+1,c))
  if c+1<len(a):options.append(grid_oracle(a,r,c+1))
  return a[r][c]+max(options)
 for case in range(65):
  n=rng.randrange(1,6);a=[[rng.randrange(1,20)for _ in range(n)]for _ in range(n)]
  if case==0:a=grid;n=5
  if case==1:a=[[10**9]*2 for _ in range(2)];n=2
  out=run('grid',str(n)+'\n'+'\n'.join(' '.join(map(str,row))for row in a));path=[tuple(map(int,l.split()))for l in out[1:]];assert path[0]==(1,1)and path[-1]==(n,n);assert all((r2-r,c2-c)in[(1,0),(0,1)]for(r,c),(r2,c2)in zip(path,path[1:]));assert sum(a[r-1][c-1]for r,c in path)==int(out[0])==grid_oracle(a)
 for case in range(80):
  w=[rng.randrange(1,9)for _ in range(rng.randrange(11))]
  if case==0:w=[1,3,3,5]
  possible={sum(v for i,v in enumerate(w)if mask>>i&1)for mask in range(1<<len(w))};out=run('knapsack',str(len(w))+'\n'+' '.join(map(str,w)));assert set(map(int,out[0].split()))==possible==set(map(int,out[1].split()))
 def edit_bfs(s,t):
  q=collections.deque([(s,0)]);seen={s};limit=max(len(s),len(t))
  while q:
   a,d=q.popleft()
   if a==t:return d
   cand=[]
   for i in range(len(a)):
    cand.append(a[:i]+a[i+1:]);cand.extend(a[:i]+c+a[i+1:]for c in 'AB')
   if len(a)<limit:
    for i in range(len(a)+1):cand.extend(a[:i]+c+a[i:]for c in 'AB')
   for b in cand:
    if b not in seen:seen.add(b);q.append((b,d+1))
 for case in range(65):
  s=''.join(rng.choice('AB')for _ in range(rng.randrange(4)));t=''.join(rng.choice('AB')for _ in range(rng.randrange(4)));want=edit_bfs(s,t)
  if case==0:s='LOVE';t='MOVIE';want=2
  out=run('edit',s+'\n'+t+'\n');assert int(out[0])==want;cur=list(s);pos=changes=0
  for l in out[1:]:
   op,a,b=l.split()
   if op in 'KRD':assert cur[pos]==a
   if op=='K':pos+=1
   elif op=='R':cur[pos]=b;pos+=1;changes+=1
   elif op=='D':cur.pop(pos);changes+=1
   else:cur.insert(pos,b);pos+=1;changes+=1
  assert ''.join(cur)==t and changes==want
 @functools.lru_cache(None)
 def tiled(n,m,mask=0):
  full=(1<<(n*m))-1
  if mask==full:return 1
  p=next(i for i in range(n*m)if not(mask>>i&1));ans=0
  if p%m+1<m and not(mask>>(p+1)&1):ans+=tiled(n,m,mask|(1<<p)|(1<<(p+1)))
  if p//m+1<n and not(mask>>(p+m)&1):ans+=tiled(n,m,mask|(1<<p)|(1<<(p+m)))
  return ans
 for n in range(1,5):
  for m in range(1,8):assert int(run('tilings',f'{n} {m}')[0])==tiled(n,m)%MOD
 assert int(run('tilings','4 7')[0])==781
 assert int(run('tilings','2 1000')[0])==sum(math.comb(1000-j,j)for j in range(501))%MOD
 for n in range(1,9):
  for m in range(1,9):
   approx=float(run('tiling-formula',f'{n} {m}')[0]);exact=int(run('tilings',f'{n} {m}')[0]);assert math.isclose(approx,exact,rel_tol=1e-10,abs_tol=1e-7),(n,m,approx,exact)
 assert math.isclose(float(run('tiling-formula','10 10')[0]),258584046368,rel_tol=1e-12)
report={'status':'passed','programs':8,'UBSan':True,'checks':checks,'source_examples':['coin minimum10=3','ordered ways5=6','LIS length4','positive grid67','weights1,3,3,5','LOVE→MOVIE distance2','4×7 tilings781'],'independent_oracles':['coin shortest-path BFS','explicit ordered coin recursion','all LIS subsets','all monotone grid paths','all knapsack subsets','edit graph BFS and operation replay','cell-by-cell domino search','numeric product versus integer profile counts and10×10 reference'],'production_writes':0}
(root/'audit/PACKAGE03-DP-CODE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
