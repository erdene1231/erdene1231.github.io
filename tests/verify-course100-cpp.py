"""Linux GCC and Bash checks only: never a Windows/IOI-VM test claim."""
import json,pathlib,tempfile,subprocess
R=pathlib.Path(__file__).resolve().parents[1];docs=json.loads((R/'audit/course100-v2/setup-tutorials.json').read_text())+[d['document']for d in json.loads((R/'study-plan.json').read_text())['days']];codes=set(b['text']for d in docs for s in d['sections']for b in s['blocks']if b['type']=='code'and b.get('language')=='C++17'and'#include'in b['text'])
checks=[]
with tempfile.TemporaryDirectory(prefix='course-cpp-')as tmp:
 root=pathlib.Path(tmp)/'CP Practice';root.mkdir();assert subprocess.run(['bash','-c','cd \"$1\" && pwd','--',str(root)],check=True,capture_output=True,text=True).stdout.strip()==str(root)
 for i,code in enumerate(sorted(codes)):
  src=root/'main.cpp';src.write_text(code)
  for standard in ['c++17','c++20']:
   subprocess.run(['g++','-std='+standard,'-O2','-Wall','-Wextra',str(src),'-o',str(root/'a')],check=True,capture_output=True)
   if'__cplusplus'in code:cases=[('',('201703'if standard=='c++17'else'202002')+'\n')]
   elif'cin >> a >> b'in code:cases=[('2 3\n','5\n'),('0 0\n','0\n'),('-1000 999\n','-1\n')]
   elif'vector<int>'in code:cases=[('3\n1000000000 -2 5\n','1000000003\n'),('3\n1000000000 1000000000 1000000000\n','3000000000\n'),('0\n','0\n')]
   elif'string s'in code:cases=[('AAABBBAA\n','5\n'),('A\n','0\n'),('ABCD\n','0\n')]
   else:cases=[('3\n','3\n2\n1\n'),('0\n','')]
   for data,expected in cases:
    (root/'a.in').write_text(data)
    r=subprocess.run(['bash','-c','./a < a.in > a.out 2> a.err'],cwd=root,capture_output=True,text=True,check=True);assert(root/'a.out').read_text()==expected;assert(root/'a.err').read_text()=='';checks.append({'program':i,'standard':standard,'redirected_output_exact':True})
  # A failed compile must not execute a stale program in the documented && chain.
 (root/'broken.cpp').write_text('this is not C++');(root/'a.out').write_text('sentinel\n');r=subprocess.run(['bash','-c','g++ -std=c++17 broken.cpp -o a && ./a < a.in > a.out'],cwd=root,capture_output=True);assert r.returncode!=0;assert(root/'a.out').read_text()=='sentinel\n'
report={'status':'passed','unique_complete_programs':len(codes),'compile_run_cases':len(checks),'standards':['c++17','c++20'],'bash_file_redirection':True,'quoted_space_path':True,'failed_compile_does_not_run_stale_binary':True,'limits':'Linux GCC/Bash only; CMD, PowerShell, MSYS2 GUI, Dev-C++ GUI and IOI VM not executed.'};(R/'audit/course100-v2/cpp-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
