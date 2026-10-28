"""Exact native lesson programs against direct products and divisor-incidence counting."""
from pathlib import Path
import json,subprocess,tempfile,random,hashlib
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['fast-power','sieve']:
  body=json.loads((ROOT/f'audit/package02-lessons/{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];source=(ROOT/f'audit/package02-work/{id}.cpp').read_text();pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]==source;assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
  exe=Path(tmp)/id;build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(ROOT/f'audit/package02-work/{id}.cpp'),'-o',str(exe)],capture_output=True,text=True,check=True);assert not build.stderr,build.stderr
  def run(text):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=20,check=True).stdout.split()
  if id=='fast-power':
   cases=[(a,e,m)for a in range(19)for e in range(17)for m in range(1,21)];expected=[]
   for a,e,m in cases:
    value=1
    for _ in range(e):value*=a
    expected.append(str(value%m))
   assert run(str(len(cases))+'\n'+''.join(f'{a} {e} {m}\n'for a,e,m in cases))==expected
   small=len(cases);cases=[(0,0,1),(0,0,7),(0,10**18,10**9+7),(10**18,0,10**9+7),(10**18,10**18,1),(10**9+6,10**18,10**9+7),(10**9+7,10**18,10**9+7),(3,13,17)]
   cases +=[(rng.randrange(10**18+1),rng.randrange(10**18+1),rng.randrange(1,10**9+8))for _ in range(200000-len(cases))]
   assert run(str(len(cases))+'\n'+''.join(f'{a} {e} {m}\n'for a,e,m in cases))==[str(pow(a,e,m))for a,e,m in cases];assert run('0\n')==[]
   trace=[(1,3,13),(3,9,6),(3,13,3),(5,16,1),(12,1,0)];assert all(answer*pow(base,exponent,17)%17==pow(3,13,17)for answer,base,exponent in trace)
   extra={'small_direct_product_queries':small,'large_boundary_queries':len(cases),'trace_rows_checked':len(trace),'zero_query_case':True};oracle='Independent direct full products for small exponents; Python exact modular power for200000bounded large queries including zero exponent/modulus1/maxresidue; every published trace row preserves the product'
  else:
   count=0
   for limit in [1,2,3,4,9,20,49,97,1500]:
    expected=[]
    for value in range(1,limit+1):
     divisors=sum(value%d==0 for d in range(1,value+1));expected +=[str(int(divisors==2)),str(divisors)]
    assert run(f'{limit} {limit}\n'+'\n'.join(map(str,range(1,limit+1)))+'\n')==expected;count+=limit
   limit=10**6;divisors=[0]*(limit+1)
   # Independent oracle: every divisor contributes once to every multiple, with no prime/SPF logic.
   for divisor in range(1,limit+1):
    for multiple in range(divisor,limit+1,divisor):divisors[multiple]+=1
   for start in range(1,limit+1,200000):
    values=range(start,min(start+200000,limit+1));expected=[token for v in values for token in(str(int(divisors[v]==2)),str(divisors[v]))];assert run(f'{limit} {len(values)}\n'+'\n'.join(map(str,values))+'\n')==expected;count+=len(values)
   assert run('1 0\n')==[]
   helper=Path(tmp)/'spf-check.cpp';helper.write_text('#define main lesson_main\n'+source+'\n#undef main\nint main(){for(int n=0;n<=100;++n){auto s=build_smallest_factor(n);if(s.size()!=static_cast<size_t>(n+1))return 1;for(int x=2;x<=n;++x){int d=2;while(x%d!=0)++d;if(s[x]!=d)return 2;}}return 0;}');h=Path(tmp)/'spf-check';subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(helper),'-o',str(h)],check=True);subprocess.run([str(h)],check=True)
   extra={'query_values_checked':count,'maximum_table_limit':limit,'maximum_query_batch':200000,'smallest_factor_helper_limits':101,'zero_query_case':True};oracle='Direct divisor enumeration on small ranges; all1millionvalues independently verified by divisor-incidence counting rather than prime/SPF logic in five200000querybatches; smallest factors independently checked by ascending trial divisors'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split();reports.append({'lesson':id,**extra,'sample_passed':True,'compile_warnings':0,'undefined_behavior_sanitizer':'passed for all valid-contract executions','program_sha256':hashlib.sha256(source.encode()).hexdigest(),'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Local exact C++17 programs/fragments and explicit trace/helper checks; semantic/native editor/publication gates separate'};(ROOT/'audit/PACKAGE02-POWER-SIEVE-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
