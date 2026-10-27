"""Actual reader/admin components with mocked RPC only; no remote writes."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
p=next(p for p in json.loads((ROOT/'audit/PART04-REVIEWED-NEW-TASKS.json').read_text())if p.get('editorial'))
p={**p,'id':'editorial-ui','number':1,'revision':1,'tags':[p['primaryTopic']],'hasEditorial':True,'priority':True,'level':'Practice'};doc=p.pop('editorial');checks=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.fixtureProblem='+json.dumps(p)+';window.fixtureDoc='+json.dumps(doc)+''';window.requests=[];window.testClient={auth:{getSession:async()=>({data:{session:null}}),onAuthStateChange:()=>{}},rpc:async(name,args)=>{requests.push(name);if(name==='get_catalog')return{data:{problems:[fixtureProblem,{...fixtureProblem,id:'slow',number:2,title:'Slow editorial'},{...fixtureProblem,id:'missing',number:3,title:'Missing editorial',hasEditorial:false}],knownIds:['editorial-ui','slow','missing']}};if(name==='get_problem_editorial'){if(args.p_problem_id==='slow')return new Promise(resolve=>window.resolveSlow=()=>resolve({data:{body:{...fixtureDoc,title:'STALE DOCUMENT'},problemRevision:1}}));return{data:{body:fixtureDoc,problemRevision:1,revision:1}};}return{data:name==='is_admin'?false:[]};}};''')
  def route(r):
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not r.request.url.startswith(base):r.abort()
   elif '/config.js' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={supabaseUrl:"https://fixture.invalid",supabaseKey:"public-test-fixture"};')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_selector('#problems .open')
  assert page.evaluate("requests.filter(x=>x==='get_problem_editorial').length")==0
  for width,theme in [(375,'light'),(1200,'dark')]:
   page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
   page.get_by_role('button',name=p['title'],exact=False).first.click();page.locator('#problem-editorial summary').click();page.wait_for_selector('#problem-editorial article section')
   assert page.locator('#problem-editorial article pre code').count()==1
   assert page.locator('#problem-editorial').evaluate('e=>e.scrollWidth<=e.clientWidth')
   page.locator('#problem-editorial select').select_option('en');assert 'not published' in page.locator('#problem-editorial p.muted').inner_text()
   page.locator('#problem-status').select_option('trying');assert page.locator('#problem-editorial details').get_attribute('open') is not None
   page.locator('#problem-back').click()
  checks.append('actual app: lazy body RPC only on open; rich code, language fallback, status preserves reader, mobile/light and desktop/dark')
  page.get_by_role('button',name='Slow editorial',exact=False).first.click();page.locator('#problem-editorial summary').click();page.wait_for_function('typeof resolveSlow==="function"')
  page.locator('#problem-back').click();page.get_by_role('button',name='Missing editorial',exact=False).first.click();page.locator('#problem-editorial summary').click();page.evaluate('resolveSlow()');page.wait_for_timeout(100)
  assert 'бэлтгэгдэж' in page.locator('#problem-editorial').inner_text();assert page.locator('#problem-editorial article section').count()==0
  checks.append('stale lazy response cannot populate another problem; missing High editorial stated honestly');page.close()
  # Isolate the real admin component; the application itself is blocked to avoid duplicate handlers.
  page=browser.new_page(viewport={'width':1200,'height':950});page.on('pageerror',lambda e:errors.append(str(e)))
  def admin_route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/app.js?'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='')
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   else:r.continue_()
  page.route('**/*',admin_route);page.goto(base+'/index.html#admin-section',wait_until='networkidle')
  page.evaluate('''async({p,doc})=>{window.actor={id:'00000000-0000-0000-0000-000000000001'};window.rows=[p];window.documentBody=doc;window.saved=[];window.allowed=true;window.backendAvailable=true;window.client={rpc:async(name,args)=>{if(name==='is_admin')return{data:allowed};if(name==='get_admin_catalog')return{data:rows};if(name==='get_problem_editorial')return backendAvailable?{data:{body:documentBody,problemRevision:rows[0].revision}}:{error:{code:'PGRST202',message:'not installed'}};if(name==='admin_save_problem'){saved.push(args);documentBody=args.p_body.editorial;rows=[{...p,...args.p_body,editorial:undefined,hasEditorial:!!documentBody,revision:p.revision+saved.length}];return{data:{...rows[0],editorial:documentBody}};}return{data:[]};}};const{setupAdmin}=await import('./admin.js?v=46');window.adminUI=setupAdmin({client:()=>client,user:()=>actor,sources:()=>['AtCoder'],progress:()=>({}),refreshCatalog:async()=>{}});adminUI.connected();}''',{'p':p,'doc':doc})
  page.wait_for_function("document.querySelector('#admin-choose').options.length===2")
  page.evaluate("const s=document.querySelector('#admin-choose');s.value='1';s.onchange()")
  page.wait_for_function("document.querySelector('#admin-editorial-document input').value.length>0")
  page.locator('#admin-editorial-document > details > summary').click();editable=page.locator('#admin-editorial-document .block-rich-input').first;editable.fill('Шинээр зассан тайлбар $x_1$.')
  page.locator('#admin-save').click();page.wait_for_function('saved.length===1');assert page.evaluate("saved[0].p_body.editorial.sections[0].blocks[0].content[0].text")=='Шинээр зассан тайлбар $x_1$.'
  assert page.evaluate('saved[0].p_revision')==1;assert page.evaluate('saved[0].p_body.ratingBasis')==p['ratingBasis']
  checks.append('actual admin: lazy editor load, existing tutorial block authoring, shared revision save payload and explicit rating rationale preserved')
  page.wait_for_function("document.querySelector('#admin-choose').value==='1'");page.wait_for_timeout(100)
  page.locator('#admin-editorial-document > details > summary').click();page.locator('#admin-editorial-document .block-rich-input').first.fill('Do not lose this draft')
  page.evaluate('backendAvailable=false');page.locator('#admin-save').click();page.wait_for_function("document.querySelector('#admin-message').textContent.includes('идэвхжээгүй')");assert page.evaluate('saved.length')==1;assert 'Do not lose this draft' in page.locator('#admin-editorial-document').inner_text();checks.append('missing backend fails closed before write and retains unsaved rich content')
  page.on('dialog',lambda d:d.dismiss());page.locator('#admin-new').click();assert page.locator('#admin-choose').input_value()=='1'
  page.evaluate("actor=null;adminUI.accountChanged()");assert page.locator('#admin-nav').is_hidden();assert page.locator('#admin-editorial-document .block-rich-input').count()==0
  checks.append('dirty-editor switch cancellation and logout invalidation preserve privacy')
  assert not errors,errors;browser.close()
finally:s.shutdown()
report={'status':'passed','checks':checks,'limitations':'Mocked RPC with actual frontend components. SQL proposal tested separately in synthetic PGlite; no live backend/schema/permission changes.'}
(ROOT/'audit/PART04-EDITORIAL-UI.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
