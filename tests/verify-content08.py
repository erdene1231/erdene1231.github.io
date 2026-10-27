"""Source samples and independent small/grid/enumeration checks for content08 programs."""
import hashlib,itertools,json,math,random,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));records=json.load(open(root/'audit/PART04-CONTENT08-SAMPLES.json'));rng=random.Random(81027);results=[]
def grid_optimum(height,width):
 squares=[sum(1<<((r+dr)*width+c+dc)for dr in range(2)for dc in range(2))for r in range(height-1)for c in range(width-1)]
 return max(mask.bit_count()for mask in range(1<<(height*width))if all((mask&square).bit_count()<=1 for square in squares))
def composition_count(total):
 if total%9:return 0
 # For each possible length, bounded positive compositions via inclusion/exclusion.
 result=0
 for length in range(1,total+1):
  for excluded in range(min(length,(total-length)//9)+1):
   result+=(-1)**excluded*math.comb(length,excluded)*math.comb(total-9*excluded-1,length-1)
 return result%1000000007
def convert_reference(numeral,iterations):
 for _ in range(iterations):
  value=int(numeral,8);power=1
  while power*9<=value:power*=9
  digits=[]
  while power:
   digit=0
   while value>=power:value-=power;digit+=1
   digits.append('5'if digit==8 else str(digit));power//=9
  numeral=''.join(digits)
 return numeral
def graph_input(n,edges):return f'{n} {len(edges)}\n'+'\n'.join(f'{a} {b}'for a,b in edges)+'\n'
with tempfile.TemporaryDirectory()as tmp:
 for record in records:
  suffix=record['ref'].split('_')[-1];row=next(p for p in rows if p['ref']==record['ref']);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');src=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';src.write_text(code)
  built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(src),'-o',str(exe)],capture_output=True,text=True);assert built.returncode==0 and not built.stderr,built.stderr
  cases=[(s['input'],s['output'])for s in record['samples']];oracle_cases=0
  if suffix=='ag':
   for height,width in itertools.product(range(1,5),repeat=2):cases.append((f'{height} {width}\n',str(grid_optimum(height,width))));oracle_cases+=1
  else:
   for _ in range(40):
    if suffix=='av':
     n=rng.randint(1,7);minutes=rng.randint(1,2*n);tasks=[]
     for i in range(n):
      full=rng.randint(3,40);tasks.append((full,rng.randint(full//2+1,full-1)))
     expected=max(sum(0 if t==0 else tasks[i][1]if t==1 else tasks[i][0]for i,t in enumerate(allocation))for allocation in itertools.product(range(3),repeat=n)if sum(allocation)<=minutes);inp=f'{n} {minutes}\n'+'\n'.join(f'{a} {b}'for a,b in tasks)+'\n'
    elif suffix=='ap':
     total=rng.randint(1,90);inp=f'{total}\n';expected=composition_count(total)
    elif suffix=='bc':
     n=rng.randint(5,11);modulus=rng.randint(1,100);target=rng.randrange(modulus);values=[rng.randrange(1000000001)for i in range(n)];expected=sum(math.prod(choice)%modulus==target for choice in itertools.combinations(values,5));inp=f'{n} {modulus} {target}\n'+' '.join(map(str,values))+'\n'
    elif suffix=='bo':
     numeral=oct(rng.randrange(1<<60))[2:];iterations=rng.randint(1,100);inp=f'{numeral} {iterations}\n';expected=convert_reference(numeral,iterations)
    else:
     n=rng.randint(2,12);labels=rng.sample(range(1,n+1),n);edges={tuple(sorted((labels[i],labels[rng.randrange(i)])))for i in range(1,n)};candidates=[e for e in itertools.combinations(range(1,n+1),2)if e not in edges];edges.update(rng.sample(candidates,rng.randrange(len(candidates)+1)))
     adjacency=[[False]*(n+1)for i in range(n+1)]
     for a,b in edges:adjacency[a][b]=adjacency[b][a]=True
     expected=sum(sum(adjacency[v][u]for u in range(1,v))==1 for v in range(1,n+1));oriented=[e if rng.randrange(2)else e[::-1]for e in edges];rng.shuffle(oriented);inp=graph_input(n,oriented)
    cases.append((inp,str(expected)));oracle_cases+=1
  if suffix=='ag':focused=[('100 100\n','2500'),('1 100\n','100'),('99 99\n','2500')]
  elif suffix=='av':focused=[('200000 400000\n'+'1000000000 999999999\n'*200000,'200000000000000'),('2 2\n3 2\n3 2\n','4'),('1 2\n3 2\n','3')]
  elif suffix=='ap':
   # Independent order-ten recurrence from (1-2x+x^10)F(x)=1-x.
   recent=[1]+[1<<(i-1)for i in range(1,10)]
   for total in range(10,100000):recent.append((2*recent[-1]-recent[-10])%1000000007);recent.pop(0)
   focused=[('100000\n','0'),('99999\n',str(recent[-1])),('9\n','256')]
  elif suffix=='bc':focused=[('100 1 0\n'+'0 '*100+'\n',str(math.comb(100,5))),('100 1000000000 0\n'+'1000000000 '*100+'\n',str(math.comb(100,5))),('5 1000000000 999999999\n'+'999999999 '*5+'\n','1'),('5 12 0\n2 3 4 5 6\n','1')]
  elif suffix=='bo':focused=[('0 100\n','0'),('7 100\n','7'),('10 1\n','5'),('7'*20+' 100\n',convert_reference('7'*20,100))]
  else:focused=[(graph_input(100000,[(100000,i)for i in range(1,100000)]),'0'),(graph_input(100000,[(i,1)for i in range(2,100001)]),'99999'),(graph_input(7,list(itertools.combinations(range(1,8),2))),'1')]
  cases+=focused
  for inp,out in cases:
   run=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=10);assert run.returncode==0 and run.stdout.split()==out.split(),(suffix,inp[:200],run.stdout[:200],out[:200])
  results.append({'ref':record['ref'],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'official_samples':len(record['samples']),'independent_oracles':oracle_cases,'focused_boundary_cases':len(focused),'warnings':0,'status':'passed'})
(root/'audit/PART04-CONTENT08-CPP.json').write_text(json.dumps({'status':'passed','seed':81027,'programs':results,'oracle_methods':['all cell subsets for all sixteen grids up to4x4','all0/1/2-minute allocations','bounded compositions by inclusion-exclusion for every length','arbitrary-precision full combination products','builtin octal parse plus greedy positional base-nine conversion','adjacency-matrix lower-neighbor scans on connected random labeled graphs'],'focused_methods':'Large digit-sum boundary also checked by independent generating-function recurrence.','limits':'Local executable checks; no judge submission.'},indent=2)+'\n');print(results)
