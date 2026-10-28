"""Exact native lesson programs against ordinary sets and direct divisor enumeration."""
from pathlib import Path
import json,subprocess,tempfile,random,hashlib,math
ROOT=Path(__file__).resolve().parents[1];rng=random.Random(20261028);reports=[]
with tempfile.TemporaryDirectory()as tmp:
 for id in ['bit-operations','gcd']:
  body=json.loads((ROOT/f'audit/package02-lessons/{id}.json').read_text())['body'];blocks=body['sections'][7]['blocks'];source=(ROOT/f'audit/package02-work/{id}.cpp').read_text();pieces=[b['text']for b in blocks if b.get('language')=='C++17'];assert len(pieces)==5 and ''.join(pieces[:4])==pieces[-1]==source;assert pieces==[b['text']for b in body['translations']['en']['sections'][7]['blocks']if b.get('language')=='C++17']
  exe=Path(tmp)/id;build=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(ROOT/f'audit/package02-work/{id}.cpp'),'-o',str(exe)],capture_output=True,text=True,check=True);assert not build.stderr,build.stderr
  def run(text):return subprocess.run([str(exe)],input=text,capture_output=True,text=True,timeout=15,check=True).stdout.split()
  if id=='bit-operations':
   cases=[]
   for width in range(9):
    commands=[]
    for number in range(2**width):
     commands +=[f'CLEAR {i}'for i in range(width)]
     # Binary text supplies selected positions; expected results use an ordinary set.
     commands +=[f'SET {i}'for i,d in enumerate(reversed(format(number,'b')))if d=='1']
     commands +=['COUNT']+[f'HAS {i}'for i in range(width)]+[f'TOGGLE {i}'for i in range(width)]+['COUNT','FLIP','COUNT']
    cases.append((width,commands))
   for width in [0,1,2,7,30,60]:
    for _ in range(12):
     commands=[rng.choice(['COUNT','FLIP']+[f'{op} {rng.randrange(width)}'for op in['SET','CLEAR','TOGGLE','HAS']]if width else['COUNT','FLIP'])for _ in range(500)]
     cases.append((width,commands))
   cases +=[(60,[f'SET {i}'for i in range(60)]+['COUNT']*199940),(60,['SET 59','HAS 59','FLIP','HAS 59','CLEAR 0','COUNT']),(0,[])]
   operations=0
   for width,commands in cases:
    members=set();expected=[]
    for c in commands:
     op,*arg=c.split()
     if op=='COUNT':expected.append(str(len(members)))
     elif op=='FLIP':members=set(range(width))-members
     else:
      i=int(arg[0])
      if op=='SET':members.add(i)
      elif op=='CLEAR':members.discard(i)
      elif op=='TOGGLE':
       if i in members:members.remove(i)
       else:members.add(i)
      else:expected.append(str(int(i in members)))
    assert run(f'{width} {len(commands)}\n'+'\n'.join(commands)+'\n')==expected;operations+=len(commands)
   grey=[''];states=0
   for width in range(1,17):
    grey=['0'+s for s in grey]+['1'+s for s in reversed(grey)]
    assert len(grey)==len(set(grey))==2**width
    assert all(sum(a!=b for a,b in zip(x,y))==1 for x,y in zip(grey,grey[1:]));states+=len(grey)
   extra={'cases':len(cases),'commands':operations,'reflected_gray_states_checked':states};oracle='Ordinary Python set transitions, every small mask through width 8, widths0/60 and200000commands; reflected Gray coverage/uniqueness/adjacency through16bits'
  else:
   pairs=[(a,b)for a in range(101)for b in range(101)]
   def direct(a,b):return max([d for d in range(1,max(a,b)+1)if a%d==0 and b%d==0],default=0)
   expected=[]
   for a,b in pairs:
    g=direct(a,b);expected +=[str(g),str(0 if not a or not b else a*b//g)]
   assert run(str(len(pairs))+'\n'+''.join(f'{a} {b}\n'for a,b in pairs))==expected
   small=len(pairs)
   fibonacci=[0,1]
   while fibonacci[-1]+fibonacci[-2]<=10**9:fibonacci.append(sum(fibonacci[-2:]))
   pairs=[(a,b)for a,b in zip(fibonacci,fibonacci[1:])]+[(10**9,10**9-1),(10**9,0),(0,10**9),(0,0),(1,10**9)]+[(rng.randrange(10**9+1),rng.randrange(10**9+1))for _ in range(199947)]
   pairs=pairs[:200000]
   pairs +=[(rng.randrange(10**9+1),rng.randrange(10**9+1))for _ in range(200000-len(pairs))]
   expected=[]
   for a,b in pairs:
    g=math.gcd(a,b);expected +=[str(g),str(0 if not a or not b else a*b//g)]
   assert run(str(len(pairs))+'\n'+''.join(f'{a} {b}\n'for a,b in pairs))==expected
   assert run('0\n')==[]
   # The extended positive-input overflow test in the prose is checked before product formation.
   limits=[(10**18,3,10**18),(10**18,1,10**18),(10**18-1,10**18,10**18)]+[(rng.randrange(1,10**18+1),rng.randrange(1,10**18+1),10**18)for _ in range(500)]
   for a,b,limit in limits:assert (a//math.gcd(a,b)>limit//b)==(math.lcm(a,b)>limit)
   extra={'direct_divisor_pairs':small,'large_boundary_pairs':len(pairs),'overflow_guard_comparisons':len(limits),'zero_query_case':True};oracle='Independent exhaustive direct divisor enumeration for all0..100pairs; arbitrary-precision reference for200000bounded pairs including consecutive Fibonacci/extreme/zero values; positive large-LCM limit predicate compared with full arbitrary-precision product'
  sample_in=next(b['text']for b in blocks if b.get('language')=='Input');sample_out=next(b['text']for b in blocks if b.get('language')=='Output');assert run(sample_in)==sample_out.split();reports.append({'lesson':id,**extra,'sample_passed':True,'compile_warnings':0,'undefined_behavior_sanitizer':'passed on all valid-contract executions','program_sha256':hashlib.sha256(source.encode()).hexdigest(),'oracle':oracle})
report={'status':'passed','programs':reports,'scope':'Local complete C++17 programs and exact MN/EN fragments, explicit extension checks; semantic/native editor/publication gates separate'};(ROOT/'audit/PACKAGE02-BITS-GCD-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
