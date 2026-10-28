"""Exact native lesson programs with independent rectangle/interval oracles."""
from pathlib import Path
import subprocess,tempfile,json,random,hashlib
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['prefix-sums-2d','sliding-window']:
  d=json.loads((ROOT/f'audit/package02-lessons/{id}.json').read_text())['body'];blocks=d['sections'][7]['blocks'];pieces=[b['text']for b in blocks if b.get('language')=='C++17'];source=(ROOT/f'audit/package02-work/{id}.cpp').read_text();assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]==source;assert pieces==[b['text']for b in d['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
  src=Path(tmp)/(id+'.cpp');exe=Path(tmp)/id;src.write_text(source);build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(src),'-o',str(exe)],capture_output=True,text=True,check=True);assert not build.stderr,build.stderr
  def run(text):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=12,check=True).stdout.split()
  count=0
  if id=='prefix-sums-2d':
   for rows,cols in [(0,0),(0,4),(4,0),(1,1),(3,4)]+[(rng.randrange(1,8),rng.randrange(1,9))for _ in range(120)]:
    a=[[rng.randrange(-10**9,10**9+1)for _ in range(cols)]for _ in range(rows)];queries=[(t,l,b,r)for t in range(rows)for b in range(t+1,rows+1)for l in range(cols)for r in range(l+1,cols+1)]
    text=f'{rows} {cols} {len(queries)}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n'+''.join(f'{t+1} {l+1} {b} {r}\n'for t,l,b,r in queries)
    expected=[sum(a[i][j]for i in range(t,b)for j in range(l,r))for t,l,b,r in queries];assert list(map(int,run(text)))==expected;count+=len(queries)
   rows=cols=1000;queries=[(0,0,1000,1000),(999,999,1000,1000),(0,0,1,1)]+[(lambda t,l,b,r:(min(t,b),min(l,r),max(t,b)+1,max(l,r)+1))(*(rng.randrange(1000)for _ in range(4)))for _ in range(199997)]
   text='1000 1000 200000\n'+(' '.join(['1000000000']*1000)+'\n')*1000+''.join(f'{t+1} {l+1} {b} {r}\n'for t,l,b,r in queries);assert list(map(int,run(text)))==[(b-t)*(r-l)*10**9 for t,l,b,r in queries];count+=len(queries)
   helper=Path(tmp)/'grid-helper.cpp';helper.write_text('#define main lesson_main\n'+source+'\n#undef main\nint main(){Grid a={{2,-1,3,4},{0,5,-2,1},{7,2,0,-3}};auto p=build_prefix(a,4);if(p!=Grid{{0,0,0,0,0},{0,2,1,4,8},{0,2,6,7,12},{0,9,15,16,18}})return 1;for(int r=0;r<=3;++r)for(int c=0;c<=4;++c)if(rectangle_sum(p,r,c,r,c)!=0)return 2;return 0;}');h=Path(tmp)/'grid-helper';subprocess.run(['g++','-std=c++17','-O2',str(helper),'-o',str(h)],check=True);subprocess.run([str(h)],check=True)
   oracle='Direct nested-cell addition for every rectangle of random small signed grids; maximum 1000x1000 grid and200000queries with independent constant-cell area formula; full prefix-table/empty helper checks'
  else:
   def query(a,target):return int(run(f'{len(a)} {target}\n'+' '.join(map(str,a))+'\n')[0])
   def oracle_count(a,target):return sum(sum(a[i:j])==target for i in range(len(a))for j in range(i+1,len(a)+1))
   cases=[([],1),([1],1),([2],1),([1],2),([2,1,3,2,1],3),([10**9]*5,10**9)]+[([rng.randrange(1,15)for _ in range(rng.randrange(75))],rng.randrange(1,100))for _ in range(220)]
   for a,target in cases:assert query(a,target)==oracle_count(a,target);count+=1
   for a,target,expected in [([1]*200000,1,200000),([1]*200000,200000,1),([1]*200000,2,199999),([10**9]*200000,10**9,200000),([2]*200000,1,0)]:assert query(a,target)==expected;count+=1
   for a,target in [([0,1],1),([4,-1],3)]:assert query(a,target)!=oracle_count(a,target)
   oracle='Independent all-interval direct sums on positive arrays; maximum-size closed-form cases; actual failure witnesses verify zero/negative limitation claims'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split();reports.append({'lesson':id,'cases':count,'sample_passed':True,'compile_warnings':0,'program_sha256':hashlib.sha256(source.encode()).hexdigest(),'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Local complete programs and exact MN/EN fragments; native editor/semantic/publication gates separate'};(ROOT/'audit/PACKAGE02-GRID-WINDOW-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
