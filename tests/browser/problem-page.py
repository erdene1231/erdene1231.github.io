"""Routable problem workspace, real browser/MathJax; synthetic RPC/Auth only."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
seed=next(p for p in json.loads((ROOT/'audit/PART04-REVIEWED-NEW-TASKS.json').read_text())if p.get('editorial'));doc=seed['editorial'];pool=[{**seed,'editorial':None,'id':f'route-{i}','number':i,'title':f'Route Problem {i}','tags':['secret-tag'],'ref':f'route-{i}','url':f'https://example.com/task/{i}','revision':1,'hasEditorial':True,'hints':[r'Хувьсагч $x_1\le y$.',r'$$\frac{x}{2}$$','Finish'],'hintsEn':['A','B','C']}for i in range(1,126)]
for p in pool:p.pop('editorial')
pool[0].update(priorityLevel='low',hasEditorial=False)
checks=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.pool='+json.dumps(pool)+';window.doc='+json.dumps(doc)+''';window.calls=[];window.solverMode='normal';window.testClient={auth:{onAuthStateChange:cb=>window.authCallback=cb,getSession:async()=>({data:{session:null}})},from:name=>({select:()=>({eq:()=>name==='profiles'?{maybeSingle:async()=>({data:null})}:Promise.resolve({data:[]})}),upsert:async()=>({data:[]})}),rpc:async(name,args)=>{calls.push({name,args});if(name==='get_catalog')return{data:{problems:pool,knownIds:pool.map(p=>p.id)}};if(name==='get_problem_editorial')return{data:{body:doc,problemRevision:1}};if(name==='get_problem_solvers'){if(solverMode==='error')return{error:{message:'private backend error'}};if(solverMode==='empty')return{data:[]};return{data:Array.from({length:args.p_offset?1:50},(_,i)=>({username:'public_'+(args.p_offset+i),total_count:51}))};}return{data:name==='is_admin'?false:[]};}};''')
  def route(r):
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not r.request.url.startswith(base):r.abort()
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture"};')
   elif '/problems.json'in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps({'problems':pool}))
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_function("document.querySelector('#problems .open')&&!document.querySelector('#problems .open').disabled")
  page.locator('#search').fill('Route');page.locator('#priority-filter').select_option('high');page.locator('#sort').select_option('number-asc');page.locator('#problem-next').click();assert page.locator('#problems .problem').count()==24
  target=page.locator('#problems .open').first;pid=target.get_attribute('data-problem-id');target.click();page.wait_for_url('**#problem/'+pid)
  assert page.locator('dialog#detail').count()==0;assert page.locator('main > #detail').is_visible();assert page.locator('#library').is_hidden();assert page.locator('.site-nav [data-route=library]').get_attribute('aria-current')=='page'
  origin=page.evaluate('history.state.erdeneProblemOrigin');assert origin['filters']['search']=='Route';assert origin['page']==1
  assert page.locator('#detail-tags').inner_text()=='';assert page.locator('#tags').inner_text()=='';assert 'secret-tag' not in page.locator('#detail').inner_text();assert page.locator('#problem-link').get_attribute('rel')=='noopener noreferrer'
  page.locator('#reveal-detail-tags').click();assert page.locator('#detail-tags').inner_text()=='secret-tag';page.locator('#reveal-detail-tags').click();assert page.locator('#detail-tags').inner_text()==''
  page.locator('#problem-status').select_option('solved');assert page.locator('#detail-tags').inner_text()=='secret-tag';page.locator('#problem-status').select_option('trying');assert page.locator('#detail-tags').inner_text()==''
  page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async text=>window.copiedProblemLink=text}})");page.locator('#problem-share').click();page.wait_for_function('typeof copiedProblemLink==="string"');assert page.evaluate('copiedProblemLink')==base+'/index.html#problem/'+pid
  checks.append('dedicated URL/main page; hidden tags omitted from DOM until explicit reveal/solved; stable progress and safe external link')
  page.locator('#problem-hints-button').click();page.locator('#next-hint').click();page.wait_for_selector('#hint-list mjx-container');assert page.locator('#hint-list mjx-merror').count()==0
  assert page.evaluate("calls.filter(c=>c.name==='get_problem_editorial').length")==0;page.locator('#problem-editorial-button').click();page.wait_for_selector('#problem-editorial article section');assert page.evaluate("calls.filter(c=>c.name==='get_problem_editorial').length")==1
  page.wait_for_function("document.querySelectorAll('#solver-list li').length===50");page.locator('#more-solvers').click();page.wait_for_function("document.querySelectorAll('#solver-list li').length===51");assert page.evaluate("calls.filter(c=>c.name==='get_problem_solvers').at(-1).args.p_offset")==50
  page.evaluate("solverMode='error'");page.locator('#refresh-solvers').click();page.wait_for_function("document.querySelector('#solvers-message').textContent.includes('чадсангүй')");assert 'private backend' not in page.locator('#solvers-message').inner_text()
  page.evaluate("solverMode='empty'");page.locator('#refresh-solvers').click();page.wait_for_function("document.querySelector('#solvers-message').textContent.includes('Одоогоор')");assert page.locator('#solver-list li').count()==0
  checks.append('explicit hint/editorial actions, actual MathJax, lazy editorial; public RPC50+1pagination and safe empty/error states')
  page.evaluate("authCallback('SIGNED_IN',{user:{id:'00000000-0000-0000-0000-000000000002',email:'local-test@example.invalid'}})");page.wait_for_timeout(150);assert page.url.endswith('#problem/'+pid);assert page.locator('#problem-status').input_value()=='new'
  checks.append('auth interruption keeps route and switches to the current user progress')
  for width,theme in [(375,'light'),(1440,'dark')]:
   page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme);assert page.locator('#detail').evaluate('e=>e.scrollWidth<=e.clientWidth');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.locator('#detail').screenshot(path=str(ROOT/f'audit/browser/part04-problem-page-{width}-{theme}.png'))
  page.locator('#problem-back').click();page.wait_for_url('**#library');assert page.locator('#search').input_value()=='Route';assert page.locator('#sort').input_value()=='number-asc';assert page.locator('#priority-filter').input_value()=='high';assert page.locator('#problems .problem').count()==24
  page.wait_for_function('(s)=>Math.abs(scrollY-s)<3',arg=origin['scroll']);page.go_forward();page.wait_for_url('**#problem/'+pid);page.wait_for_selector('#problem-status')
  page.reload(wait_until='networkidle');page.wait_for_function("document.querySelector('#detail-title').textContent.includes('Route Problem')");assert page.url.endswith('#problem/'+pid)
  page.go_back();page.wait_for_url('**#library');assert page.locator('#search').input_value()=='Route';assert page.locator('#problems .problem').count()==24
  checks.append('back/forward and refresh retain shareable route, original list filters/sort/page/scroll; responsive light/dark')
  page.goto(base+'/index.html#problem/1',wait_until='networkidle');page.wait_for_url('**#problem/route-1');assert page.locator('#problem-hints-button').is_hidden();assert page.locator('#problem-hints-panel').is_hidden();assert page.locator('#hint-list .hint').count()==0
  page.goto(base+'/index.html#problem/no-such-problem',wait_until='networkidle');page.wait_for_function("document.querySelector('#detail-title').textContent==='Бодлого олдсонгүй'");assert page.locator('#problem-retry').is_visible();assert page.locator('#problem-share').is_disabled()
  checks.append('numeric direct link canonicalizes to stable ID; Low exposes no hint content; missing/archived-style state has retry/back')
  assert not errors,errors;browser.close()
finally:s.shutdown()
report={'status':'passed','checks':checks,'limits':'Synthetic public RPC/Auth fixtures only; server public-solver function tested separately. No live RLS expansion or production writes.'}
(ROOT/'audit/PART04-PROBLEM-PAGE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
