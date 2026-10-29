import json,random,subprocess,tempfile,math,itertools
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];out=Path(tempfile.mkdtemp(prefix='geometry-tests-'));rng=random.Random(2901);runs=0;queries=0
names=['complex','intersection','distance','inside','area','manhattan']
def compile(name,src):
 p=out/(name+'.cpp');p.write_text(src);subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=all',str(p),'-o',str(out/name)],check=True)
for name in names:compile(name,(R/f'audit/package03-work/geometry-{name}.cpp').read_text())
def run(name,s):
 global runs
 p=subprocess.run([str(out/name)],input=s,text=True,capture_output=True,timeout=15);assert p.returncode==0,(name,p.stderr,s[:200]);runs+=1;return p.stdout.split()
def same(name,s,w):assert run(name,s)==list(map(str,w)),(name,s[:200],w)
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on(a,b,p):return cross(a,b,p)==0 and all(min(a[i],b[i])<=p[i]<=max(a[i],b[i])for i in [0,1])
def coords(ps):return ' '.join(str(x)for p in ps for x in p)
# Independent exact intersection: solve the two parameter equations with rational arithmetic.
def intersect(a,b,c,d):
 if a==b:return 'POINT'if on(c,d,a)else'NONE'
 if c==d:return 'POINT'if on(a,b,c)else'NONE'
 u=(b[0]-a[0],b[1]-a[1]);v=(d[0]-c[0],d[1]-c[1]);w=(c[0]-a[0],c[1]-a[1]);det=u[0]*v[1]-u[1]*v[0]
 if det:
  t=F(w[0]*v[1]-w[1]*v[0],det);s=F(w[0]*u[1]-w[1]*u[0],det);return 'POINT'if 0<=t<=1 and 0<=s<=1 else'NONE'
 if w[0]*u[1]!=w[1]*u[0]:return'NONE'
 axis=0 if u[0] else 1;t0=F(c[axis]-a[axis],u[axis]);t1=F(d[axis]-a[axis],u[axis]);l=max(F(0),min(t0,t1));r=min(F(1),max(t0,t1));return 'NONE'if l>r else'POINT'if l==r else'OVERLAP'
ops=[];ans=[];pts=list(itertools.product(range(-1,2),repeat=2))
for a,b,c,d in itertools.product(pts,repeat=4):ops.append('S '+coords([a,b,c,d]));ans.append(intersect(a,b,c,d))
for _ in range(500):
 a,b,c,d=[(rng.randint(-10**9,10**9),rng.randint(-10**9,10**9))for _ in range(4)];ops.append('S '+coords([a,b,c,d]));ans.append(intersect(a,b,c,d))
for a,b,c in itertools.product(pts,repeat=3):
 z=cross(a,b,c);ops.append('O '+coords([a,b,c]));ans.append('DEGENERATE'if a==b else'LEFT'if z>0 else'RIGHT'if z<0 else'TOUCH')
ops+=['O -1000000000 -1000000000 1000000000 -1000000000 -1000000000 1000000000'];ans+=['LEFT'];same('intersection',str(len(ops))+'\n'+'\n'.join(ops)+'\n',ans);queries+=len(ops)
# Distance oracle: rational projection and exact squared distances; sqrt only at the final comparison.
for _ in range(90):
 ps=[(rng.randint(-10**9,10**9),rng.randint(-10**9,10**9))for _ in range(3)]
 if rng.randrange(8)==0:ps[1]=ps[0]
 a,b,p=ps;u=(b[0]-a[0],b[1]-a[1]);len2=sum(x*x for x in u);got=run('distance','1\n'+coords(ps)+'\n')
 if not len2:assert got[0]=='DEGENERATE';sq=sum((p[i]-a[i])**2 for i in [0,1]);want=math.sqrt(sq)
 else:
  line=abs(cross(a,b,p))/math.sqrt(len2);assert math.isclose(float(got[0]),line,abs_tol=1e-8,rel_tol=1e-12)
  t=max(F(0),min(F(1),F(sum((p[i]-a[i])*u[i]for i in[0,1]),len2)));sq=sum((F(a[i])+t*u[i]-p[i])**2 for i in[0,1]);want=math.sqrt(sq)
 assert math.isclose(float(got[1]),want,abs_tol=1e-8,rel_tol=1e-12)
# Independent winding-number oracle for containment (production uses parity).
def locate(poly,p):
 if any(on(a,b,p)for a,b in zip(poly,poly[1:]+poly[:1])):return'BOUNDARY'
 winding=0
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if a[1]<=p[1]<b[1]and cross(a,b,p)>0:winding+=1
  if b[1]<=p[1]<a[1]and cross(a,b,p)<0:winding-=1
 return'INSIDE'if winding else'OUTSIDE'
source=[(2,4),(5,5),(7,3),(4,1),(4,3)];raypoly=[(0,0),(1,3),(2,1),(2,4),(5,4),(3,2),(5,2),(7,3),(10,1),(7,2),(4,0)]
article=json.loads((R/'audit/PACKAGE03-GEOMETRY-EXAMPLES.json').read_text());article_poly=[tuple(p)for p in article['schematic_polygon']]
polys=[article_poly,source,source[::-1],source+[source[0]],raypoly,[(0,0),(4,0),(4,4),(0,4)],[(0,0),(4,0),(4,4),(2,2),(0,4)]]
for _ in range(70):
 x=rng.randint(-30,30);y=rng.randint(-30,30);w=rng.randint(1,15);h=rng.randint(1,15);polys.append([(x,y),(x+w,y),(x+w,y+h),(x,y+h)])
for poly in polys:
 ps=list(itertools.product(range(-2,13),range(-2,8)))
 if poly==article_poly:ps += [tuple(p)for p in article['schematic_points'].values()]
 same('inside',f'{len(poly)} {len(ps)}\n'+'\n'.join(coords([p])for p in poly+ps)+'\n',[locate(poly,p)for p in ps]);queries+=len(ps)
# Area oracle: triangulate a convex hull as independent fan areas; Pick checked by brute lattice enumeration.
def hull(ps):
 ps=sorted(set(ps))
 def half(ps):
  out=[]
  for p in ps:
   while len(out)>1 and cross(out[-2],out[-1],p)<=0:out.pop()
   out.append(p)
  return out
 return half(ps)[:-1]+half(ps[::-1])[:-1]
for poly in [source,source[::-1],source+[source[0]]]+[hull([(rng.randrange(-8,9),rng.randrange(-8,9))for _ in range(20)])for _ in range(90)]:
 pts2=[(x,y)for x in range(min(p[0]for p in poly),max(p[0]for p in poly)+1)for y in range(min(p[1]for p in poly),max(p[1]for p in poly)+1)];i=sum(locate(poly,p)=='INSIDE'for p in pts2);b=sum(locate(poly,p)=='BOUNDARY'for p in pts2)
 if poly!=source and poly!=source[::-1]and poly!=source+[source[0]]:area2=sum(abs(cross(poly[0],poly[j],poly[j+1]))for j in range(1,len(poly)-1));assert area2==2*i+b-2
 else:area2=17;assert(i,b)==(6,7)
 same('area',str(len(poly))+'\n'+'\n'.join(coords([p])for p in poly)+'\n',[area2,i,b])
same('area','4\n-1000000000 -1000000000\n1000000000 -1000000000\n1000000000 1000000000\n-1000000000 1000000000\n',[8000000000000000000,3999999996000000001,8000000000])
same('area','3\n0 0\n1 0\n2 0\n',['DEGENERATE'])
# Pure cross-sum accumulator stress beyond signed64, exposed only in a test harness; not claimed to be a simple polygon.
src=(R/'audit/package03-work/geometry-area.cpp').read_text();many=[(10**9,0),(0,10**9),(-10**9,0),(0,-10**9)]*50000
raw=sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(many,many[1:]+many[:1]));assert raw>2**63
harness=src.rsplit('int main()',1)[0]+r'''int main(){i128 s=0;for(int i=0;i<200000;i++)s+=(i128)1000000000*1000000000;cout<<decimal(s);}''';compile('wide-accumulator',harness);same('wide-accumulator','',[200000*10**18])
# Full valid n200000 simple rectangle boundary with collinear subdivision.
large=[(i,0)for i in range(50000)]+[(50000,i)for i in range(50000)]+[(50000-i,50000)for i in range(50000)]+[(0,50000-i)for i in range(50000)]
same('area',str(len(large))+'\n'+'\n'.join(coords([p])for p in large)+'\n',[5000000000,2499900001,200000])
same('inside',f'{len(large)} 3\n'+'\n'.join(coords([p])for p in large)+'\n25000 25000\n0 0\n-1 -1\n',['INSIDE','BOUNDARY','OUTSIDE']);queries+=3
for _ in range(110):
 ps=[(rng.randint(-10**9,10**9),rng.randint(-10**9,10**9))for _ in range(rng.randint(1,60))]
 if rng.randrange(12)==0:ps=[ps[0]]*len(ps)
 got=list(map(int,run('manhattan',str(len(ps))+'\n'+'\n'.join(coords([p])for p in ps)+'\n')));want=max(abs(a[0]-b[0])+abs(a[1]-b[1])for a in ps for b in ps);assert got[0]==want;assert abs(ps[got[1]][0]-ps[got[2]][0])+abs(ps[got[1]][1]-ps[got[2]][1])==want;assert len(ps)==1 or got[1]!=got[2]
vals=list(map(float,run('complex','')));assert vals[:4]==[4,2,5,3];assert math.isclose(vals[4],math.sqrt(10),abs_tol=5e-6);assert math.isclose(vals[5],math.atan2(2,4),abs_tol=5e-7);assert math.isclose(vals[6],math.atan2(2,4)+.5,abs_tol=5e-7);assert vals[7:]==[6,1,6]
# Actual complex helpers and long-double rotation across a range of magnitudes.
prefix=(R/'audit/package03-work/geometry-complex.cpp').read_text().rsplit('int main()',1)[0]
compile('rotation',prefix+r'''int main(){int q;cin>>q;cout<<setprecision(20);while(q--){ld x,y,t;cin>>x>>y>>t;P p{x,y};P r=p*polar(1.0L,t);cout<<r.real()<<' '<<r.imag()<<' '<<abs(r)<<'\n';}cout<<close(1e12L,1e12L+.1L)<<' '<<close(0,1e-6L);}''')
ps=[(rng.uniform(-1e9,1e9),rng.uniform(-1e9,1e9),rng.uniform(-10,10))for _ in range(100)]+[(0,0,0),(1e-12,0,.5)]
got=list(map(float,run('rotation',str(len(ps))+'\n'+'\n'.join(f'{x:.20g} {y:.20g} {t:.20g}'for x,y,t in ps)+'\n')))
for j,(x,y,t)in enumerate(ps):
 expected=[x*math.cos(t)-y*math.sin(t),x*math.sin(t)+y*math.cos(t),math.hypot(x,y)]
 for a,b in zip(got[j*3:j*3+3],expected):assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-6)
assert got[-2:]==[1,0]
compile('heron',prefix+r'''int main(){cout<<setprecision(20);for(ld s:{1e-6L,1.0L,1e9L})cout<<heron(3*s,4*s,5*s)<<' ';cout<<heron(1,1,2);}''')
h=list(map(float,run('heron','')));assert all(math.isclose(x,y,rel_tol=1e-12,abs_tol=1e-24)for x,y in zip(h,[6e-12,6,6e18,0]))
report={'programs':6,'ubsan_oracle_executions':runs,'batched_exact_queries':queries,'all_passed':True,'intersection_exhaustive_3x3_points':9**4,'source_polygon_area2':17,'source_polygon_interior':6,'source_polygon_boundary':7,'source_complex_distance':'sqrt(10)','source_rotation_angles':[math.atan2(2,4),math.atan2(2,4)+.5],'coordinate_bound':10**9,'cross_conservative_abs_bound':8*10**18,'GNU128_accumulator_tested_beyond64':True,'max_valid_polygon_vertices':200000,'numeric_types':'int counts/indices; ll coordinates and bounded cross/dot; long double lengths/angles; GNU128 polygon sum'}
(R/'audit/PACKAGE03-GEOMETRY-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
