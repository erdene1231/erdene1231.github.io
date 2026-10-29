import collections,hashlib,itertools,json,math,pathlib,random,subprocess,tempfile
R=pathlib.Path(__file__).resolve().parents[1];rng=random.Random(221029);counts=collections.Counter();MOD=1000000007
names=['composition','binomial','catalan','inclusion','derangement','burnside','prufer']
def call(name,data):
 p=subprocess.run([str(tmp/name)],input=data,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(name,data[:100],p.stderr);counts[name]+=1;return p.stdout.splitlines()
def choose(n,k):return math.comb(n,k)if 0<=k<=n else 0
def code_oracle(n,edges):
 a=[set()for _ in range(n+1)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 out=[]
 for _ in range(n-2):
  u=next(i for i in range(1,n+1)if len(a[i])==1);v=next(iter(a[u]));out.append(v);a[u].clear();a[v].remove(u)
 return out
def parse(out,n,code=None):
 assert int(out[0])==(1 if n==1 else pow(n,n-2,MOD));row=list(map(int,out[1].split()));c=row[1:];assert row[0]==len(c)==max(n-2,0)
 if code is not None:assert c==list(code)
 edges=[tuple(map(int,s.split()))for s in out[3:]];assert int(out[2])==len(edges)==n-1
 assert all(1<=a<=n and 1<=b<=n and a!=b for a,b in edges)
 seen={1}
 for _ in range(n):
  old=len(seen)
  for a,b in edges:
   if a in seen or b in seen:seen.update([a,b])
  if len(seen)==old:break
 assert len(seen)==n and code_oracle(n,edges)==c
 return c,{tuple(sorted(e))for e in edges}
with tempfile.TemporaryDirectory(prefix='combinatorics-code-')as folder:
 tmp=pathlib.Path(folder)
 for name in names:subprocess.run(['g++','-std=c++17','-O1','-g','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/combinatorics-{name}.cpp'),'-o',str(tmp/name)],check=True)
 for n in list(range(13))+[60]:
  out=call('composition',f'{n}\n');f=list(map(int,out[0].split()));assert f==[1]+[2**(i-1)for i in range(1,n+1)]and int(out[1])==f[-1]
 for n,k in [(0,0),(5,3),(999998,2),(1000000,0),(100,101)]+[(rng.randrange(500),rng.randrange(501))for _ in range(70)]:
  out=call('binomial',f'B {n} {k}\n');assert int(out[0])==choose(n,k)%MOD
  if n<500:assert int(call('binomial',f'P {n} {k}\n')[0])==choose(n,k)%MOD
 for n in range(1,8):
  for k in range(6):
   out=list(map(int,call('binomial',f'X {n} {k}\n')[0].split()));balls=sum(sum(t)==k for t in itertools.product(range(k+1),repeat=n))if n<=5 and k<=3 else choose(n+k-1,k)
   sep=sum(sum(t)==k and all(not(t[i]and t[i+1])for i in range(n-1))for t in itertools.product([0,1],repeat=n));assert out==[choose(n,k),balls,sep]
 for groups in [[],[0],[1,1,1],[2,2,1],[0,2,1]]+[[rng.randrange(5)for _ in range(rng.randrange(1,6))]for _ in range(40)]:
  out=int(call('binomial','M '+str(len(groups))+'\n'+' '.join(map(str,groups))+'\n')[0]);assert out==math.factorial(sum(groups))//math.prod(math.factorial(k)for k in groups)%MOD
 for n in range(31):
  out=call('catalan',f'{n}\n');expected=choose(2*n,n)//(n+1);assert list(map(int,out[0].split()))==[expected]*2
  if n<=8:
   values=out[1:];assert len(values)==len(set(values))==expected
   for s in values:
    b=0
    for c in s:b+=1 if c=='('else-1;assert b>=0
    assert b==0 and len(s)==2*n
 for n in range(1,9):
  for _ in range(8):
   members=[rng.randrange(1<<n)for _ in range(rng.randrange(45))];out=list(map(int,call('inclusion',f'{n} {len(members)}\n'+' '.join(map(str,members))+'\n')[0].split()));assert out==[sum(x!=0 for x in members),sum(x==(1<<n)-1 for x in members)]
 assert call('inclusion','16 200000\n'+('65535 '*200000)+'\n')==['200000 200000']
 assert int(call('binomial','P 2000 1000\n')[0])==choose(2000,1000)%MOD
 # Exact source fixed-point sets and every intersection size.
 perms=list(itertools.permutations(range(1,4)));sets=[{p for p in perms if p[i]==i+1}for i in range(3)];assert [len(x)for x in sets]==[2,2,2]and len(set.union(*sets))==4
 members=[sum(1<<i for i in range(3)if p[i]==i+1)for p in perms];assert call('inclusion','3 6\n'+' '.join(map(str,members))+'\n')==['4 1']
 for n in range(10):
  expected=sum(all(x!=i for i,x in enumerate(p))for p in itertools.permutations(range(n)));assert list(map(int,call('derangement',f'{n}\n')[0].split()))==[expected]*2
 a,b=1,0
 for n in range(2,1000001):a,b=b,(n-1)*(a+b)%MOD
 assert list(map(int,call('derangement','1000000\n')[0].split()))==[b,b]
 for n in range(1,8):
  for m in range(1,4):
   necklaces={min(t[i:]+t[:i]for i in range(n))for t in itertools.product(range(m),repeat=n)};assert int(call('burnside',f'{n} {m}\n')[0])==len(necklaces)
 assert int(call('burnside',f'6 {MOD-1}\n')[0])==(sum((MOD-1)**math.gcd(k,6)for k in range(6))//6)%MOD
 assert call('burnside','4 3\n')==['24'];assert int(call('burnside','1000 1\n')[0])==1
 all_trees={}
 for n in range(1,6):
  trees=set()
  for c in itertools.product(range(1,n+1),repeat=max(0,n-2)):
   code,edges=parse(call('prufer',f'D {n}\n'+' '.join(map(str,c))+'\n'),n,c);trees.add(tuple(sorted(edges)));p,e=parse(call('prufer',f'E {n}\n'+''.join(f'{a} {b}\n'for a,b in edges)),n,c);assert e==edges
  assert len(trees)==(1 if n==1 else n**(n-2));all_trees[n]=trees
 # Independent enumerate connected n-1 edge sets, not another decoder.
 for n in [3,4,5]:
  brute=set()
  for edges in itertools.combinations(itertools.combinations(range(1,n+1),2),n-1):
   seen={1}
   for _ in range(n):
    for a,b in edges:
     if a in seen or b in seen:seen.update([a,b])
   if len(seen)==n:brute.add(tuple(sorted(edges)))
  assert brute==all_trees[n]
 source=[(1,4),(3,4),(2,4),(2,5)];assert parse(call('prufer','E 5\n'+''.join(f'{a} {b}\n'for a,b in source)),5)[0]==[4,4,2]
 n=200000;out=call('prufer',f'E {n}\n'+''.join(f'{i} {i+1}\n'for i in range(1,n)));assert int(out[2])==n-1 and int(out[1].split()[0])==n-2
 report={'programs':len(names),'UBSan_oracle_executions':sum(counts.values()),'cases':dict(counts),'maxN_prufer_iterative_chain':200000,'maxN_factorials_derangements':1000000,'oracles':['Python exact binomial/multinomial arithmetic','direct box placements','all valid brackets through8pairs','direct universe membership unions/intersections','permutation derangements','rotation-canonical necklace enumeration','every Prufer sequence through5 vertices versus independent connected-edge-set tree enumeration'],'source_checks':{'compositions4':8,'choose5_3':10,'boxes5_2':[10,15,6],'Catalan3':5,'derangements3':2,'necklace4_3':24,'Cayley4':16,'Prufer_source':[4,4,2]},'source_sha256':{name:hashlib.sha256((R/f'audit/package03-work/combinatorics-{name}.cpp').read_bytes()).hexdigest()for name in names}}
 (R/'audit/PACKAGE03-COMBINATORICS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
