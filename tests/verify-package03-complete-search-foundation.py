import subprocess,tempfile,random,itertools,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];rng=random.Random(5);cases=0
with tempfile.TemporaryDirectory()as d:
 ex={}
 for name in ['mitm','grid','queens','subsets','permutations']:
  out=Path(d)/name;r=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-fsanitize=undefined','-fno-sanitize-recover=all',str(root/f'audit/package03-work/complete-search-{name}.cpp'),'-o',str(out)],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr;ex[name]=out
 def run(name,inp):return subprocess.check_output([str(ex[name])],input=inp,text=True,timeout=60).strip()
 for a,target in [([2,4,5,9],15),([2,4,5,9],10),([],0),([],1)]+[([rng.randrange(-20,21)for _ in range(rng.randrange(13))],rng.randrange(-40,41))for _ in range(150)]:
  sums={sum(a[i]for i in range(len(a))if mask>>i&1)for mask in range(1<<len(a))};assert run('mitm',f'{len(a)} {target}\n'+ ' '.join(map(str,a))+'\n')==('YES'if target in sums else'NO');cases+=1
 for n in range(1,9):
  expected=sum(len({i+p[i]for i in range(n)})==n and len({i-p[i]for i in range(n)})==n for p in itertools.permutations(range(n)));assert int(run('queens',f'{n}\n'))==expected;cases+=1
 def brute(n):
  seen={(0,0)}
  def f(r,c):
   if len(seen)==n*n:return int((r,c)==(n-1,n-1))
   ans=0
   for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
    p=(r+dr,c+dc)
    if 0<=p[0]<n and 0<=p[1]<n and p not in seen:
     seen.add(p);ans+=f(*p);seen.remove(p)
   return ans
  return f(0,0)
 for n in range(1,5):
  expected=brute(n)
  for level in range(5):assert int(run('grid',f'{n} {level}\n'))==expected;cases+=1
 assert run('grid','7 4\n')=='111712';cases+=1
 for name,marker,limit in [('subsets','MASK',9),('permutations','NEXT',8)]:
  for n in range(limit):
   lines=run(name,f'{n}\n').splitlines();at=lines.index(marker);left=lines[1:at];right=lines[at+1:]
   if name=='subsets':expected={tuple(i for i in range(n)if mask>>i&1)for mask in range(1<<n)}
   else:expected=set(itertools.permutations(range(n)))
   parse=lambda v:tuple(map(int,v[1:-1].split()))
   assert set(map(parse,left))==expected and set(map(parse,right))==expected
   assert len(left)==len(expected)==len(right);cases+=1
 report={'status':'passed','foundation_only_not_lesson_complete':True,'programs':5,'UBSan':True,'checks':cases,'source_7x7_count':111712,'source_queens8':92,'independent_small_grid_and_permutation_oracles':True,'remaining':'Full bilingual lesson, source figure review, editor/reader and guarded publication','production_writes':0};(root/'audit/PACKAGE03-COMPLETE-SEARCH-FOUNDATION.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
