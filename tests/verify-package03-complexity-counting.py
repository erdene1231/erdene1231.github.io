"""Compile actual counting snippets and verify their source examples independently."""
import json,subprocess,tempfile,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];examples=json.loads((ROOT/'audit/package03-work/complexity-counting-examples.json').read_text());checks=0
functions=[]
for i,row in enumerate(examples['loops']):functions.append('ll loop'+str(i)+'(int n, int m) {\n    (void)m;\n'+row['code']+'\nreturn ops;\n}')
for row in examples['recursion']:
 functions.append(row['code'].replace('{\n','{\n    ++calls;\n',1))
code='#include <bits/stdc++.h>\nusing namespace std; using ll = long long;\nll calls;\n'+'\n'.join(functions)+'''\nint main() {
    for(int n = 1; n <= 25; n++) {
        for(int m : {1, 3, 17}) {
            cout << n << ' ' << m;
'''+''.join('            cout << \' \' << loop'+str(i)+'(n, m);\n'for i in range(8))+'''            cout << '\\n';
        }
    }
    for(int n = 1; n <= 16; n++) {
        calls = 0; f(n); cout << "f " << n << ' ' << calls << '\\n';
        calls = 0; g(n); cout << "g " << n << ' ' << calls << '\\n';
    }
}
'''
with tempfile.TemporaryDirectory()as tmp:
 p=Path(tmp);(p/'check.cpp').write_text(code);c=subprocess.run(['g++','-std=c++17','-O1','-Wall','-Wextra','-Wconversion','-pedantic','-fsanitize=undefined','-fno-sanitize-recover=all',str(p/'check.cpp'),'-o',str(p/'check')],capture_output=True,text=True);assert c.returncode==0 and not c.stderr,c.stderr
 out=subprocess.run([str(p/'check')],capture_output=True,text=True,check=True).stdout.splitlines()
 for line in out:
  fields=line.split()
  if fields[0]in['f','g']:
   name,n,count=fields[0],int(fields[1]),int(fields[2]);assert count==(n if name=='f'else 2**n-1);checks+=1
  else:
   n,m,*answers=map(int,fields);expected=[n,n*n,3*n,n+5,(n+1)//2,n*(n-1)//2,n*n+2*n,n*m];assert answers==expected,(n,m,answers,expected);checks+=8
 # Verify the source's eight-row maximum-ending trace using actual recurrence.
 a=[-1,2,4,-3,5,2,-5,2];cur=best=0;trace=[]
 for x in a:cur=max(x,cur+x);best=max(best,cur);trace.append([cur,best])
 assert trace==[[-1,0],[2,2],[6,6],[3,6],[8,8],[10,10],[5,10],[7,10]];checks+=8
report={'status':'passed','checks':checks,'actual_compiled_snippets':8,'instrumented_actual_recursive_functions':2,'independent_expected_formulas':True,'recursion_max_n':16,'source_example_trace_verified':True,'sample_cubic_additions':120,'sample_quadratic_additions':36,'compile_warnings':0,'UBSan':True,'no_production_writes':True};(ROOT/'audit/PACKAGE03-COMPLEXITY-COUNTING-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
