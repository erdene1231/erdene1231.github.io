"""Six sequence/structure programs: strictness, boundaries, bases and huge exponents."""
import json,subprocess,random,time,hashlib,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch09-code');out.mkdir(parents=True,exist_ok=True);refs=['typical90_ac','typical90_bt','typical90_ca','typical90_cc','typical90_cg','typical90_ch'];samples=json.loads((ROOT/'audit/native-problem-editorials/batch09-source-samples.json').read_text())['records'];rng=random.Random(397);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0;edge_checks=[]
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='typical90_ac':
  for _ in range(180):
   w=rng.randint(2,40);n=rng.randint(1,80);a=[0]*w;ops=[];expected=[]
   for i in range(n):
    l=rng.randint(1,w);r=rng.randint(l,w);height=max(a[l-1:r])+1;a[l-1:r]=[height]*(r-l+1);ops.append(f'{l} {r}');expected.append(str(height))
   assert run(f'{w} {n}\n'+'\n'.join(ops)+'\n')==expected;naive+=1
  w=500000;n=250000;assert run(f'{w} {n}\n'+f'1 {w}\n'*n)==list(map(str,range(1,n+1)));assert run(f'{w} 4\n1 1\n{w} {w}\n1 {w}\n1 1\n')==['1','1','2','3'];edge_checks.append('range max plus range ASSIGN not addition;inclusiveinput converted tohalf-open;W500000,N250000;height<=N')
 elif ref=='typical90_bt':
  def oracle(grid):
   h=len(grid);w=len(grid[0]);points=[(r,c)for r in range(h)for c in range(w)if grid[r][c]=='.'];v=len(points);adj=[sum(1<<j for j,(x,y)in enumerate(points)if abs(r-x)+abs(c-y)==1)for r,c in points];best=-1
   for start in range(v):
    dp=[0]*(1<<v);dp[1<<start]=1<<start
    for mask in range(1<<v):
     ends=dp[mask]
     while ends:
      bit=ends&-ends;ends-=bit;last=bit.bit_length()-1
      if adj[last]>>start&1 and mask.bit_count()>=3:best=max(best,mask.bit_count())
      choices=adj[last]&~mask
      while choices:
       bit=choices&-choices;choices-=bit;dp[mask|bit]|=bit
   return best
  for _ in range(100):
   h,w=rng.choice([(1,1),(1,8),(2,3),(3,3)]);g=[''.join('.'if rng.random()<.7 else'#'for c in range(w))for r in range(h)]
   if all('.'not in row for row in g):g[0]='.'+g[0][1:]
   expected=oracle(g);assert run(f'{h} {w}\n'+'\n'.join(g)+'\n')==[str(expected)];naive+=1
  for g,expected in [(['....']*4,16),(['........']*2,16),(['.'*16],-1),(['.'], -1),(['..','..'],4)]:assert run(f'{len(g)} {len(g[0])}\n'+'\n'.join(g)+'\n')==[str(expected)]
  edge_checks.append('HW<=16,atleastoneplaincell;distinctvisitedcells;length>=3 closure,notbacktrackingedge;independent subsetDP;full4x4/2x8cycles')
 elif ref=='typical90_ca':
  from fractions import Fraction
  def oracle(a,b):
   h=len(a);w=len(a[0]);vars=[(i,j)for i in range(h-1)for j in range(w-1)];m=[]
   for i in range(h):
    for j in range(w):m.append([Fraction(int(x<=i<=x+1 and y<=j<=y+1))for x,y in vars]+[Fraction(b[i][j]-a[i][j])])
   row=0;pivots=[]
   for col in range(len(vars)):
    at=next((r for r in range(row,len(m))if m[r][col]),None)
    if at is None:continue
    m[row],m[at]=m[at],m[row];v=m[row][col];m[row]=[x/v for x in m[row]]
    for r in range(len(m)):
     if r!=row and m[r][col]:v=m[r][col];m[r]=[x-v*y for x,y in zip(m[r],m[row])]
    pivots.append((row,col));row+=1
   if any(not any(r[:-1])and r[-1]for r in m):return None
   assert len(pivots)==len(vars);coeff=[m[r][-1]for r,c in pivots];assert all(x.denominator==1 for x in coeff);return sum(abs(int(x))for x in coeff)
  for _ in range(180):
   h=rng.randint(2,4);w=rng.randint(2,4);a=[[rng.randint(20,40)for j in range(w)]for i in range(h)];b=[row[:]for row in a]
   if rng.randrange(2):
    for i in range(h-1):
     for j in range(w-1):
      v=rng.randint(-3,3)
      for di in range(2):
       for dj in range(2):b[i+di][j+dj]+=v
   else:b=[[rng.randint(0,60)for j in range(w)]for i in range(h)]
   expected=oracle(a,b);inp=f'{h} {w}\n'+'\n'.join(' '.join(map(str,r))for mat in[a,b]for r in mat)+'\n';assert run(inp)==(['No']if expected is None else['Yes',str(expected)]);naive+=1
  h=w=100;assert run(f'{h} {w}\n'+('0 '*w+'\n')*h+('1 '*w+'\n')*h)==['Yes','2500'];assert run('2 2\n0 0\n0 0\n1 0\n0 0\n')==['No'];assert run('2 2\n0 0\n0 0\n0 0\n0 0\n')==['Yes','0'];edge_checks.append('sourceH,W>=2;positive andnegative2x2 moves;independent rational Gaussian elimination uniqueness/minimum;100x100 and impossiblelastboundary')
 elif ref=='typical90_cc':
  for _ in range(160):
   n=rng.randint(1,12);k=rng.randint(1,12);points=[(rng.randint(1,12),rng.randint(1,12))for i in range(n)];expected=1
   for mask in range(1,1<<n):
    chosen=[points[i]for i in range(n)if mask>>i&1];xs,ys=zip(*chosen)
    if max(xs)-min(xs)<=k and max(ys)-min(ys)<=k:expected=max(expected,len(chosen))
   assert run(f'{n} {k}\n'+'\n'.join(f'{a} {b}'for a,b in points)+'\n')==[str(expected)];naive+=1
  assert run('2 1\n1 1\n2 2\n')==['2'];n=200000;points='1 1\n'*(n//2)+'5000 5000\n'*(n//2)
  for k,expected in [(1,n//2),(5000,n)]:assert run(f'{n} {k}\n'+points)==[str(expected)]
  edge_checks.append('inclusive difference<=K spansK+1 coordinatevalues;duplicatescountasdistinctstudents;N200000/coordinate5000;K1/K5000;~100MBgrid')
 elif ref=='typical90_cg':
  for _ in range(180):
   k=rng.randint(1,100000);expected=0;a=1
   while a*a*a<=k:
    b=a
    while a*b*b<=k:
     if k%(a*b)==0:expected+=1
     b+=1
    a+=1
   assert run(f'{k}\n')==[str(expected)];naive+=1
  def burnside(k):
   exps=[];p=2
   while p*p<=k:
    e=0
    while k%p==0:k//=p;e+=1
    if e:exps.append(e)
    p+=1
   if k>1:exps.append(1)
   ordered=swap=1
   for e in exps:ordered*=(e+1)*(e+2)//2;swap*=e//2+1
   cycle=int(all(e%3==0 for e in exps));return(ordered+3*swap+2*cycle)//6
  for k in [1,7,42,192,10**12,9999999967,999983**2,2**39,735134400000]:assert run(f'{k}\n')==[str(burnside(k))]
  edge_checks.append('positivea<=b<=c;K1,prime,square,cube andhighdivisorcount<=1e12;independentBurnsidefactor-exponent oracle;divisionguardsavoidrawproducts')
 else:
  mod=1000000007
  for _ in range(100):
   n=rng.randint(3,5);q=rng.randint(1,6);queries=[(*sorted(rng.sample(range(n),3)),rng.randrange(4))for i in range(q)];covered=set(i for x,y,z,w in queries for i in[x,y,z]);expected=sum(all(a[x]|a[y]|a[z]==w for x,y,z,w in queries)for a in itertools.product(range(4),repeat=n))*pow(2,58*(n-len(covered)),mod)%mod;inp=f'{n} {q}\n'+'\n'.join(f'{x+1} {y+1} {z+1} {w}'for x,y,z,w in queries)+'\n';assert run(inp)==[str(expected)];naive+=1
  n=12
  for w in[0,(1<<59),(1<<60)-1]:
   expected=pow(7,w.bit_count(),mod)*pow(2,60*(n-3),mod)%mod;assert run(f'{n} 50\n'+f'1 2 3 {w}\n'*50)==[str(expected)]
  assert run('3 2\n1 2 3 0\n1 2 3 1\n')==['0'];edge_checks.append('all60bits,highbit59,ORnotXOR;N12/Q50;duplicatedconstraints,contradiction,unreferencedvariablesretain2^60choices;fullintegerassignment oracle')
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'source_edge_contract_checks':edge_checks,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Code checks only; bilingual/native content reviewed separately. Oracles use direct height arrays, subset path DP, rational Gaussian elimination, all point subsets, factor-triple enumeration/Burnside and full small-integer assignments. Host timing is not a judge-runtime claim.'};(ROOT/'audit/native-problem-editorials/batch09-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
