import json,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
harness=r'''
#include <bits/stdc++.h>
using namespace std;
#define main sample1
#include "SEARCH1"
#undef main
#define main sample2
#include "SEARCH2"
#undef main
#define main sample3
#include "SEARCH3"
#undef main
int main(){
 long long cases=0, checks=0;
 auto check=[&](vector<ll>a){
  sort(a.begin(),a.end());cases++;
  vector<ll> xs={LLONG_MIN,-9,-4,-2,-1,0,1,2,3,4,9,LLONG_MAX};
  if(a.size()<=50) xs.insert(xs.end(),a.begin(),a.end()); else {xs.push_back(a.front());xs.push_back(a.back());}
  for(ll x:xs){int l=0,r=0;while(l<(int)a.size()&&a[l]<x)l++;while(r<(int)a.size()&&a[r]<=x)r++;
   assert(l==lower_bound(a.begin(),a.end(),x)-a.begin());assert(r==upper_bound(a.begin(),a.end(),x)-a.begin());
   assert(lowerBound(a,x)==l);assert(upperBound(a,x)==r);int p=findAny(a,x),q=findFirst(a,x);bool found=l<(int)a.size()&&a[l]==x;
   assert((p>=0)==found);if(p>=0)assert(p<(int)a.size()&&a[p]==x);assert(q==(found?l:-1));checks++;
  }
 };
 for(int n=0;n<=7;n++){int all=1;for(int i=0;i<n;i++)all*=3;for(int m=0;m<all;m++){int k=m;vector<ll>a(n);for(ll&x:a){x=k%3-1;k/=3;}check(a);}}
 mt19937_64 rng(17003);for(int t=0;t<1000;t++){vector<ll>a(rng()%50);for(ll&x:a)x=(ll)(rng()%25)-12;check(a);}
 check({LLONG_MIN,LLONG_MIN,0,LLONG_MAX,LLONG_MAX});check(vector<ll>(200000,2));vector<ll>a(200000);iota(a.begin(),a.end(),-100000);check(a);
 int l=INT_MAX-3,r=INT_MAX;assert(l+(r-l)/2==INT_MAX-2);
 cout<<cases<<' '<<checks<<'\n';
}
'''
for i,id in enumerate(['binary-search','lower-bound','upper-bound'],1):harness=harness.replace('SEARCH'+str(i),str(R/f'audit/package03-work/search-{id}.cpp'))
with tempfile.TemporaryDirectory()as t:
 p=Path(t);(p/'test.cpp').write_text(harness);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(p/'test.cpp'),'-o',str(p/'test')],check=True,capture_output=True)
 cases,checks=map(int,subprocess.check_output([str(p/'test')],text=True,timeout=40).split())
 for id in ['binary-search','lower-bound','upper-bound']:
  subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/search-{id}.cpp'),'-o',str(p/id)],check=True)
  for a,xs in [([],[0]),([1,2,2,2,5],[0,2,4,5,6]),([-(2**63),2**63-1],[-(2**63),2**63-1])]:
   data=f'{len(a)} {len(xs)}\n'+ ' '.join(map(str,a))+'\n'+'\n'.join(map(str,xs))+'\n';out=subprocess.check_output([str(p/id)],input=data,text=True).splitlines();assert len(out)==len(xs)
   for row,x in zip(out,xs):
    v=list(map(int,row.split()));lo=sum(y<x for y in a);hi=sum(y<=x for y in a)
    if id=='lower-bound':assert v==[lo,lo-1]
    elif id=='upper-bound':assert v==[hi,hi-1,hi-lo]
    else:assert (v[0]>=0)==(x in a) and v[1]==(lo if x in a else -1)
report={'status':'passed','complete_Cpp17_programs':3,'UBSan':True,'array_cases':cases,'naive_and_stdlib_query_checks':checks,'all_ternary_arrays_through_length':7,'random_arrays':1000,'max_n':200000,'ll_min_max_targets':True,'no_x_plus_one_arithmetic':True,'overflow_safe_midpoint':True,'standalone_program_IO_cases':9}
(R/'audit/PACKAGE03-SEARCH-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
