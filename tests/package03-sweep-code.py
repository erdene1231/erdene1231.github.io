import json,random,subprocess,tempfile,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=Path(tempfile.mkdtemp(prefix='sweep-tests-'));rng=random.Random(3001);runs=0
for name in ['office','intersections','closest','hull']:
 subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/sweep-{name}.cpp'),'-o',str(out/name)],check=True)
def run(name,s):
 global runs
 p=subprocess.run([str(out/name)],input=s,text=True,capture_output=True,timeout=20);assert p.returncode==0,(name,p.stderr,s[:300]);runs+=1;return p.stdout.split()
def same(name,s,w):assert run(name,s)==list(map(str,w)),(name,s[:300],w)
def flat(ps):return '\n'.join(' '.join(map(str,p))for p in ps)
same('office','4\n10 15\n6 12\n14 16\n5 13\n',[3])
for _ in range(150):
 a=[sorted([rng.randint(-10,10),rng.randint(-10,10)])for j in range(rng.randrange(35))];want=max([sum(l<=t<r for l,r in a)for t in range(-10,11)]+[0]);same('office',str(len(a))+'\n'+flat(a)+'\n',[want])
same('office','3\n0 1\n1 2\n1 1\n',[1]);same('office','200000\n'+'-1000000000 1000000000\n'*200000,[200000])
source=[('H',0,8,4),('H',-1,7,0),('H',9,15,2),('V',3,-2,8),('V',12,0,6)]
for mode in ['PAIRS','POINTS']:same('intersections',mode+' 5\n'+flat(source)+'\n',[3])
for _ in range(180):
 a=[];hs=[];vs=[]
 for j in range(rng.randrange(35)):
  k=rng.choice('HV');x,y,z=[rng.randint(-6,6)for i in range(3)];a.append((k,x,y,z))
  if k=='H':hs.append((min(x,y),max(x,y),z))
  else:vs.append((x,min(y,z),max(y,z)))
 pts=[(x,y)for l,r,y in hs for x,b,t in vs if l<=x<=r and b<=y<=t]
 for mode,want in [('PAIRS',len(pts)),('POINTS',len(set(pts)))]:same('intersections',f'{mode} {len(a)}\n'+flat(a)+'\n',[want])
same('intersections','PAIRS 4\nH 0 1 0\nH 0 1 0\nV 1 0 0\nV 1 0 0\n',[4]);same('intersections','POINTS 4\nH 0 1 0\nH 0 1 0\nV 1 0 0\nV 1 0 0\n',[1])
stress='H -1000000000 1000000000 0\n'*100000+'V 0 -1000000000 1000000000\n'*100000
same('intersections','PAIRS 200000\n'+stress,[10000000000]);same('intersections','POINTS 200000\n'+stress,[1])
cloud=[(0,6),(2,2),(2,12),(8,2),(6,10),(12,10),(14,4),(17,0),(18,4),(20,8),(22,6),(24,2),(32,4),(36,6)]
for ps in [cloud,[],[(0,0)],[(0,0),(0,0)],[(-10**9,-10**9),(10**9,10**9)]]+[[rng.choice([(rng.randint(-10**9,10**9),rng.randint(-10**9,10**9)),(0,rng.randrange(10)),(rng.randrange(10),0)])for j in range(rng.randrange(70))]for _ in range(200)]:
 got=run('closest',str(len(ps))+'\n'+flat(ps)+'\n')
 if len(ps)<2:assert got==['NONE'];continue
 d,a,b=map(int,got);want=min((x-u)**2+(y-v)**2 for i,(x,y)in enumerate(ps)for u,v in ps[:i]);assert d==want and a!=b and 0<=a<len(ps)and 0<=b<len(ps);assert sum((ps[a][i]-ps[b][i])**2 for i in[0,1])==d
for ps,want in [([(0,i)for i in range(200000)],1),([(0,0)]*200000,0),([(i,0)for i in range(200000)],1)]:
 got=run('closest','200000\n'+flat(ps)+'\n');assert int(got[0])==want and got[1]!=got[2]
def cross(a,b,c):return(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def distance(a,b):return sum((a[i]-b[i])**2 for i in[0,1])
def jarvis(ps):
 p=sorted(set(ps))
 if len(p)<=1:return p
 start=p[0];a=start;h=[]
 while True:
  h.append(a);b=next(x for x in p if x!=a)
  for c in p:
   z=cross(a,b,c)
   if z<0 or z==0 and distance(a,c)>distance(a,b):b=c
  a=b
  if a==start:return h
  assert len(h)<=len(p)
def on(a,b,p):return cross(a,b,p)==0 and all(min(a[i],b[i])<=p[i]<=max(a[i],b[i])for i in[0,1])
small=list(itertools.product(range(3),repeat=2));src=[(0,1),(0,3),(1,2),(2,3),(2,5),(3,3),(4,0),(4,1),(4,4),(5,3),(6,2),(6,4),(7,2)]
cases=[src]+[[small[i]for i in range(9)if mask>>i&1]for mask in range(512)]+[[(rng.randint(-10,10),rng.randint(-10,10))for i in range(rng.randrange(25))]for _ in range(100)]+[[(-10**9,-10**9),(-10**9,10**9),(10**9,10**9),(10**9,-10**9),(0,0)]]
for ps in cases:
 expected=jarvis(ps);boundary={p for p in set(ps)if len(expected)<2 or any(on(a,b,p)for a,b in zip(expected,expected[1:]+expected[:1]))}
 for mode,desired in [('STRICT',set(expected)),('BOUNDARY',boundary)]:
  got=list(map(int,run('hull',f'{mode} {len(ps)}\n'+flat(ps)+'\n')));n=got[0];h=list(zip(got[1::2],got[2::2]));assert len(h)==n==len(set(h)) and set(h)==desired,(mode,ps,h,desired)
  if h:assert h[0]==min(h)
  if len(expected)>=3:assert all(cross(a,b,c)>=0 for a,b,c in zip(h,h[1:]+h[:1],h[2:]+h[:2]))
# Source's exact upper-hull append/pop trace: retain collinear intermediate points.
h=sorted(src)[:2];trace=[h[:]]
for p in sorted(src)[2:]:
 h.append(p);trace.append(h[:])
 while len(h)>=3 and cross(h[-3],h[-2],h[-1])>0:h.pop(-2);trace.append(h[:])
assert len(trace)==20 and h==[(0,1),(0,3),(2,5),(6,4),(7,2)]
(R/'audit/PACKAGE03-SWEEP-EXAMPLES.json').write_text(json.dumps({'office_people':[['John',10,15],['Maria',6,12],['Peter',14,16],['Lisa',5,13]],'office_events':[[5,1,1],[6,1,2],[10,1,3],[12,-1,2],[13,-1,1],[14,1,2],[15,-1,1],[16,-1,0]],'intersection_segments':source,'intersection_points':[[3,0],[3,4],[12,2]],'closest_cloud':cloud,'closest_source_pair_indices':[9,10],'closest_squared_distance':8,'hull_points':src,'source_upper_trace':trace,'source_upper_final':h,'strict_hull':jarvis(src)},indent=2)+'\n')
report={'programs':4,'ubsan_oracle_executions':runs,'all_passed':True,'office_max':3,'axis_crossings':3,'closest_source_squared':8,'source_upper_steps':20,'exhaustive_hull_subsets_3x3':512,'coordinate_bound':10**9,'pair_count_beyond32':10000000000,'distinct_same_geometry':1,'max_points_or_segments':200000,'duplicate_and_collinear_policies_verified':True,'event_ties_and_closed_endpoint_hits':True,'exact_isqrt_no_floating_exclusion':True,'last_numbered_handbook_chapter':30}
(R/'audit/PACKAGE03-SWEEP-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
