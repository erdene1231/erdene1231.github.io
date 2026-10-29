import collections,hashlib,itertools,json,math,pathlib,random,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parents[1];rng=random.Random(211029);counts=collections.Counter()
def trial(n):return [d for d in range(1,n+1)if n%d==0]
def isprime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def call(name,data):
 p=subprocess.run([str(tmp/name)],input=data,text=True,capture_output=True,timeout=15);assert p.returncode==0 and not p.stderr,(name,data,p.stderr);counts[name]+=1;return p.stdout.splitlines()
with tempfile.TemporaryDirectory(prefix='number-code-')as folder:
 tmp=pathlib.Path(folder)
 for name in ['basic','sieve','mod','equations','results','gcd']:
  subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/number-{name}.cpp'),'-o',str(tmp/name)],check=True)
 for a,b in [(24,36),(13,8),(1,1),(10**9,999999937)]+[(rng.randrange(1,10**9),rng.randrange(1,10**9))for _ in range(70)]:
  out=list(map(int,call('gcd',f'{a} {b}\n')[0].split()));assert out==[math.gcd(a,b),math.lcm(a,b)]
 for n in list(range(1,105))+[360,1000,99991,10**9]:
  out=call('basic',f'{n}\n');f=list(map(int,out[1].split()));assert f[0]==len(f)-1 and math.prod(f[1:])==n and all(isprime(x)for x in f[1:]);assert int(out[0])==isprime(n)
  ds=[d for d in range(1,math.isqrt(n)+1)if n%d==0];ds=set(ds+[n//d for d in ds]);cnt,s,phi=map(int,out[2].split());assert cnt==len(ds)and s==sum(ds)
  assert (int(out[3])==math.prod(ds)) if math.prod(ds)<=2**63-1 else out[3]=='OVERFLOW'
  if n<10**5:assert phi==sum(math.gcd(i,n)==1 for i in range(1,n+1))
  else:assert phi==400000000
 for n in [1,2,20,127,1000]:
  out=call('sieve',f'{n} {n}\n'+'\n'.join(map(str,range(1,n+1)))+'\n');a=list(map(int,out[0].split()));assert len(a)==max(n-1,0)
  for x,line in enumerate(out[1:],1):
   v=list(map(int,line.split()));assert v[0]==isprime(x)and v[1]==len(v)-2 and math.prod(v[2:])==x and all(isprime(p)for p in v[2:])
   if x>=2:assert (a[x-2]==0)==isprime(x) and (a[x-2]==0 or x%a[x-2]==0)
  if n==20:assert a==[0,0,2,0,3,0,2,3,5,0,3,0,7,5,2,0,3,0,5]
 for x,n,m in [(6,15,17),(2,0,4),(0,0,1),(-2,9,7),(-2**63,10**18,2147483647),(2**63-1,10**18,2147483646)]+[(rng.randrange(-100000,100000),rng.randrange(1000),rng.randrange(1,300))for _ in range(85)]:
  out=call('mod',f'{x} {n} {m}\n');assert int(out[0])==pow(x,n,m)and int(out[2])==2537071545
  if m>1 and math.gcd(x,m)==1:assert int(out[1])*x%m==1
  else:assert out[1]=='NO INVERSE'
 for a,b,c in [(39,15,12),(5,2,11),(4,6,7),(10**9,999999937,-10**9)]+[(rng.randrange(1,100),rng.randrange(1,100),rng.randrange(-500,500))for _ in range(90)]:
  out=call('equations',f'D {a} {b} {c}\n')[0];g=math.gcd(a,b)
  if c%g:assert out=='NONE'
  else:
   x,y,dx,dy=map(int,out.split());assert a*x+b*y==c and dx==b//g and dy==-a//g
   for k in [-3,0,4]:assert a*(x+k*dx)+b*(y+k*dy)==c
 for _ in range(60):
  ms=rng.sample([2,3,5,7,11,13],rng.randrange(1,5));aa=[rng.randrange(-100,100)for m in ms];out=call('equations','C '+str(len(ms))+'\n'+''.join(f'{a} {m}\n'for a,m in zip(aa,ms)))[0];x,m=map(int,out.split());assert m==math.prod(ms)and 0<=x<m and all(x%d==a%d for a,d in zip(aa,ms))
  assert x==next(k for k in range(m)if all(k%d==a%d for a,d in zip(aa,ms)))
 assert call('equations','C 3\n3 5\n4 7\n2 3\n')==['53 105']
 assert call('equations','C 2\n1 4\n1 6\n')==['UNSUPPORTED']
 assert call('equations','C 2\n1 999999937\n2 3\n')==['UNSUPPORTED']
 for n in list(range(65))+[123,9999,10000]:
  v=list(map(int,call('results',f'S {n}\n')[0].split()));assert len(v)==4 and min(v)>=0 and sum(x*x for x in v)==n
 for n in list(range(1,110))+[10**18,74]:
  out=list(map(int,call('results',f'Z {n}\n')[0].split()));v=out[1:];assert out[0]==len(v)and sum(v)==n
  f=[1,2]
  while f[-1]<n:f.append(sum(f[-2:]))
  ids=[f.index(x)for x in v];assert len(set(ids))==len(ids)and all(abs(a-b)>1 for a,b in itertools.combinations(ids,2))
 for cmax in [1,5,30,100,300]:
  out=call('results',f'P {cmax}\n');v=[tuple(map(int,line.split()))for line in out[1:]];expected={(a,b,c)for c in range(1,cmax+1)for a in range(1,c)for b in [math.isqrt(c*c-a*a)]if a<b and a*a+b*b==c*c and math.gcd(a,b)==1};assert len(v)==int(out[0])==len(set(v))and set(v)==expected
 for n in range(100):assert int(call('results',f'W {n}\n')[0])==isprime(n)
 report={'programs':6,'UBSan_oracle_executions':sum(counts.values()),'cases':dict(counts),'oracles':['enumerated divisors and exact big-integer products','trial-prime sieve checks','Python modular pow/inverses','Bezout identities and family shifts','brute CRT residues','four-square identities','nonconsecutive Fibonacci uniqueness conditions','complete primitive-triple enumeration','trial-prime Wilson checks'],'source_checks':{'cube33':sum(x**3 for x in [8866128975287528,-8778405442862239,-2736111468807040])==33,'84product':84**6==351298031616,'CRT263':263%105==53},'source_sha256':{name:hashlib.sha256((R/f'audit/package03-work/number-{name}.cpp').read_bytes()).hexdigest()for name in counts}}
 assert all(report['source_checks'].values());(R/'audit/PACKAGE03-NUMBER-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
