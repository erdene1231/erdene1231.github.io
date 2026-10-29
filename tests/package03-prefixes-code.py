import json,itertools,random,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];rng=random.Random(98485);counts={'arrays':0,'range_queries':0,'grids':0,'rectangle_queries':0}
with tempfile.TemporaryDirectory()as td:
 p=Path(td)
 def compile(src,out):subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(out)],check=True)
 for k in ['one','two']:compile(R/f'audit/package03-work/prefixes-{k}.cpp',p/k)
 def arr(a,queries=None):
  n=len(a);qs=queries if queries is not None else[(l,r)for l in range(n)for r in range(l+1,n+1)];s=f'{n} {len(qs)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l+1} {r}\n'for l,r in qs)
  out=list(map(int,subprocess.check_output([str(p/'one')],input=s,text=True,timeout=20).split()));assert out==[sum(a[l:r])for l,r in qs];counts['arrays']+=1;counts['range_queries']+=len(qs)
 for n in range(6):
  for a in itertools.product([-2,0,3],repeat=n):arr(a)
 for _ in range(180):arr([rng.randint(-10**9,10**9)for _ in range(rng.randrange(31))])
 source=[1,3,4,8,6,1,4,2];signed=[4,-2,7,0,3];arr(source);arr(signed);arr([10**9]*200000,[(0,200000),(0,1),(199999,200000)]);arr([-10**9]*200000,[(0,200000),(1,199999)])
 def grid(a,n,m,qs=None):
  qs=qs if qs is not None else[(y1,x1,y2,x2)for y1 in range(n)for y2 in range(y1+1,n+1)for x1 in range(m)for x2 in range(x1+1,m+1)]
  s=f'{n} {m} {len(qs)}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n'+''.join(f'{y1+1} {x1+1} {y2} {x2}\n'for y1,x1,y2,x2 in qs)
  out=list(map(int,subprocess.check_output([str(p/'two')],input=s,text=True,timeout=25).split()));want=[sum(a[y][x]for y in range(y1,y2)for x in range(x1,x2))for y1,x1,y2,x2 in qs];assert out==want;counts['grids']+=1;counts['rectangle_queries']+=len(qs)
 for n in range(3):
  for m in range(3):
   for flat in itertools.product([-2,0,3],repeat=n*m):grid([list(flat[i*m:(i+1)*m])for i in range(n)],n,m)
 for _ in range(180):
  n=rng.randrange(7);m=rng.randrange(7);grid([[rng.randint(-100,100)for _ in range(m)]for _ in range(n)],n,m)
 A=[[2,-1,3,4],[0,5,-2,1],[7,2,0,-3]];grid(A,3,4);grid([[10**9]*1000 for _ in range(1000)],1000,1000,[(0,0,1000,1000),(999,999,1000,1000),(1,1,1000,1000)]);grid([[-10**9]*12 for _ in range(10)],10,12)
 # Include actual tested helpers to cover all half-open empty ranges, even zero dimensions.
 h1='#define main lessonMain\n#include "'+str(R/'audit/package03-work/prefixes-one.cpp')+'"\n#undef main\nint main(){int cases=0;for(int n=0;n<=12;n++){vector<ll>a(n);for(int i=0;i<n;i++)a[i]=i%5-2;auto p=prefix(a);assert(p.size()==size_t(n+1)&&p[0]==0);for(int l=0;l<=n;l++)for(int r=l;r<=n;r++){ll v=0;for(int i=l;i<r;i++)v+=a[i];assert(rangeSum(p,l,r)==v);cases++;}}cout<<cases;}'
 h2='#define main lessonMain\n#include "'+str(R/'audit/package03-work/prefixes-two.cpp')+'"\n#undef main\nint main(){int cases=0;for(int n=0;n<=4;n++)for(int m=0;m<=4;m++){vector<vector<ll>>a(n,vector<ll>(m));for(int i=0;i<n;i++)for(int j=0;j<m;j++)a[i][j]=i*7-j*3-4;Prefix2D p(n,m);p.build(a);for(int j=0;j<=m;j++)assert(p.p[0][j]==0);for(int i=0;i<=n;i++)assert(p.p[i][0]==0);for(int y1=0;y1<=n;y1++)for(int y2=y1;y2<=n;y2++)for(int x1=0;x1<=m;x1++)for(int x2=x1;x2<=m;x2++){ll v=0;for(int y=y1;y<y2;y++)for(int x=x1;x<x2;x++)v+=a[y][x];assert(p.sum(y1,x1,y2,x2)==v);cases++;}}cout<<cases;}'
 empty=[]
 for i,h in enumerate([h1,h2]):
  (p/f'h{i}.cpp').write_text(h);compile(p/f'h{i}.cpp',p/f'h{i}');empty.append(int(subprocess.check_output([str(p/f'h{i}')],text=True)))
 assert empty==[455,1225]
 pref=lambda a:[sum(a[:i])for i in range(len(a)+1)]
 table=[[sum(A[y][x]for y in range(i)for x in range(j))for j in range(5)]for i in range(4)]
 e={'source_array':source,'source_prefix_with_zero':pref(source),'source_inclusive_zero_query':[3,6],'source_query':19,'old_signed_array':signed,'old_signed_prefix':pref(signed),'old_signed_external_query':[2,4],'old_signed_query':5,'grid':A,'grid_prefix':table,'external_rectangle':[2,2,3,4],'internal_rectangle':[1,1,3,4],'corners':{'A':table[3][4],'B':table[3][1],'C':table[1][4],'D':table[1][1]},'rectangle_sum':3,'full_grid_sum':18,'single_cell_query':-2,'letter_layout':[['D','C'],['B','A']]}
 assert e['source_prefix_with_zero']==[0,1,4,8,16,22,23,27,29]and e['corners']=={'A':18,'B':9,'C':8,'D':2}
 (R/'audit/PACKAGE03-PREFIXES-EXAMPLES.json').write_text(json.dumps(e,indent=2)+'\n')
 report={'status':'passed','Cpp17_programs':2,'UBSan':True,'cases':counts,'one_helper_half_open_cases':empty[0],'two_helper_half_open_cases':empty[1],'includes_empty_internal_ranges':True,'includes_zero_dimensions':True,'oracle':'direct Python/unoptimized C++ sums over all requested original cells; independent of prefix recurrence','exhaustive_values':[-2,0,3],'stress_array_n':200000,'stress_grid':[1000,1000],'ll_negative_and_positive_sums':True,'source19_and_old_signed5_and_rectangle3_verified':True,'production_writes':0}
 (R/'audit/PACKAGE03-PREFIXES-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
