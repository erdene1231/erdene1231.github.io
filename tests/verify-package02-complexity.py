"""Independent pair enumeration / bit-length oracle for the complexity lesson; local only."""
import hashlib,itertools,json,math,random,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
doc=json.loads((ROOT/'audit/package02-lessons/complexity.json').read_text())['body']
blocks=doc['sections'][7]['blocks'];programs=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(programs)==5 and ''.join(programs[:-1])==programs[-1]
assert programs==[b['text']for b in doc['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
code=programs[-1];rng=random.Random(20261028)
values=sorted(set(list(range(101))+[2**k+d for k in range(1,30)for d in [-1,0,1]]+[10**9]+[rng.randrange(10**9+1)for _ in range(40)]))
with tempfile.TemporaryDirectory()as tmp:
 source=Path(tmp)/'complexity.cpp';exe=Path(tmp)/'complexity';source.write_text(code)
 result=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',str(source),'-o',str(exe)],capture_output=True,text=True,check=True);assert not result.stderr,result.stderr
 def run(value):return subprocess.run([str(exe)],input=str(value),capture_output=True,text=True,check=True,timeout=3).stdout.split()
 for n in values:
  pairs=sum(1 for _ in itertools.combinations(range(n),2))if n<=100 else math.comb(n,2)
  assert run(n)==[str(pairs),str(max(0,n.bit_length()-1))],n
 sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split()
report={'status':'passed','lesson':'complexity','program_sha256':hashlib.sha256(code.encode()).hexdigest(),'cases':len(values),'small_oracle':'enumerate unordered pairs','large_oracle':'arbitrary-precision math.comb and bit_length, including maximum and powers-of-two boundaries','sample_passed':True,'compile_warnings':0,'scope':'Local reference-program correctness and contract only; not whole-lesson acceptance'}
(ROOT/'audit/PACKAGE02-COMPLEXITY-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
