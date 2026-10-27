"""Compile exact authored code; official samples, witness predicates and focused edge cases."""
from pathlib import Path
import json,hashlib,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
rows=json.loads((ROOT/'audit/PART04-REVIEWED-NEW-TASKS.json').read_text());evidence=json.loads((ROOT/'audit/PART04-ATCODER-CONTENT06-SAMPLES.json').read_text())['records'];results=[]
def verify(ref,inp,expected,actual):
 if ref!='typical90_z':assert actual.split()==expected.split(),(ref,inp,expected,actual)
 else:
  tokens=list(map(int,inp.split()));n=tokens[0];chosen=list(map(int,actual.split()));assert len(chosen)==n//2 and len(set(chosen))==len(chosen) and all(1<=v<=n for v in chosen),(ref,'invalid vertex set',actual)
  selected=set(chosen);assert all(a not in selected or b not in selected for a,b in zip(tokens[1::2],tokens[2::2])),(ref,'adjacent selected',actual)
extra={
 'typical90_b':[('1\n',''),('4\n','(())\n()()\n')],
 'typical90_c':[('3\n1 2\n2 3\n','3\n')],
 'typical90_f':[('4 4\nbaaa\n','baaa\n'),('4 2\nzaza\n','aa\n')],
 'typical90_h':[('6\natcode\n','0\n'),('8\naatcoder\n','2\n')],
 'typical90_j':[('1\n2 100\n1\n1 1\n','0 100\n')],
 'typical90_l':[('1 1\n3\n2 1 1 1 1\n1 1 1\n2 1 1 1 1\n','No\nYes\n')],
 'typical90_m':[('3 2\n1 2 10000\n2 3 10000\n','20000\n20000\n20000\n')],
 'typical90_n':[('3\n1 5 9\n2 6 8\n','3\n')],
 'typical90_u':[('3 1\n1 2\n','0\n'),('3 3\n1 2\n2 3\n3 1\n','3\n')],
 'typical90_v':[('1000000000000000000 999999999999999999 999999999999999998\n','2999999999999999994\n')],
 'typical90_x':[('1 1\n5\n5\n','No\n'),('1 2\n5\n5\n','Yes\n')],
 'typical90_z':[('2\n1 2\n','')]
}
with tempfile.TemporaryDirectory(prefix='part04-atcoder06-')as temporary:
 for record in evidence:
  ref=record['ref'];row=next(r for r in rows if r['ref']==ref);codes=[b['text']for s in row['editorial']['sections']for b in s['blocks']if b['type']=='code'];assert len(codes)==1
  code=codes[0];source=Path(temporary)/(ref+'.cpp');binary=Path(temporary)/ref;source.write_text(code)
  built=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wshadow','-pedantic',str(source),'-o',str(binary)],capture_output=True,text=True,timeout=30);assert built.returncode==0 and not built.stderr,(ref,built.stderr)
  cases=[(s['input'],s['output'])for s in record['samples']]+extra.get(ref,[])
  for inp,expected in cases:
   ran=subprocess.run([str(binary)],input=inp,capture_output=True,text=True,timeout=4);assert ran.returncode==0 and not ran.stderr,(ref,ran.stderr);verify(ref,inp,expected,ran.stdout)
  results.append({'ref':ref,'code_sha256':hashlib.sha256(code.encode()).hexdigest(),'compiler_warnings':0,'official_samples':len(record['samples']),'focused_edge_cases':len(extra.get(ref,[])),'status':'passed','output_check':'independent-set witness predicate'if ref=='typical90_z'else'whitespace-normalized exact output'})
report={'status':'passed','programs':len(results),'official_samples':sum(r['official_samples']for r in results),'focused_edge_cases':sum(r['focused_edge_cases']for r in results),'results':results,'limits':'Local original implementations, no judge submissions; official samples and targeted edge cases are not exhaustive/random oracle coverage.'}
(ROOT/'audit/PART04-ATCODER-CONTENT06-CPP.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='results'}))
