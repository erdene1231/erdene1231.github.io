import itertools,random,subprocess,tempfile,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];src=(R/'audit/package03-work/suffix-array.cpp').read_text();d=Path(tempfile.mkdtemp(prefix='suffix-code-'));exe=d/'test';subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/'audit/package03-work/suffix-array.cpp'),'-o',str(exe)],check=True)
def run(s):
 out=subprocess.check_output([str(exe)],input=s+'\n',text=True).splitlines();return [tuple(map(int,x.split()))for x in out[:-1]],int(out[-1])
def oracle(s):
 sa=sorted(range(len(s)),key=lambda i:s[i:]);lcp=[0]*len(s)
 for r in range(1,len(s)):
  i,j=sa[r-1],sa[r]
  while i+lcp[r]<len(s)and j+lcp[r]<len(s)and s[i+lcp[r]]==s[j+lcp[r]]:lcp[r]+=1
 return list(zip(sa,lcp)),len({s[i:j]for i in range(len(s))for j in range(i+1,len(s)+1)})
cases=[''.join(x)for n in range(9)for x in itertools.product('ab',repeat=n)];rng=random.Random(4401);cases+=[''.join(rng.choice('abcxyz $!')for _ in range(rng.randrange(65)))for _ in range(200)];cases+=['banana','mississippi','abababab','zyxwvutsrqponmlkjihgfedcba','a','']
for s in cases:assert run(s)==oracle(s),s
n=200000;rows,count=run('a'*n);assert rows==[(n-1-i,i)for i in range(n)]and count==n
s='ab'*(n//2);rows,count=run(s);assert [i for i,_ in rows]==list(range(n-2,-1,-2))+list(range(n-1,-1,-2));assert count==2*n-1
x={'status':'passed','source_sha256':hashlib.sha256(src.encode()).hexdigest(),'Cpp17_UBSan':True,'naive_suffix_lcp_and_distinct_cases':len(cases),'empty_singleton_all_equal_periodic_distinct':True,'space_dollar_punctuation_not_sentinel':True,'stress_length':n,'construction':'comparison-sort doubling O(n log² n), no stored sentinel','lcp':'Kasai O(n), lcp[0]=0, previous-suffix convention','memory':'O(n)','publication':False};(R/'audit/PACKAGE03-SUFFIX-CODE.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x))
