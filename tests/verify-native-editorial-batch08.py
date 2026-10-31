"""Six sequence/structure programs: strictness, boundaries, bases and huge exponents."""
import json,subprocess,random,time,hashlib,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];out=Path('/workspace/native-problem-editorials/batch08-code');out.mkdir(parents=True,exist_ok=True);refs=['abc005_4','typical90_ab','typical90_bw','typical90_bx','typical90_bz','typical90_cf'];samples=json.loads((ROOT/'audit/native-problem-editorials/batch08-source-samples.json').read_text())['records'];rng=random.Random(397);report=[]
for ref in refs:
 src=ROOT/'audit/native-problem-editorials/code'/f'{ref}.cpp';exe=out/ref;subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=undefined','-fno-sanitize-recover=undefined','-Wall','-Wextra','-Werror',str(src),'-o',str(exe)],check=True);runs=0;naive=0;edge_checks=[]
 def run(text):
  global runs
  p=subprocess.run([str(exe)],input=text,text=True,capture_output=True,timeout=30);assert p.returncode==0 and not p.stderr,(ref,p.stderr);runs+=1;return p.stdout.split()
 record=next(p for p in samples if p['ref']==ref)
 for s in record['samples']:assert run(s['input'])==s['output'].split(),(ref,'source sample')
 start=time.monotonic()
 if ref=='abc005_4':
  for _ in range(180):
   n=rng.randint(1,6);a=[[rng.randint(1,100)for j in range(n)]for i in range(n)];best=[0]*(n*n+1)
   for top in range(n):
    for bottom in range(top+1,n+1):
     for left in range(n):
      for right in range(left+1,n+1):
       area=(bottom-top)*(right-left);value=sum(a[i][j]for i in range(top,bottom)for j in range(left,right))
       for p in range(area,n*n+1):best[p]=max(best[p],value)
   inp=f'{n}\n'+'\n'.join(' '.join(map(str,row))for row in a)+f'\n{n*n}\n'+'\n'.join(map(str,range(1,n*n+1)))+'\n';assert run(inp)==list(map(str,best[1:]));naive+=1
  n=50;expected=[str(100*max(h*w for h in range(1,n+1)for w in range(1,n+1)if h*w<=p))for p in range(1,n*n+1)];assert run(f'{n}\n'+('100 '*n+'\n')*n+f'{n*n}\n'+'\n'.join(map(str,range(1,n*n+1)))+'\n')==expected
  assert run('3\n1 1 1\n1 1 1\n9 9 9\n1\n4\n')==['27'];edge_checks.append('N50/Q2500 positive-cell limit;all capacities checked;capacity is upper bound, not exact area')
 elif ref=='typical90_ab':
  for _ in range(100):
   n=rng.randint(1,30);rect=[];cells=[[0]*8 for i in range(8)]
   for i in range(n):
    lx=rng.randrange(8);ly=rng.randrange(8);rx=rng.randint(lx+1,8);ry=rng.randint(ly+1,8);rect.append((lx,ly,rx,ry))
    for x in range(lx,rx):
     for y in range(ly,ry):cells[x][y]+=1
   expected=[str(sum(v==k for row in cells for v in row))for k in range(1,n+1)];assert run(f'{n}\n'+'\n'.join(' '.join(map(str,r))for r in rect)+'\n')==expected;naive+=1
  n=100000;assert run(f'{n}\n'+'0 0 1000 1000\n'*n)==['0']*(n-1)+['1000000'];assert run('2\n0 0 1 1\n1 1 2 2\n')==['2','0'];edge_checks.append('half-open unit cells;touching edges/corners have zero area;N100000 fully overlapping atcoordinate1000')
 elif ref=='typical90_bw':
  assert all(9999999967%d for d in range(2,100000))
  import functools
  @functools.cache
  def depth(n):
   options=[1+max(depth(d),depth(n//d))for d in range(2,int(n**0.5)+1)if n%d==0];return min(options)if options else 0
  for n in list(range(2,352))+[rng.randint(352,3000)for _ in range(70)]:assert run(f'{n}\n')==[str(depth(n))];naive+=1
  for n,expected in [(2,0),(2**39,6),(10**12,5),(999983**2,1),(9999999967,0),(42,2),(48,3),(54,2)]:assert run(f'{n}\n')==[str(expected)]
  edge_checks.append('simultaneous split rounds not total splits;prime multiplicity;prime0;N<=1e12;2^39 requires6 rounds,large-prime square')
 elif ref=='typical90_bx':
  for _ in range(200):
   n=rng.randint(1,30);a=[rng.randint(1,100)for i in range(n)];total=sum(a);ok=any(10*sum(a[(l+j)%n]for j in range(length))==total for l in range(n)for length in range(1,n+1));assert run(f'{n}\n'+' '.join(map(str,a))+'\n')==['Yes'if ok else'No'];naive+=1
  for a,expected in [([1,18,1],'Yes'),([1,9,1,9],'No'),([1],'No'),([10**9]*100000,'Yes')]:assert run(f'{len(a)}\n'+' '.join(map(str,a))+'\n')==[expected]
  edge_checks.append('strictlypositivepieces;wraparound required;noncontiguous pair rejected;N1 andtotal1e14')
 elif ref=='typical90_bz':
  for _ in range(200):
   n=rng.randint(2,30);edges={(rng.randrange(i),i)for i in range(1,n)};possible=[(a,b)for a in range(n)for b in range(a+1,n)if(a,b)not in edges];rng.shuffle(possible);edges.update(possible[:rng.randint(0,len(possible))]);adj=[set()for i in range(n)]
   for a,b in edges:adj[a].add(b);adj[b].add(a)
   expected=sum(sum(j<i for j in adj[i])==1 for i in range(n));pairs=[(a+1,b+1)if rng.randrange(2)else(b+1,a+1)for a,b in edges];assert run(f'{n} {len(pairs)}\n'+'\n'.join(f'{a} {b}'for a,b in pairs)+'\n')==[str(expected)];naive+=1
  n=100000
  for edges,expected in [([(i,i+1)for i in range(1,n)],n-1),([(1,i)for i in range(2,n+1)],n-1),([(n,i)for i in range(1,n)],0)]:assert run(f'{n} {n-1}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+'\n')==[str(expected)]
  edge_checks.append('source connected/simple/undirected;exactlyone smaller-labelneighbor not degree1;unorderedendpointinput;N100000 chain/stars')
 else:
  for _ in range(220):
   n=rng.randint(1,80);s=''.join(rng.choice('ox')for i in range(n));expected=sum('o'in s[l:r]and'x'in s[l:r]for l in range(n)for r in range(l+1,n+1));assert run(f'{n}\n{s}\n')==[str(expected)];naive+=1
  n=1000000;assert run(f'{n}\n'+'o'*n+'\n')==['0'];assert run(f'{n}\n'+'ox'*(n//2)+'\n')==[str(n*(n-1)//2)];assert run('1\nx\n')==['0'];edge_checks.append('bothcharacters required;lastoccurrences use-1;N1;N1e6 uniform/alternating;answer499999500000')
 report.append({'ref':ref,'program_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'official_samples':len(record['samples']),'independent_naive_cases':naive,'source_edge_contract_checks':edge_checks,'limit_stress_passed':True,'oracle_and_stress_wall_seconds':round(time.monotonic()-start,3),'ubsan_warnings_as_errors':True,'program_runs':runs})
result={'status':'passed','records':report,'total_program_runs':sum(r['program_runs']for r in report),'limits':'Code checks only; bilingual/native content reviewed separately. Oracles use direct rectangle sums, unit-cell painting, recursive minimax split depths, all circular intervals, adjacency sets and direct substring enumeration. Host timing is not a judge-runtime claim.'};(ROOT/'audit/native-problem-editorials/batch08-code-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
