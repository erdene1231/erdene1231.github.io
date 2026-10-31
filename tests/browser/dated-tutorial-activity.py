"""Actual tutorial/learning modules, synthetic own-user Auth/save transport only."""
import functools,http.server,json,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   u=r.request.url
   if not u.startswith(base):r.abort()
   elif '/app.js?'in u or'/navigation.js?'in u:r.fulfill(status=200,content_type='text/javascript',body='')
   elif '/config.js?'in u:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={learningActivityVersion:1};')
   else:r.continue_()
  page.route('**/*',route)
  setup='''async()=>{
   const{setupTutorials}=await import('/tutorials.js?v=activity-test');const{setupLearning}=await import('/learning.js?v=activity-test');
   const seed=(await(await fetch('/tutorials.json')).json()).tutorials[0];window.lessons=['standalone-fixture','legacy-fixture','section-fixture','retry-fixture','isolation-fixture'].map(id=>{const t=structuredClone(seed);t.id=id;t.title=id;t.related=[];t.prerequisiteIds=[];delete t.learningRelations;t.sections=[{title:'First',blocks:[{type:'p',text:'One $n$.'}]},{title:'Second',blocks:[{type:'p',text:'Two $n$.'}]}];t.translations={en:{title:id,sections:structuredClone(t.sections)}};return t;});
   window.actor={id:localStorage.getItem('fixture-actor')||'alice'};window.server=JSON.parse(localStorage.getItem('fixture-server')||'{}');window.writes=[];window.reads=[];window.failSave=false;window.holdSave=false;
   if(!server.alice)server.alice={'tutorial:legacy-fixture':{readSections:[0,1],checks:['purpose'],unknown:{keep:7}},'tutorial:standalone-fixture':{readSections:[],checks:['purpose'],unknown:{keep:8}}};
   const persist=()=>localStorage.setItem('fixture-server',JSON.stringify(server));persist();
   const client={rpc:async name=>({data:name==='get_tutorials'?lessons.map(body=>({body,revision:1})):false,error:null}),from:name=>({
    select:()=>({eq:async(_,uid)=>{reads.push(uid);return{data:Object.entries(server[uid]||{}).map(([key,value])=>({kind:key.split(':')[0],key:key.slice(key.indexOf(':')+1),value:structuredClone(value)})),error:null};}}),
    upsert:rows=>({select:async()=>{
     writes.push(structuredClone(rows));if(holdSave)await new Promise(resolve=>window.releaseSave=resolve);if(failSave)return{error:Error('offline')};
     for(const row of rows){const key=row.kind+':'+row.key,prior=server[row.user_id]?.[key]||{},next=structuredClone(row.value),event=next._activityEvent;for(const field of['viewedAt','viewedDays','completedAt','viewEventId','completionEventId']){delete next[field];if(field in prior)next[field]=prior[field];}delete next._activityEvent;
      if(event){const stamp=new Date().toISOString();const complete=Array.from({length:event.sectionCount||0},(_,i)=>i).every(i=>(prior.readSections||[]).includes(i));if(event.type==='completed'&&!complete&&!prior.completedAt){next.completedAt=stamp;next.completionEventId=event.id;}if(prior.viewEventId!==event.id&&prior.completionEventId!==event.id){next.viewedAt=stamp;next.viewEventId=event.id;next.viewedDays=[...new Set([...(prior.viewedDays||[]),new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Ulaanbaatar',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(stamp))])];}}
      (server[row.user_id]||={})[key]=next;
     }persist();return{data:rows.map(r=>({kind:r.kind,key:r.key,value:structuredClone(r.value)})),error:null};
    }})})};window.client=client;let learning;
   window.tutorials=setupTutorials({requiresOnline:true,problems:()=>[],progress:()=>({}),client:()=>client,user:()=>actor,learning:()=>learning});
   learning=await setupLearning({client:()=>client,user:()=>actor,profile:()=>null,problems:()=>[],progress:()=>({}),openProblem:()=>{}});window.learning=learning;tutorials.refreshLearning();await tutorials.connected();
   document.getElementById('tutorials').hidden=false;location.hash='#tutorial/standalone-fixture';
  }'''
  def start():
   page.goto(base+'/index.html?activity-run='+str(time.time_ns())+'#tutorial/standalone-fixture',wait_until='networkidle');page.evaluate(setup);page.wait_for_selector('#tutorial-activity-actions:not([hidden])');page.wait_for_function("learning.activityReady()")
  start();bar=page.locator('#tutorial-activity-actions');assert page.locator('#tutorial-learning-extras').inner_text()==''
  bar.locator('button').nth(0).click();page.wait_for_function("learning.lessonRecord('standalone-fixture').viewedAt&&!learning.lessonRecord('standalone-fixture')._activityEvent");assert page.evaluate("!learning.lessonRecord('standalone-fixture').completedAt&&learning.lessonRecord('standalone-fixture').checks.join()==='purpose'&&learning.lessonRecord('standalone-fixture').unknown.keep===8")
  first=page.evaluate("JSON.stringify(learning.lessonRecord('standalone-fixture'))");count=page.evaluate('writes.length');bar.locator('button').nth(0).evaluate('(b)=>b.click()');assert page.evaluate('writes.length')==count
  bar.locator('button').nth(1).click();page.wait_for_function("learning.lessonRecord('standalone-fixture').completedAt&&!learning.lessonRecord('standalone-fixture')._activityEvent");complete=page.evaluate("JSON.stringify(learning.lessonRecord('standalone-fixture'))");assert page.evaluate("!learning.mastery(lessons[0]).mastered");assert bar.locator('button').nth(1).is_disabled();assert page.evaluate("reads.length>writes.length")
  start();assert page.evaluate("JSON.stringify(learning.lessonRecord('standalone-fixture'))")==complete
  page.evaluate("location.hash='#tutorial/legacy-fixture'");page.wait_for_function("document.getElementById('tutorial-title').textContent==='legacy-fixture'");assert bar.locator('button').nth(1).is_disabled();assert 'огноо тодорхойгүй'in bar.inner_text();assert page.evaluate("!learning.lessonRecord('legacy-fixture').completedAt&&!learning.lessonRecord('legacy-fixture').viewedAt");bar.locator('button').nth(0).click();page.wait_for_function("learning.lessonRecord('legacy-fixture').viewedAt&&!learning.lessonRecord('legacy-fixture')._activityEvent");assert page.evaluate("!learning.lessonRecord('legacy-fixture').completedAt")
  page.evaluate("location.hash='#tutorial/section-fixture'");page.wait_for_function("document.getElementById('tutorial-title').textContent==='section-fixture'");page.locator('#tutorial-reading-mode').select_option('step');page.locator('[data-read-current]').click();page.wait_for_function("learning.lessonRecord('section-fixture').viewedAt&&!learning.lessonRecord('section-fixture')._activityEvent");assert page.evaluate("!learning.lessonRecord('section-fixture').completedAt");page.locator('#tutorial-section-next').click();page.wait_for_function("location.hash.endsWith('/part/1')");page.locator('[data-read-current]').click();page.wait_for_function("learning.lessonRecord('section-fixture').completedAt&&!learning.lessonRecord('section-fixture')._activityEvent")
  page.evaluate("location.hash='#tutorial/retry-fixture';failSave=true");page.wait_for_function("document.getElementById('tutorial-title').textContent==='retry-fixture'");bar.locator('button').nth(0).click();page.wait_for_function("!!learning.lessonRecord('retry-fixture')._activityEvent");pending=page.evaluate("learning.lessonRecord('retry-fixture')._activityEvent.id");assert page.evaluate("!server.alice['tutorial:retry-fixture']");page.evaluate('failSave=false');bar.locator('button').nth(0).click();page.wait_for_function("learning.lessonRecord('retry-fixture').viewedAt&&!learning.lessonRecord('retry-fixture')._activityEvent");assert page.evaluate("server.alice['tutorial:retry-fixture'].viewEventId")==pending
  for width,theme in[(375,'light'),(1200,'light'),(375,'dark'),(1200,'dark')]:
   page.set_viewport_size({'width':width,'height':950});page.evaluate('t=>document.documentElement.dataset.theme=t',theme);assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth'),(width,theme)
   page.screenshot(path=str(ROOT/f'audit/ui-followup/reading-{width}-{theme}.png'),full_page=True)
  page.evaluate("location.hash='#tutorial/isolation-fixture';holdSave=true");page.wait_for_function("document.getElementById('tutorial-title').textContent==='isolation-fixture'");bar.locator('button').nth(0).click();page.wait_for_function("typeof releaseSave==='function'");page.evaluate("async()=>{actor={id:'bob'};localStorage.setItem('fixture-actor','bob');await learning.accountChanged();}");assert page.evaluate("!learning.lessonRecord('isolation-fixture').viewedAt");page.evaluate('holdSave=false;releaseSave()');page.wait_for_timeout(100);assert page.evaluate("!learning.lessonRecord('isolation-fixture').viewedAt&&server.alice['tutorial:isolation-fixture'].viewedAt");assert not bar.locator('button').nth(0).is_disabled()
  page.locator('#tutorial-language').select_option('en');page.wait_for_function("document.querySelector('#tutorial-activity-actions button').textContent==='Mark viewed'");assert 'Reading activity is separate'in bar.inner_text()
  assert errors==[],errors
  result={'status':'passed','actual_modules':['tutorials.js','learning.js','learning-store.js','tutorial-activity.js'],'checks':['full-mode relation-less tutorial controls','viewed distinct from reading completion/mastery','repeat clicks stable','fresh committed save readback despite stale RETURNING','page reload preserves exact saved record','legacy full-read dates remain unknown','section-by-section last section records completion','failed-save retry keeps event ID','pending Alice save cannot contaminate Bob','mobile/desktop light/dark no page overflow','English reading controls and status'],'transport':'synthetic Auth/own-row storage; separate actual PostgreSQL17 concurrency/RLS tests; no real-user writes','limitations':'No authenticated live-user browser claim; feature remains disabled until040 install/readback is verified'}
  (ROOT/'audit/ui-followup/dated-tutorial-browser.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));browser.close()
finally:server.shutdown()
