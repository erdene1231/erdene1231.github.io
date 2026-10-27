"""Compile the exact authored full programs; seeded independent small-case oracles."""
import hashlib,itertools,json,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];rows=json.loads((ROOT/'audit/PART04-REVIEWED-NEW-TASKS.json').read_text());rng=random.Random(41006);report=[]
with tempfile.TemporaryDirectory(prefix='part04-editorial-')as td:
 for ref in ['typical90_a','typical90_d','typical90_g']:
  doc=next(r['editorial']for r in rows if r['source']=='AtCoder'and r['ref']==ref);code=next(b['text']for s in doc['sections']for b in s['blocks']if b['type']=='code');src=Path(td)/(ref+'.cpp');binary=Path(td)/ref;src.write_text(code)
  assert any(s['title']=='C++ хэрэгжүүлэлтийн хэсгүүд'for s in doc['sections']);assert '\t' not in code;assert all(not line.startswith(' ')or(len(line)-len(line.lstrip()))%4==0 for line in code.splitlines());
  built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow','-Wconversion','-pedantic',str(src),'-o',str(binary)],capture_output=True,text=True,check=True);assert not built.stderr,built.stderr
  for case in range(60):
   if ref=='typical90_a':
    length=rng.randint(5,100);n=rng.randint(1,min(7,length-1));cuts=sorted(rng.sample(range(1,length),n));k=rng.randint(1,n);data=f'{n} {length}\n{k}\n'+ ' '.join(map(str,cuts))+'\n';expected=[max(min(b-a for a,b in zip((0,)+choice,choice+(length,)))for choice in itertools.combinations(cuts,k))]
   elif ref=='typical90_d':
    h,w=rng.randint(1,6),rng.randint(1,6);a=[[rng.randint(1,50)for _ in range(w)]for _ in range(h)];data=f'{h} {w}\n'+'\n'.join(' '.join(map(str,row))for row in a)+'\n';expected=[sum(a[i])+sum(a[r][j]for r in range(h))-a[i][j]for i in range(h)for j in range(w)]
   else:
    n=rng.randint(1,9);a=[rng.randint(1,100)for _ in range(n)];queries=[rng.randint(1,120)for _ in range(10)];data=f'{n}\n'+ ' '.join(map(str,a))+'\n10\n'+'\n'.join(map(str,queries))+'\n';expected=[min(abs(x-q)for x in a)for q in queries]
   got=list(map(int,subprocess.run([str(binary)],input=data,capture_output=True,text=True,check=True,timeout=2).stdout.split()));assert got==expected,(ref,case,data,expected,got)
  report.append({'ref':ref,'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'cases':60,'compile_warnings':0,'review':'4-space indentation; descriptive role names; state/preprocessing/algorithm/output explanations reviewed against exact code.'})
result={'status':'passed','seed':41006,'cases':180,'programs':report};(ROOT/'audit/PART04-AUTHORED-EDITORIAL-TESTS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
