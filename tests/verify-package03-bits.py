import itertools,json,math,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(10037);names=['representation','operations','sets','hamming','rectangles','selection','elevator','subset-sums'];counts={n:0 for n in names};MASK=(1<<64)-1
with tempfile.TemporaryDirectory() as tmp:
 bins={}
 for name in names:
  exe=str(Path(tmp)/name);subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(ROOT/f'audit/package03-work/bits-{name}.cpp'),'-o',exe],check=True,capture_output=True);bins[name]=exe
 def run(name,text):
  r=subprocess.run([bins[name]],input=text,text=True,capture_output=True,timeout=12);assert r.returncode==0,(name,r.stderr);counts[name]+=1;return r.stdout
 def check(name,text,expected):assert run(name,text).split()==list(map(str,expected)),(name,text[:300],expected)
 check('representation','',[f'{43:032b}',-43,2**32-43,f'{2**32-43:032b}',0,2**31-1,2**31])
 for x,y,k in [(0,0,0),(0,MASK,63),(MASK,0,63),(1<<63,MASK,63),(22,26,4),(5328,29,31)]+[(rng.getrandbits(64),rng.getrandbits(64),rng.randrange(64))for _ in range(90)]:
  low=x&-x;expected=[x&y,x|y,x^y,MASK^x,(x<<k)&MASK,x>>k,int(bool(x&(1<<k))),x|(1<<k),x&~(1<<k),x^(1<<k),x&((x-1)&MASK),low,x|((x-1)&MASK),int(x!=0 and x&(x-1)==0),64-x.bit_length(),(low.bit_length()-1 if x else 64),x.bit_count(),x.bit_count()%2,19,4,5,1];check('operations',f'{x} {y} {k}\n',expected)
 for n in range(9):
  for _ in range(6):
   a=[i for i in range(n) if rng.randrange(2)];b=[i for i in range(n) if rng.randrange(2)];k=rng.randrange(n+1);x=sum(1<<i for i in a);y=sum(1<<i for i in b);limit=(1<<n)-1
   text=f'{n} {len(a)} {len(b)} {k}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n';lines=run('sets',text).splitlines();assert len(lines)==6
   wanted=[[x,len(a)],a,[x&y,x|y,(~x)&limit,x&~y],list(range(1<<n)),[s for s in range(1<<n)if s.bit_count()==k],[s for s in range(1<<n)if s&x==s]];assert [list(map(int,line.split()))for line in lines]==wanted
 # Call the actual struct operations too: constructor, duplicate insert, erase, high bit.
 harness=Path(tmp)/'set-methods.cpp';harness.write_text('#define main example_main\n#include "'+str(ROOT/'audit/package03-work/bits-sets.cpp')+'"\n#undef main\nint main(){MaskSet a(20);if(a.mask!=0)return 1;a.add(19);a.add(19);a.add(0);if(a.size()!=2||!a.contains(19))return 2;a.erase(19);if(a.contains(19)||a.size()!=1||a.mask!=1)return 3;}');exe=str(Path(tmp)/'set-methods');subprocess.run(['g++','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all',str(harness),'-o',exe],check=True,capture_output=True);subprocess.run([exe],check=True,capture_output=True);counts['sets']+=1
 for k in [1,5,31,32,33,63,64]:
  for _ in range(6):
   n=rng.randint(2,14);s=[''.join(rng.choice('01')for _ in range(k))for _ in range(n)];ans=min(sum(x!=y for x,y in zip(a,b))for a,b in itertools.combinations(s,2));check('hamming',f'{n} {k}\n'+'\n'.join(s)+'\n',[ans,ans])
 check('hamming','3 5\n00111\n01101\n11110\n',[2,2])
 source=['01001','01100','10000','01101','00000']
 for a in [source]+[[''.join(rng.choice('01')for _ in range(n))for _ in range(n)]for n in range(1,10)for _ in range(5)]:
  n=len(a);ans=sum(a[r][c]==a[r][d]==a[s][c]==a[s][d]=='1'for r,s in itertools.combinations(range(n),2)for c,d in itertools.combinations(range(n),2))
  for mode in [0,1]:check('rectangles',f'{n} {mode}\n'+'\n'.join(a)+'\n',[ans])
 for n in [31,32,33,63,64,65,127,128,129]:
  a=['1'*n]*n;expected=math.comb(n,2)**2;check('rectangles',f'{n} 0\n'+'\n'.join(a)+'\n',[expected])
 n=2500;check('rectangles',f'{n} 0\n'+('1'*n+'\n')*n,[math.comb(n,2)**2])
 def schedule_oracle(price,n):
  k=len(price)
  if k>n:return -1
  return min((sum(price[x][d]for x,d in enumerate(days))for days in itertools.permutations(range(n),k)),default=0)
 price=[[6,9,5,2,8,9,1,6],[8,2,6,2,7,5,7,2],[5,3,9,7,3,5,1,4]];check('selection','3 3\n1000000000 1000000000 1000000000\n1000000000 1000000000 1000000000\n1000000000 1000000000 1000000000\n',[3000000000])
 check('selection','3 8\n'+'\n'.join(' '.join(map(str,row))for row in price)+'\n',[5])
 for n in range(7):
  for k in range(5):
   price=[[rng.randrange(10**9) for _ in range(n)]for _ in range(k)];ans=schedule_oracle(price,n);check('selection',f'{k} {n}\n'+'\n'.join(' '.join(map(str,row))for row in price)+'\n',[ans])
 def binpack(w,x):
  if not w:return 0
  best=len(w);loads=[]
  def go(i):
   nonlocal best
   if i==len(w):best=min(best,len(loads));return
   if len(loads)>=best:return
   seen=set()
   for j in range(len(loads)):
    if loads[j]not in seen and loads[j]+w[i]<=x:
     seen.add(loads[j]);loads[j]+=w[i];go(i+1);loads[j]-=w[i]
   loads.append(w[i]);go(i+1);loads.pop()
  go(0);return best
 check('elevator','5 10\n2 3 3 5 6\n',[2]);check('elevator','2 1000000000000000000\n1000000000000000000 1000000000000000000\n',[2])
 for n in range(10):
  for _ in range(8):
   x=rng.randint(1,30);w=[rng.randint(1,x)for _ in range(n)];check('elevator',f'{n} {x}\n'+' '.join(map(str,w))+'\n',[binpack(sorted(w,reverse=True),x)])
 for n in range(9):
  for _ in range(4):
   v=[rng.randint(-10**9,10**9)for _ in range(1<<n)];ans=[sum(v[a]for a in range(1<<n)if a&s==a)for s in range(1<<n)];check('subset-sums',str(n)+'\n'+' '.join(map(str,v))+'\n',ans)
 check('subset-sums','3\n3 1 4 5 5 1 3 3\n',[3,4,7,13,8,10,15,25])
report={'status':'passed','compiled_programs':8,'UBSan_oracle_cases':sum(counts.values()),'per_program':counts,'source_examples':True,'boundaries':['zero/full/high-bit64 masks','word-block31/32/33/63/64/65/127/128/129','empty/full subsets','duplicate set insert and erase','unreachable shopping states and prices beyond32-bit totals','empty elevator and capacity10^18','negative SOS values']};(ROOT/'audit/PACKAGE03-BITS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
