"""Independent calculations for the nine original factual-restatement examples."""
import itertools,json,math
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
records=json.loads((ROOT/'audit/atcoder-expansion/new-native-documents.json').read_text())
def solve(ref,text):
 a=list(map(int,text.split())) if ref!='typical90_bt' else None
 if ref=='typical90_ab':
  n=a[0];r=[a[i:i+4]for i in range(1,len(a),4)];counts=[0]*(n+1)
  for x in range(max(t[2]for t in r)):
   for y in range(max(t[3]for t in r)):
    k=sum(lx<=x<rx and ly<=y<ry for lx,ly,rx,ry in r);counts[k]+=1
  return '\n'.join(map(str,counts[1:]))
 if ref=='typical90_ac':
  w,n=a[:2];h=[0]*w;ans=[]
  for l,r in zip(a[2::2],a[3::2]):
   z=max(h[l-1:r])+1;h[l-1:r]=[z]*(r-l+1);ans.append(z)
  return '\n'.join(map(str,ans))
 if ref=='typical90_bt':
  lines=text.splitlines();h,w=map(int,lines[0].split());grid=lines[1:];best=-1
  def dfs(start,p,seen):
   nonlocal best
   x,y=divmod(p,w)
   for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if not(0<=nx<h and 0<=ny<w)or grid[nx][ny]=='#':continue
    q=nx*w+ny
    if q==start and len(seen)>=3:best=max(best,len(seen))
    elif q not in seen:dfs(start,q,seen|{q})
  for p in range(h*w):
   if grid[p//w][p%w]=='.':dfs(p,p,{p})
  return str(best)
 if ref=='typical90_bw':return str(split_depth(a[0]))
 if ref=='typical90_ca':
  h,w=a[:2];assert h==2 and w==3;v=a[2:];before=[v[:w],v[w:2*w]];after=[v[2*w:3*w],v[3*w:4*w]];answers=[]
  # Enumerate signed operation counts for the only two 2x2 positions.
  for x,y in itertools.product(range(-5,6),repeat=2):
   got=[[before[i][j]+(x if j<2 else 0)+(y if j>0 else 0)for j in range(w)]for i in range(h)]
   if got==after:answers.append(abs(x)+abs(y))
  return 'Yes\n'+str(min(answers))if answers else'No'
 if ref=='typical90_cc':
  n,k=a[:2];points=list(zip(a[2::2],a[3::2]));best=0
  for mask in range(1,1<<n):
   chosen=[p for i,p in enumerate(points)if mask>>i&1]
   if max(p[0]for p in chosen)-min(p[0]for p in chosen)<=k and max(p[1]for p in chosen)-min(p[1]for p in chosen)<=k:best=max(best,len(chosen))
  return str(best)
 if ref=='typical90_cg':
  k=a[0];return str(sum(k%(x*y)==0 and k//(x*y)>=y for x in range(1,k+1)for y in range(x,k//x+1)))
 if ref=='typical90_ch':
  n,q=a[:2];constraints=[a[i:i+4]for i in range(2,len(a),4)];bound=1<<max(c[3]for c in constraints).bit_length()
  # In this example all indices occur in a constraint, so no unbounded free bit.
  assert {i for c in constraints for i in c[:3]}==set(range(1,n+1))
  return str(sum(all(v[x-1]|v[y-1]|v[z-1]==w for x,y,z,w in constraints)for v in itertools.product(range(bound),repeat=n)))
 if ref=='abc005_4':
  n=a[0];v=a[1:1+n*n];d=[v[i*n:(i+1)*n]for i in range(n)];q=a[1+n*n];queries=a[2+n*n:];assert len(queries)==q;ans=[]
  for limit in queries:
   ans.append(max(sum(d[i][j]for i in range(t,b)for j in range(l,r))for t in range(n)for b in range(t+1,n+1)for l in range(n)for r in range(l+1,n+1)if(b-t)*(r-l)<=limit))
  return '\n'.join(map(str,ans))
 raise AssertionError(ref)
@lru_cache(None)
def split_depth(n):
 factors=[d for d in range(2,math.isqrt(n)+1)if n%d==0]
 return 0 if not factors else 1+min(max(split_depth(d),split_depth(n//d))for d in factors)
for p in records:
 codes=[b['text']for b in p['statement']['sections'][4]['blocks']if b['type']=='code'];assert len(codes)==2;assert solve(p['ref'],codes[0]).strip()==codes[1].strip(),p['ref']
 assert codes==[b['text']for b in p['statement']['translations']['en']['sections'][4]['blocks']if b['type']=='code']
for n in range(2,301):
 v=n;omega=0
 for d in range(2,math.isqrt(n)+1):
  while v%d==0:omega+=1;v//=d
 if v>1:omega+=1
 assert split_depth(n)==(omega-1).bit_length()
assert solve('typical90_bt','1 3\n...\n')=='-1'
report={'status':'passed','original_example_pairs':9,'split_process_small_number_checks':299,'cycle_without_solution_check':True,'independent_methods':['unit-square coverage','direct interval heights','exhaustive simple cycles','optimal factor split-depth recursion','signed operation enumeration','subset enumeration','sorted factor triples','exhaustive OR arrays','all rectangles per query']}
(ROOT/'audit/atcoder-expansion/original-example-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
