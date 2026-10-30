import subprocess,tempfile,selectors,json,hashlib,random,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];w=Path(tempfile.mkdtemp(prefix='interactive-code-'));names=['interactive-search','communication-encode','communication-decode'];hashes={}
for name in names:
 p=R/f'audit/package03-work/{name}.cpp';hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest();subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wconversion','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(p),'-o',str(w/name)],check=True)
def line(p):
 with selectors.DefaultSelector()as sel:
  sel.register(p.stdout,selectors.EVENT_READ)
  assert sel.select(3),'No flushed query/final line before timeout'
 return p.stdout.readline().decode().strip()
def judge(n,x,fail=None,terminal='OK'):
 p=subprocess.Popen([str(w/'interactive-search')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,bufsize=0);p.stdin.write((str(n)+'\n').encode());queries=0;found=False;error=False
 try:
  while True:
   s=line(p);assert s,s
   fields=s.split();assert len(fields)==2 and fields[0]in['?','!'],s;y=int(fields[1]);assert 1<=y<=n
   if fields[0]=='!':
    assert y==x and not error;found=True
    if terminal is None:p.stdin.close()
    else:p.stdin.write((terminal+'\n').encode());p.stdin.close()
    break
   queries+=1;assert queries<=n.bit_length()
   if fail is not None:
    if fail=='EOF':p.stdin.close()
    else:p.stdin.write((fail+'\n').encode());p.stdin.close()
    error=True;break
   p.stdin.write(('='if x==y else'<'if x<y else'>').encode()+b'\n')
  rc=p.wait(timeout=3);rest=p.stdout.read();assert rest==b'',rest;assert p.stderr.read()==b''
  expected=0 if found and terminal=='OK'else 1;assert rc==expected,(n,x,fail,terminal,rc);return queries
 finally:
  if p.poll()is None:p.kill();p.wait()
cases=[(n,x)for n in range(1,41)for x in range(1,n+1)];rng=random.Random(721);cases += [(1000000000,x)for x in [1,2,500000000,999999999,1000000000]]+[(rng.randrange(1,1000000001),None)for _ in range(120)];cases=[(n,rng.randrange(1,n+1)if x is None else x)for n,x in cases];worst=max(judge(n,x)for n,x in cases)
for s in ['-1','INVALID','yes','EOF']:judge(10,3,fail=s)
# Contradiction at a singleton, invalid terminal and terminal EOF.
judge(1,1,fail='<');judge(1,1,fail='>');judge(1,1,terminal='-1');judge(1,1,terminal='WRONG');judge(1,1,terminal=None)
for s in ['0','-1','1000000001','bad','']:
 p=subprocess.run([str(w/'interactive-search')],input=s+'\n',text=True,capture_output=True,timeout=3);assert p.returncode==1 and not p.stdout
enc=(R/'audit/package03-work/communication-encode.cpp').read_text().split('int main()')[0];dec=(R/'audit/package03-work/communication-decode.cpp').read_text().split('int main()')[0];h=enc+dec+'''int main() {
    for (int x = 0; x < 4096; x++) {
        string s = encode(x);
        if (s.size() != 13 || decode(s) != x) return 1;
        for (int i = 0; i < 13; i++) {
            string t = s; t[i] = t[i] == '0' ? '1' : '0';
            if (decode(t)) return 2;
        }
    }
    if (decode("") || decode("000") || decode("00000000000000") || decode("000000000000x")) return 3;
    if (decode("1100000000000") != 3) return 4;
}
''';(w/'h.cpp').write_text(h);subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined','-fno-sanitize-recover=all',str(w/'h.cpp'),'-o',str(w/'h')],check=True);subprocess.run([str(w/'h')],check=True)
for x in [0,1,2,13,2048,4095]:
 s=subprocess.check_output([str(w/'communication-encode')],input=str(x)+'\n',text=True).strip();assert len(s)==13 and int(s[:12][::-1],2)==x and s.count('1')%2==0;y=subprocess.check_output([str(w/'communication-decode')],input=s+'\n',text=True).strip();assert int(y)==x
for s in ['-1','4096','bad','']:
 assert subprocess.check_output([str(w/'communication-encode')],input=s+'\n',text=True).strip()=='INVALID'
for s in ['','1','0000000000001','000000000000x']:
 assert subprocess.check_output([str(w/'communication-decode')],input=s+'\n',text=True).strip()=='INVALID'
r={'status':'passed','Cpp17_UBSan_warning_error_programs':3,'compiled_source_sha256':hashes,'pipe_mock_judge_sessions':len(cases),'max_queries_observed':worst,'proven_bound':'floor(log2 n)+1=ceil(log2(n+1)); <=30 for n<=1e9','exhaustive_all_secrets_n_through':40,'flushing_required_by_three_second_pipe_deadline':True,'error_eof_invalid_contradictory_and_terminal_responses_stop_without_further_stdout':True,'codec_all_values':4096,'all_single_bit_corruptions_detected':4096*13,'invalid_length_alphabet_and_numeric_domain_rejected':True,'separate_process_roundtrips':6,'two_bit_undetected_counterexample_verified':True,'production_writes':0};(R/'audit/PACKAGE03-INTERACTIVE-CODE.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
