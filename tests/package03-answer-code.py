import json,tempfile,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
h=r'''
#include <bits/stdc++.h>
using namespace std;
#define main machineMain
#include "MACHINES"
#undef main
#define main ropeMain
#include "ROPES"
#undef main
int main(){
 long long arrays=0, answers=0, predicates=0;
 auto check=[&](vector<ll>a){
  arrays++;
  for(ll k=0;k<=9;k++)for(ll cap=0;cap<=15;cap++){
   ll want=-1;bool seen=false;for(ll t=0;t<=cap;t++){
    ll sum=0;for(ll v:a)sum+=t/v;bool ok=sum>=k;
    assert(machineOk(a,k,t)==ok);assert(!seen||ok);seen|=ok;
    if(ok&&want<0)want=t;predicates++;
   }
   assert(firstTime(a,k,cap)==want);answers++;
  }
 };
 for(int n=0;n<=5;n++){int all=1;for(int i=0;i<n;i++)all*=3;for(int mask=0;mask<all;mask++){int v=mask;vector<ll>a(n);for(ll&x:a){x=v%3+1;v/=3;}check(a);}}
 mt19937 rng(11823);for(int i=0;i<300;i++){vector<ll>a(rng()%8);for(ll&x:a)x=rng()%8+1;check(a);}
 for(int n=0;n<=4;n++){int all=1;for(int i=0;i<n;i++)all*=5;for(int mask=0;mask<all;mask++){
  vector<ll>a(n);int v=mask;for(ll&x:a){x=v%5;v/=5;}arrays++;
  for(ll k=1;k<=10;k++){ll want=0;bool failed=false;for(ll x=1;x<=5;x++){
   ll sum=0;for(ll z:a)sum+=z/x;bool ok=sum>=k;assert(ropeOk(a,k,x)==ok);assert(!failed||!ok);failed|=!ok;if(ok)want=x;predicates++;
  }assert(lastLength(a,k)==want);answers++;}
 }}
 ll L=LLONG_MAX;
 for(vector<ll>a:vector<vector<ll>>{{},{1},{L},{1,1},{L,L},{1,L},{L,1,L}}){
  for(ll k:vector<ll>{0,1,2,17,L}){
   for(ll t:vector<ll>{0,1,2,L/2,L-1,L}){__int128 sum=0;for(ll x:a)sum+=(__int128)t/x;assert(machineOk(a,k,t)==(sum>=k));predicates++;}
   for(ll cap:vector<ll>{0,1,10,L}){
    ll x=firstTime(a,k,cap);if(x<0){__int128 sum=0;for(ll z:a)sum+=(__int128)cap/z;assert(sum<k);}else{__int128 here=0,before=0;for(ll z:a){here+=(__int128)x/z;if(x)before+=(__int128)(x-1)/z;}assert(here>=k);assert(x==0||before<k);}answers++;
   }
  }
  for(ll k:vector<ll>{1,2,17,L}){ll x=lastLength(a,k),maxv=a.empty()?0:*max_element(a.begin(),a.end());assert(x>=0&&x<=maxv);__int128 here=0,after=0;for(ll z:a){if(x)here+=(__int128)z/x;if(x<maxv)after+=(__int128)z/(x+1);}assert(x==0||here>=k);assert(x==maxv||after<k);answers++;}
 }
 vector<ll>a(200000,1);ll need=L/200000+(L%200000!=0);assert(firstTime(a,L,L)==need);fill(a.begin(),a.end(),L);assert(lastLength(a,L)==L/need);assert(firstTime({L},2,L)==-1);assert(firstTime({1},L,L)==L);assert(lastLength({L},1)==L);
 cout<<arrays<<' '<<answers<<' '<<predicates<<'\n';
}
'''
h=h.replace('MACHINES',str(R/'audit/package03-work/answer-machines.cpp')).replace('ROPES',str(R/'audit/package03-work/answer-ropes.cpp'))
with tempfile.TemporaryDirectory()as td:
 p=Path(td);(p/'h.cpp').write_text(h);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(p/'h.cpp'),'-o',str(p/'h')],check=True,capture_output=True);arrays,answers,predicates=map(int,subprocess.check_output([str(p/'h')],text=True,timeout=40).split())
 for name,cases in {'machines':[('3 7 16\n3 2 5\n','8'),('3 7 7\n3 2 5\n','-1'),('0 0 0\n','0'),('0 1 8\n','-1'),('1 9223372036854775807 9223372036854775807\n1\n','9223372036854775807')],'ropes':[('3 5\n4 7 9\n','3'),('3 21\n4 7 9\n','0'),('0 1\n','0'),('1 1\n9223372036854775807\n','9223372036854775807')]}.items():
  subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/answer-{name}.cpp'),'-o',str(p/name)],check=True)
  for inp,want in cases:assert subprocess.check_output([str(p/name)],input=inp,text=True).strip()==want
report={'status':'passed','Cpp17_programs':2,'UBSan':True,'array_cases':arrays,'bruteforce_answer_checks':answers,'independent_predicate_checks':predicates,'machine_example':8,'rope_example':3,'random_machine_arrays':300,'max_n':200000,'ll_max_endpoints':True,'all_no_feasible_and_single_endpoint':True,'test_only_128bit_oracle':True,'standalone_IO_cases':9}
(R/'audit/PACKAGE03-ANSWER-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
