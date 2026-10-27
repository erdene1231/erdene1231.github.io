import json,subprocess,tempfile,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];rows=json.load(open(root/'audit/PART04-REVIEWED-NEW-TASKS.json'));cases=json.load(open(root/'audit/PART04-CONTENT04-SAMPLES.json'));result=[]
extra={'typical90_aa':[('4\n0\n00\n0\na1\n','1\n2\n4\n')],'typical90_al':[('1000000000000000000 1\n','1000000000000000000\n'),('999999999999999999 1000000000000000000\n','Large\n')],'typical90_bi':[('4\n1 5\n2 7\n3 1\n3 2\n','5\n7\n')],'typical90_ar':[('2 4\n10 20\n2 0 0\n3 1 0\n1 1 2\n3 1 0\n','20\n10\n')]}
with tempfile.TemporaryDirectory()as tmp:
 for item in cases:
  row=next(p for p in rows if p['ref']==item['ref']);code=next(b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code');source=Path(tmp)/'main.cpp';exe=Path(tmp)/'main';source.write_text(code);c=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow',str(source),'-o',str(exe)],capture_output=True,text=True);assert c.returncode==0 and not c.stderr,c.stderr
  checks=[(p['input'],p['output'])for p in item['samples']]+extra[item['ref']]
  for inp,out in checks:
   r=subprocess.run([str(exe)],input=inp,capture_output=True,text=True,timeout=3);assert r.returncode==0 and r.stdout.split()==out.split(),(item['ref'],inp,r.stdout,out)
  result.append({'ref':item['ref'],'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'official_samples':len(item['samples']),'focused_cases':len(extra[item['ref']]),'warnings':0,'status':'passed'})
(root/'audit/PART04-CONTENT04-CPP.json').write_text(json.dumps({'status':'passed','programs':result,'limits':'Official samples and focused edge cases; no judge submission/random-oracle claim.'},indent=2)+'\n');print(result)
