import json,hashlib,tempfile,subprocess,random,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];src=R/'audit/package03-work/suffix-repeat.cpp';base=(R/'audit/package03-work/suffix-array.cpp').read_text();assert src.read_text().split('int main()')[0]==base.split('int main()')[0];work=Path(tempfile.mkdtemp(prefix='suffix-repeat-'));exe=work/'repeat';subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(src),'-o',str(exe)],check=True)
rng=random.Random(999);cases=[''.join(x)for n in range(8)for x in itertools.product('ab',repeat=n)]+[''.join(rng.choice('abc $')for _ in range(rng.randrange(65)))for _ in range(160)]+['banana','mississippi','aaaa','abc','']
for s in cases:
 out=subprocess.check_output([str(exe)],input=s+'\n',text=True).removesuffix('\n');best=0
 for i in range(len(s)):
  for j in range(i+1,len(s)):
   h=0
   while j+h<len(s)and s[i+h]==s[j+h]:h+=1
   best=max(best,h)
 if not best:assert out=='-1',s
 else:assert len(out)==best and sum(s.startswith(out,i)for i in range(len(s)))>=2,(s,out,best)
out=subprocess.check_output([str(exe)],input='a'*200000+'\n',text=True);assert out=='a'*199999+'\n'
r={'status':'passed','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'core_constructor_identical_to_previously_verified':True,'Cpp17_UBSan_warning_error':True,'naive_longest_repeat_cases':len(cases),'overlap_allowed_and_ties_validated':True,'stress_length':200000};(R/'audit/PACKAGE03-SUFFIX-REPEAT-CODE.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
# Independent suffix-automaton oracle for a genuinely 64-bit distinct count.
s=''.join(rng.choice('abcdefghijklmnopqrstuvwxyz')for _ in range(100000));go=[{}];link=[-1];length=[0];last=0
for ch in s:
 cur=len(go);go.append({});length.append(length[last]+1);link.append(0);p=last
 while p>=0 and ch not in go[p]:go[p][ch]=cur;p=link[p]
 if p>=0:
  q=go[p][ch]
  if length[p]+1==length[q]:link[cur]=q
  else:
   clone=len(go);go.append(go[q].copy());length.append(length[p]+1);link.append(link[q])
   while p>=0 and go[p].get(ch)==q:go[p][ch]=clone;p=link[p]
   link[q]=link[cur]=clone
 last=cur
expected=sum(length[i]-length[link[i]]for i in range(1,len(go)));assert expected>2**31
full=work/'full';subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/'audit/package03-work/suffix-array.cpp'),'-o',str(full)],check=True);actual=int(subprocess.check_output([str(full)],input=s+'\n',text=True).splitlines()[-1]);assert actual==expected
r.update(independent_suffix_automaton_distinct_oracle=True,large_distinct_count=actual,large_distinct_length=len(s));(R/'audit/PACKAGE03-SUFFIX-REPEAT-CODE.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'large_distinct_count':actual,'independent_oracle':True}))
