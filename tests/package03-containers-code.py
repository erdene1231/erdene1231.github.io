import json,subprocess,tempfile,random,collections
from pathlib import Path
R=Path(__file__).resolve().parents[1]
h=r'''
#include <bits/stdc++.h>
using namespace std;
#define main bracketsMain
#include "BRACKETS"
#undef main
#define main jobsMain
#include "JOBS"
#undef main
#define main roomsMain
#include "ROOMS"
#undef main
int main(){
 long long strings=0,roomsCases=0,cmpChecks=0;
 string chars="()[]{}";
 for(int n=0;n<=6;n++){int all=1;for(int i=0;i<n;i++)all*=6;for(int mask=0;mask<all;mask++){
  string s;int v=mask;for(int i=0;i<n;i++){s+=chars[v%6];v/=6;}string t=s;
  bool changed=true;while(changed){changed=false;for(string p:vector<string>{"()","[]","{}"}){auto k=t.find(p);if(k!=string::npos){t.erase(k,2);changed=true;}}}
  assert(balanced(s)==t.empty());strings++;
 }}
 assert(balanced(string(100000,'(')+string(100000,')')));assert(!balanced(string(200000,'(')));
 vector<Job> jobs;for(ll p:{-2,-1,0,1,2})for(int id=1;id<=3;id++)jobs.push_back({p,id});Cmp cmp;
 for(Job a:jobs){assert(!cmp(a,a));for(Job b:jobs)for(Job c:jobs){assert(!(cmp(a,b)&&cmp(b,a)));if(cmp(a,b)&&cmp(b,c))assert(cmp(a,c));cmpChecks++;}}
 auto verify=[&](vector<Stay>a){
  auto [n,ans]=allocate(a);assert(ans.size()==a.size());vector<vector<pair<ll,ll>>> groups(n+1);vector<pair<ll,int>> events;
  for(Stay s:a){assert(ans[s.id]>=1&&ans[s.id]<=n);groups[ans[s.id]].push_back({s.l,s.r});events.push_back({s.l,0});events.push_back({s.r,1});}
  for(auto&g:groups){sort(g.begin(),g.end());for(int i=1;i<(int)g.size();i++)assert(g[i-1].second<g[i].first);}
  sort(events.begin(),events.end());int active=0,best=0;for(auto[t,type]:events){if(type==0)active++;else active--;best=max(best,active);}assert(n==best);roomsCases++;
 };
 vector<Stay> all;for(int l=0;l<=3;l++)for(int r=l;r<=3;r++)all.push_back({l,r,0});
 for(int mask=0;mask<(1<<(int)all.size());mask++){vector<Stay>a;for(int i=0;i<(int)all.size();i++)if(mask>>i&1){Stay s=all[i];s.id=a.size();a.push_back(s);}verify(a);}
 mt19937 rng(7253);for(int c=0;c<1000;c++){vector<Stay>a(rng()%18);for(int i=0;i<(int)a.size();i++){ll l=(int)(rng()%15)-7,r=(int)(rng()%15)-7;if(l>r)swap(l,r);a[i]={l,r,i};}verify(a);}
 verify({{LLONG_MIN,LLONG_MIN,0},{LLONG_MIN,0,1},{0,LLONG_MAX,2},{LLONG_MAX,LLONG_MAX,3}});
 auto sample=allocate({{1,2,0},{2,4,1},{3,3,2},{5,6,3}});assert(sample.first==2&&sample.second==vector<int>({1,2,1,1}));roomsCases++;
 vector<Stay>a(200000);for(int i=0;i<(int)a.size();i++)a[i]={2LL*i,2LL*i+1,i};verify(a);for(int i=0;i<(int)a.size();i++)a[i]={7,7,i};verify(a);
 cout<<strings<<' '<<roomsCases<<' '<<cmpChecks<<'\n';
}
'''
for token,file in [('BRACKETS','brackets'),('JOBS','jobs'),('ROOMS','rooms')]:h=h.replace(token,str(R/f'audit/package03-work/containers-{file}.cpp'))
rng=random.Random(44417);ops=0
with tempfile.TemporaryDirectory()as td:
 p=Path(td);(p/'h.cpp').write_text(h);subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(p/'h.cpp'),'-o',str(p/'h')],check=True,capture_output=True);strings,roomcases,cmpchecks=map(int,subprocess.check_output([str(p/'h')],text=True,timeout=50).split())
 for name in ['stack-queue','brackets','heaps','jobs','rooms']:subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',str(R/f'audit/package03-work/containers-{name}.cpp'),'-o',str(p/name)],check=True)
 def run(name,s):return subprocess.check_output([str(p/name)],input=s,text=True,timeout=15).strip().splitlines()
 for name in ['stack-queue','heaps']:
  for c in range(120):
   cmds=[];want=[];a=[];b=[]
   for i in range(120):
    cmd=rng.choice(['PUSH','PUSH','PEEK','POP','SIZE']);ops+=1
    if cmd=='PUSH':
     x=rng.choice([-(2**63),2**63-1,rng.randrange(-9,10)]);cmds.append('PUSH '+str(x));a.append(x);b.append(x)
    elif cmd=='SIZE':cmds.append(cmd);want.append(str(len(a)))
    elif not a:cmds.append(cmd);want.append('EMPTY')
    elif name=='stack-queue':
     cmds.append(cmd);want.append(f'{a[-1]} {b[0]}'+(f' {b[-1]}'if cmd=='PEEK'else''))
     if cmd=='POP':a.pop();b.pop(0)
    else:
     cmds.append(cmd);want.append(f'{max(a)} {min(b)}')
     if cmd=='POP':a.remove(max(a));b.remove(min(b))
   assert run(name,str(len(cmds))+'\n'+'\n'.join(cmds)+'\n')==want
 for c in range(200):
  a=[rng.choice([-(2**63),2**63-1,rng.randrange(-3,4)])for _ in range(rng.randrange(100))];want=[f'{i} {v}'for i,v in sorted(enumerate(a,1),key=lambda z:(-z[1],z[0]))];assert run('jobs',str(len(a))+'\n'+' '.join(map(str,a))+'\n')==want
 for s,w in [('',True),('([])',True),('([)]',False),('(',False),(')',False),('{}[]()',True)]:assert run('brackets',s+'\n')==['YES'if w else'NO']
 assert run('rooms','4\n1 2\n2 4\n3 3\n5 6\n')==['2','1 2 1 1']
report={'status':'passed','Cpp17_programs':5,'UBSan':True,'exhaustive_bracket_strings':strings,'command_traces':240,'command_model_operations':ops,'custom_priority_sequences':200,'comparator_relation_checks':cmpchecks,'room_cases':roomcases,'all_interval_subsets_0_to_3':1024,'random_room_cases':1000,'max_input':200000,'ll_min_max_values_and_dates':True,'empty_duplicate_tie_and_endpoint_cases':True,'room_source_assignments':[1,2,1,1],'no_ll_negation_or_end_plus_one':True}
(R/'audit/PACKAGE03-CONTAINERS-CODE.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
