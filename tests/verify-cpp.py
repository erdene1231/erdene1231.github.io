from pathlib import Path
import json,subprocess,concurrent.futures
R=Path(__file__).resolve().parents[1];out=R/'tests/.build';out.mkdir(parents=True,exist_ok=True)
topics=json.loads((R/'tutorials.json').read_text())['tutorials']
def check(t):
 blocks=[b for s in t['sections'] for b in s['blocks']];programs=[b['text'] for b in blocks if b['type']=='code' and 'int main(' in b['text']];assert programs,t['id'];program=programs[-1]
 en=[b['text'] for s in t['translations']['en']['sections'] for b in s['blocks'] if b['type']=='code' and 'int main(' in b['text']];assert en and en[-1].strip()==program.strip(),('language code differs',t['id'])
 inputs=[b['text'] for b in blocks if b['type']=='code' and b.get('language')=='Input'];outputs=[b['text'] for b in blocks if b['type']=='code' and b.get('language')=='Output'];assert outputs and (inputs or t['id']=='debugging'),t['id']
 cpp=out/(t['id']+'.cpp');cpp.write_text(program);exe=out/t['id'];r=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(cpp),'-o',str(exe)],capture_output=True,text=True);assert r.returncode==0 and 'multi-character' not in r.stderr,(t['id'],r.stderr)
 r=subprocess.run([exe],input=inputs[0] if inputs else '',capture_output=True,text=True,timeout=8);assert r.returncode==0 and r.stdout.split()==outputs[0].split(),(t['id'],r.stdout,outputs[0],r.stderr)
 return t['id']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:result=list(pool.map(check,topics))
print(json.dumps({'tutorials':len(topics),'full_cpp17_samples_passed':len(result),'both_language_programs_match':True}))
def run(tid,data,expected,timeout=5):
 r=subprocess.run([str(out/tid)],input=data,capture_output=True,text=True,timeout=timeout);assert r.returncode==0 and r.stdout.split()==expected.split(),(tid,data[:100],r.stdout,expected)
run('lower-bound','0 3\n-5\n0\n8\n','0\n0\n0\n')
run('upper-bound','3 3\n4 4 4\n3\n4\n5\n','0\n3\n3\n')
run('sliding-window','1 5\n10\n','0\n');run('sliding-window','0 0\n','0\n')
run('connected-components','4 0\n','4\n1 2 3 4\n')
run('bipartite','5 4\n1 2\n3 4\n4 5\n5 3\n','IMPOSSIBLE\n')
run('interval-dp','1\n1000000000\n','0\n');run('tree-dp','1\n','2\n')
n=200000;a,b=1,2
for i in range(2,n+1):a,b=b,(a+b)%1000000007
run('tree-dp',str(n)+'\n'+''.join(f'{i} {i+1}\n' for i in range(1,n)),str(b)+'\n',10)
run('bellman-ford','2 2\n1 2 -1\n2 1 -1\n','NEGATIVE CYCLE\n')
run('bellman-ford','3 2\n2 3 -1\n3 2 -1\n','0 INF INF\n')
run('bellman-ford','3 2\n2 3 -10\n1 2 2\n','0 2 -8\n')
run('string-hashing','a 1\n1 1 1 1\n','YES\n')
run('invariant','1 10\n5\n','-1 -1\n')
run('subtask-strategy','0 10\n','0\n')
import random
rng=random.Random(42)
for test in range(30):
 n=rng.randrange(0,15);limit=rng.randrange(0,301);values=[rng.randrange(0,51) for _ in range(n)];sums=[0]
 for x in values:sums += [s+x for s in sums]
 expected=max(s for s in sums if s<=limit)
 run('subtask-strategy',f'{n} {limit}\n'+ ' '.join(map(str,values))+'\n',str(expected)+'\n')
print(json.dumps({'extra_boundaries_and_negative_cycles':'PASS','tree_path_200000':'PASS','meet_in_the_middle_vs_exhaustive':30}))
