"""Independent exact/floating oracles; executable cases count, no production calls."""
import subprocess,tempfile,random,math,itertools
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
R=Path(__file__).resolve().parents[1];rng=random.Random(2401);count=0
with tempfile.TemporaryDirectory()as td:
 bins={}
 for name in ['events','dice','distributions','markov','quickselect','freivalds','cut']:
  exe=Path(td)/name;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/probability-{name}.cpp'),'-o',str(exe)],check=True);bins[name]=exe
 def run(name,data):
  global count
  count+=1;p=subprocess.run([bins[name]],input=data,text=True,capture_output=True,timeout=12);assert p.returncode==0,(name,p.stderr,data);return p.stdout.strip().splitlines()
 def near(a,b,tol=2e-13):assert math.isclose(float(a),float(b),rel_tol=tol,abs_tol=2e-16),(a,b)
 for _ in range(70):
  items=[(rng.randrange(100000000),rng.randrange(4))for i in range(rng.randrange(1,30))];total=sum(w for w,m in items)or 1
  if not any(w for w,m in items):items[0]=(1,items[0][1])
  a=sum(w for w,m in items if m&1);b=sum(w for w,m in items if m&2);ab=sum(w for w,m in items if m==3);u=sum(w for w,m in items if m)
  out=run('events',str(len(items))+'\n'+'\n'.join(f'{w} {m}'for w,m in items))
  expected=[Fraction(a,total),Fraction(b,total),Fraction(u,total),Fraction(ab,total)]
  assert [Fraction(s)for s in out[:4]]==expected
  assert (out[4]=='UNDEFINED')if b==0 else Fraction(out[4])==Fraction(ab,b)
 assert run('events','2\n1000000000000 1\n0 2')[-1]=='UNDEFINED'
 for n in list(range(15))+[40,100,1000]:
  lo,hi=rng.randrange(-2,6*n+2),rng.randrange(-2,6*n+2);lo,hi=sorted([lo,hi]);out=run('dice',f'{n} {lo} {hi}')
  actual=list(map(float,out[1].split()));counts=[1]
  for i in range(n):
   nxt=[0]*(len(counts)+6)
   for s,c in enumerate(counts):
    for x in range(1,7):nxt[s+x]+=c
   counts=nxt
  denom=6**n
  assert len(actual)==6*n+1
  for a,b in zip(actual,counts):near(a,Fraction(b,denom))
  near(out[0].split()[0],sum((Fraction(c,denom)for s,c in enumerate(counts)if lo<=s<=hi),Fraction(0)))
  near(out[0].split()[1],Fraction(7*n,2));near(sum(actual),1)
 for n in [0,1,2,10,40,200,2000]:
  for p in [0,1,Fraction(1,6),Fraction(1,2),Fraction(99,100)]:
   out=run('distributions',f'B {n} {float(p):.18g}');a=list(map(float,out[0].split()))
   if n<=40:
    for k,x in enumerate(a):near(x,math.comb(n,k)*float(p)**k*(1-float(p))**(n-k))
   near(sum(a),1);near(sum(k*x for k,x in enumerate(a)),n*float(p),1e-11);near(out[1],n*float(p))
 for p in [0,1,.5,1/6,1e-12]:
  for k in [1,2,4,1000]:
   out=run('distributions',f'G {p:.18g} {k}')[0].split();near(out[0],(1-p)**(k-1)*p)
   if p:near(out[1],1/p)
   else:assert out[1]=='INF'
 for n in [0,1,10,10**18]:
  for p in [0,1,1e-18,1/6]:
   with localcontext()as ctx:
    ctx.prec=70;expected=Decimal(0) if n==0 else 1-(1-Decimal(str(p)))**n
   near(run('distributions',f'C {n} {p:.18g}')[0],expected)
 for n in [1,2,3,10,100000,10**18]:
  with localcontext()as ctx:
   ctx.prec=70;expected=Decimal(n)*(1-1/Decimal(n))**n
  near(run('distributions',f'E {n}')[0],expected)
 for a,b in [(-2**63,2**63-1),(2**63-2,2**63-1),(-5,-2),(1,6)]:near(run('distributions',f'U {a} {b}')[0],Fraction(a+b,2))
 for n in range(1,12):
  for k in [0,1,2,3,7,30,100]:
   dp=[Fraction(i==0)for i in range(n)]
   for _ in range(k):
    nxt=[Fraction(0)for i in range(n)]
    for j,p in enumerate(dp):
     if n==1:nxt[0]+=p
     elif j==0:nxt[1]+=p
     elif j==n-1:nxt[n-2]+=p
     else:nxt[j-1]+=p/2;nxt[j+1]+=p/2
    dp=nxt
   actual=list(map(float,run('markov',f'{n} {k}')[0].split()))
   for a,b in zip(actual,dp):near(a,b)
 for n in [1,2,5,50]:
  for k in [10**18,10**18-1]:
   a=list(map(float,run('markov',f'{n} {k}')[0].split()));near(sum(a),1);assert all(-1e-18<=x<=1+1e-18 for x in a)
   if n>1:
    for i,x in enumerate(a):
     if i%2!=k%2:near(x,0)
 for _ in range(160):
  n=rng.randrange(1,250);a=[rng.choice([-2**63,2**63-1,rng.randrange(-40,41)])for i in range(n)];k=rng.randrange(1,n+1)
  out=run('quickselect',f'{n} {k} {rng.getrandbits(64)}\n'+' '.join(map(str,a)));assert int(out[0])==sorted(a)[k-1]
 for a,k in [([7]*100000,50000),(list(range(100000)),99999),(list(range(100000))[::-1],1)]:assert int(run('quickselect',f'{len(a)} {k} 3\n'+' '.join(map(str,a)))[0])==sorted(a)[k-1]
 for _ in range(60):
  n=rng.randrange(1,8);a=[[rng.randrange(-10000,10001)for j in range(n)]for i in range(n)];b=[[rng.randrange(-10000,10001)for j in range(n)]for i in range(n)];c=[[sum(a[i][k]*b[k][j]for k in range(n))for j in range(n)]for i in range(n)]
  def data(c):return f'{n} 60 {rng.getrandbits(64)}\n'+'\n'.join(' '.join(map(str,row))for mat in [a,b,c]for row in mat)
  assert run('freivalds',data(c))[0]=='PROBABLY EQUAL'
  c[rng.randrange(n)][rng.randrange(n)]+=1;out=run('freivalds',data(c));assert out[0]=='DIFFERENT';x=list(map(int,out[1].split()));assert any(sum((sum(a[i][k]*b[k][j]for k in range(n))-c[i][j])*x[j]for j in range(n))for i in range(n))
 # Exact arithmetic stress, no modular aliases.
 n=200;a=[[10000]*n for _ in range(n)];b=[[-10000]*n for _ in range(n)];c=[[-20000000000]*n for _ in range(n)]
 data=f'{n} 60 17\n'+'\n'.join(' '.join(map(str,row))for mat in [a,b,c]for row in mat)
 assert run('freivalds',data)[0]=='PROBABLY EQUAL'
 # Verify one-round theoretical half bound exhaustively, not just seeded success.
 for n in range(1,6):
  for _ in range(20):
   d=[[rng.randrange(-3,4)for j in range(n)]for i in range(n)]
   if not any(map(any,d)):continue
   xs=list(itertools.product([0,1],repeat=n));accept=sum(all(sum(row[j]*x[j]for j in range(n))==0 for row in d)for x in xs);assert accept*2<=len(xs)
 for _ in range(90):
  n=rng.randrange(1,20);e=[]if n==1 else[rng.sample(range(n),2)for i in range(rng.randrange(80))];out=run('cut',f'{n} {len(e)} {rng.getrandbits(64)}\n'+'\n'.join(f'{u+1} {v+1}'for u,v in e));cut,trials=map(int,out[0].split());col=list(map(int,out[1].split()));assert len(col)==n and set(col)<={0,1};assert cut==sum(col[u]!=col[v]for u,v in e)and 2*cut>=len(e)and trials>=1
 e=[(0,1),(0,2),(0,3),(1,3),(1,4),(2,3),(3,4)];col=[0,1,1,0,0];assert sum(col[u]!=col[v]for u,v in e)==5
 assert Fraction(13*math.comb(4,3),math.comb(52,3))==Fraction(1,425)==Fraction(3,51)*Fraction(2,50)
 assert [6*3+8*6,1*3+3*6]==[8*3+7*6,3*3+2*6]==[66,21]
 print(f'Probability: seven C++17 programs; {count} independent UBSan executions passed, plus exhaustive bit-vector and exact source-example checks.')
