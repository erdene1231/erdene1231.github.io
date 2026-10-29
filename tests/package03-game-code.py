"""Independent minimax/state enumeration and source-diagram checks. No production calls."""
import subprocess,tempfile,random,itertools,functools
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(2501);count=0
@functools.lru_cache(None)
def nimwin(a,misere):
 if not any(a):return misere
 for i,x in enumerate(a):
  for y in range(x):
   b=list(a);b[i]=y
   if not nimwin(tuple(sorted(b)),misere):return True
 return False
@functools.lru_cache(None)
def splitwin(a):
 for i,x in enumerate(a):
  for y in range(1,(x+1)//2):
   if not splitwin(tuple(sorted(a[:i]+a[i+1:]+(y,x-y)))):return True
 return False
def mex(s):
 x=0
 while x in s:x+=1
 return x
boards=[['..#..','#...#','..#..','#....','.....'],['....#','..#..','.#...','.#...','.....'],['.....','.###.','.###.','.###.','.....']]
expected=[[[0,1,-1,0,1],[-1,0,1,2,-1],[0,2,-1,1,0],[-1,3,0,4,1],[0,4,1,3,2]],[[0,1,2,3,-1],[1,0,-1,0,1],[2,-1,0,1,2],[3,-1,1,2,0],[4,0,2,5,3]],[[0,1,2,3,4],[1,-1,-1,-1,0],[2,-1,-1,-1,1],[3,-1,-1,-1,2],[4,0,1,2,3]]]
def mazeoracle(a):
 n,m=len(a),len(a[0]);adj={}
 for r in range(n):
  for c in range(m):
   if a[r][c]=='#':continue
   targets=[]
   for i in range(r):
    if all(a[t][c]!='#'for t in range(i,r+1)):targets.append((i,c))
   for j in range(c):
    if all(a[r][t]!='#'for t in range(j,c+1)):targets.append((r,j))
   adj[r,c]=targets
 @functools.lru_cache(None)
 def sg(u):return mex({sg(v)for v in adj[u]})
 return [[sg((r,c))if(r,c)in adj else-1 for c in range(m)]for r in range(n)],adj
with tempfile.TemporaryDirectory()as td:
 bins={}
 for name in ['subtraction','divisors','nim','dag','maze','split']:
  exe=Path(td)/name;subprocess.run(['g++','-std=c++17','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/game-{name}.cpp'),'-o',str(exe)],check=True);bins[name]=exe
 def run(name,data):
  global count
  count+=1;p=subprocess.run([bins[name]],input=data,text=True,capture_output=True,timeout=15);assert p.returncode==0,(name,p.stderr,data[:200]);return p.stdout.strip().splitlines()
 for _ in range(65):
  n=rng.randrange(100);moves=[rng.randrange(1,30)for i in range(rng.randrange(8))]
  @functools.lru_cache(None)
  def win(k):return any(x<=k and not win(k-x)for x in moves)
  out=run('subtraction',f'{n} {len(moves)}\n'+' '.join(map(str,moves)));assert out[1]==''.join('W'if win(k)else'L'for k in range(n+1));w,t=out[0].split();t=int(t);assert(w=='WIN')==win(n)
  if t:assert t in moves and t<=n and not win(n-t)
  else:assert not win(n)
 out=run('subtraction','1000000 3\n1 2 3');assert out[0]=='LOSE 0'and all((c=='L')==(i%4==0)for i,c in enumerate(out[1]))
 for n in [1,2,3,7,8,9,10,100,1000,10000]:
  @functools.lru_cache(None)
  def win(k):return any(not win(k-x)for x in range(1,k)if k%x==0)
  out=run('divisors',str(n));assert out[1]==''.join('W'if k%2==0 else'L'for k in range(1,n+1))
  if n<=100:assert all((out[1][k-1]=='W')==win(k)for k in range(1,n+1))
  w,t=out[0].split();t=int(t)
  if w=='WIN':assert 0<t<n and n%t==0 and (n-t)%2==1
 cases=[tuple(a)for n in range(4)for a in itertools.product(range(5),repeat=n)]
 cases+=[tuple(rng.randrange(7)for i in range(4))for _ in range(80)]
 for a in cases:
  for misere in [False,True]:
   out=run('nim',f'{"M"if misere else"N"} {len(a)}\n'+' '.join(map(str,a)))[0].split();w=nimwin(tuple(sorted(a)),misere)
   if not any(a):assert out==['TERMINAL','WIN'if w else'LOSE'];continue
   assert(out[0]=='WIN')==w
   if w:
    i,t=map(int,out[1:]);i-=1;assert 0<=i<len(a)and 0<t<=a[i];b=list(a);b[i]-=t;assert not nimwin(tuple(sorted(b)),misere)
 for mode,a,target in [('N',[10,12,5],['WIN','1','1']),('M',[2**63-1,0,0],['WIN','1',str(2**63-2)]),('M',[2**63-1,1],['WIN','1',str(2**63-1)]),('N',[2**63-1,2**63-1],['LOSE'])]:assert run('nim',f'{mode} {len(a)}\n'+' '.join(map(str,a)))[0].split()==target
 for _ in range(75):
  n=rng.randrange(1,12);order=list(range(n));rng.shuffle(order);edges=[]
  for i in range(n):
   for j in range(i+1,n):
    if rng.randrange(4)==0:edges.extend([(order[i],order[j])]*(1+rng.randrange(2)))
  adj=[[]for _ in range(n)]
  for u,v in edges:adj[u].append(v)
  @functools.lru_cache(None)
  def g(u):return mex({g(v)for v in adj[u]})
  k=rng.randrange(5);pos=[rng.randrange(n)for _ in range(k)]
  @functools.lru_cache(None)
  def win(p):return any(not win(p[:i]+(v,)+p[i+1:])for i,u in enumerate(p)for v in adj[u])
  data=f'{n} {len(edges)} {k}\n'+'\n'.join(f'{u+1} {v+1}'for u,v in edges)+'\n'+' '.join(str(u+1)for u in pos);out=run('dag',data);assert list(map(int,out[0].split()))==[g(u)for u in range(n)];ans=out[1].split();assert(ans[0]=='WIN')==win(tuple(pos))
  if ans[0]=='WIN':i,v=map(int,ans[1:]);i-=1;v-=1;assert v in adj[pos[i]];after=tuple(pos[:i]+[v]+pos[i+1:]);assert not win(after)
 assert run('dag','1 1 1\n1 1\n1')[0]=='INVALID: cycle'
 assert run('dag','3 3 1\n1 2\n2 3\n3 1\n1')[0]=='INVALID: cycle'
 n=200000;out=run('dag',f'{n} {n-1} 1\n'+'\n'.join(f'{i} {i+1}'for i in range(1,n))+'\n1');assert list(map(int,out[0].split()))==[(n-1-i)%2 for i in range(n)]and out[1]=='WIN 1 2'
 e=[(1,0),(2,1),(3,0),(3,1),(4,3),(4,1),(5,4),(5,1)];out=run('dag','6 8 1\n'+'\n'.join(f'{u+1} {v+1}'for u,v in e)+'\n6');assert list(map(int,out[0].split()))==[0,1,0,2,0,2]
 for a,want in zip(boards,expected):assert mazeoracle(a)[0]==want
 maze_cases=[[(a,(4,4))for a in boards]]+[[(a,(4,4))]for a in boards]
 for _ in range(75):
  puzzles=[]
  for j in range(rng.randrange(1,4)):
   n,m=rng.randrange(1,6),rng.randrange(1,6);a=[''.join('#'if rng.randrange(4)==0 else'.'for c in range(m))for r in range(n)];floor=[(r,c)for r in range(n)for c in range(m)if a[r][c]=='.']
   if not floor:a[0]='.'+a[0][1:];floor=[(0,0)]
   puzzles.append((a,rng.choice(floor)))
  maze_cases.append(puzzles)
 for puzzles in maze_cases:
  data=str(len(puzzles))+'\n'+''.join(f'{len(a)} {len(a[0])}\n'+'\n'.join(a)+f'\n{p[0]+1} {p[1]+1}\n'for a,p in puzzles);out=run('maze',data);gs=[];adjs=[]
  for a,p in puzzles:g,adj=mazeoracle(a);gs.append(g);adjs.append(adj)
  assert list(map(int,out[0].split()))==[g[p[0]][p[1]]for g,(a,p)in zip(gs,puzzles)]
  @functools.lru_cache(None)
  def win(pos):return any(not win(pos[:i]+(v,)+pos[i+1:])for i,u in enumerate(pos)for v in adjs[i][u])
  ans=out[1].split();pos=tuple(p for a,p in puzzles);assert(ans[0]=='WIN')==win(pos)
  if ans[0]=='WIN':i,r,c=map(int,ans[1:]);i-=1;v=(r-1,c-1);assert v in adjs[i][pos[i]];assert not win(pos[:i]+(v,)+pos[i+1:])
  offset=2
  for g in gs:assert [list(map(int,line.split()))for line in out[offset:offset+len(g)]]==g;offset+=len(g)
 a=['.'*100]*100;out=run('maze','1\n100 100\n'+'\n'.join(a)+'\n100 100');g=[list(map(int,line.split()))for line in out[2:]];assert all(g[r][c]==(r^c)for r in range(100)for c in range(100))and out[1]=='LOSE'
 @functools.lru_cache(None)
 def splitg(n):return mex({splitg(a)^splitg(n-a)for a in range(1,(n+1)//2)})
 for _ in range(85):
  a=[rng.randrange(1,14)for i in range(rng.randrange(1,4))];out=run('split',str(len(a))+'\n'+' '.join(map(str,a)));g=list(map(int,out[0].split()));assert g==[splitg(i)for i in range(1,max(a)+1)];ans=out[1].split();assert(ans[0]=='WIN')==splitwin(tuple(sorted(a)))
  if ans[0]=='WIN':i,x,y=map(int,ans[1:]);i-=1;assert 0<x<y and x+y==a[i];b=tuple(sorted(a[:i]+a[i+1:]+[x,y]));assert not splitwin(b)
 out=run('split','1\n8');assert list(map(int,out[0].split()))==[0,0,1,0,2,1,0,2]and out[1]=='WIN 1 1 7'
 out=run('split','2\n2000 2000');assert len(out[0].split())==2000 and out[1]=='LOSE'
 assert run('split','0\n')[-1]=='LOSE'
 print(f'Game theory: six C++17 programs, {count} independent UBSan executions passed; exact source graph/three-maze/split examples and minimax strategy witnesses verified.')
