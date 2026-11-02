"""Actual app routes/config with six local proposals from current public JOI data; synthetic SDK transport."""
import functools,http.server,json,threading,sys,copy
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];capture=Path('/workspace/io-math-fix/prepared');catalog=json.loads((capture/'public-catalog.json').read_text());documents=json.loads((capture/'public-native-documents.json').read_text());docs={p['id']:p for p in documents}
actual={p['id']:p for p in catalog['problems']};tiers={k:sum(actual[p['id']].get('priorityLevel','high'if actual[p['id']].get('priority')else'medium')==k for p in documents)for k in['low','medium','high']}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
checks=[];images=Path('/workspace/io-math-fix/browser');images.mkdir(exist_ok=True)
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});page.set_default_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(e.stack or str(e)))
  page.add_init_script('window.publicCatalog='+json.dumps(catalog)+';window.publicDocs='+json.dumps(docs)+''';window.calls=[];window.testClient={auth:{onAuthStateChange:()=>{},getSession:async()=>({data:{session:null}})},from:name=>({select:()=>({eq:(field,id)=>name==='profiles'?{maybeSingle:async()=>({data:null})}:name==='problem_catalog'?{maybeSingle:async()=>{calls.push({name:'native_table_read',id});const p=publicDocs[id];return{data:p?{body:{statement:p.body,statementProvenance:p.provenance},revision:p.revision}:null};}}:Promise.resolve({data:[]})}),upsert:async()=>({data:[]})}),rpc:async(name,args)=>{calls.push({name,args});if(name==='get_catalog')return{data:publicCatalog};if(name==='is_admin')return{data:false};return{data:[]};}};''')
  def route(r):
   url=r.request.url
   if 'cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm'in url:r.fulfill(status=200,content_type='text/javascript',body='export function createClient(){return window.testClient;}')
   elif not url.startswith(base):r.abort()
   else:r.continue_()
  page.route('**/*',route)
  for pid in ['task-721','task-723','task-896','task-897','task-898','task-899']:
   tier=actual[pid].get('priorityLevel','medium')
   page.goto(base+'/index.html#problem/'+pid,wait_until='networkidle');page.wait_for_selector('#problem-statement article section');root=page.locator('#problem-statement');assert root.is_visible();assert page.evaluate("THINK_CP_CONFIG.problemStatementStorage")=='catalog-inline-v1';assert page.evaluate("THINK_CP_CONFIG.problemBackendVersion")==32
   assert page.evaluate("calls.filter(c=>c.name==='get_problem_editorial').length")==0;assert page.evaluate("calls.some(c=>c.name==='native_table_read'&&c.id==='"+pid+"')")
   for width,theme in[(375,'light'),(1200,'light'),(375,'dark'),(1200,'dark')]:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    for lang in['mn','en']:
     root.locator('select').select_option(lang);page.wait_for_function("document.querySelectorAll('#problem-statement mjx-container').length>0");assert root.locator('mjx-merror,[data-mjx-error]').count()==0
     expected=docs[pid]['body']if lang=='mn'else docs[pid]['body']['translations']['en'];assert root.locator('pre code').all_text_contents()==[b['text']for s in expected['sections']for b in s['blocks']if b['type']=='code'];assert root.locator('article section').nth(1).locator('.tutorial-math mjx-container').count()==1;assert root.locator('.tutorial-sample-panel mjx-container').count()==0;assert all(x=='rgba(0, 0, 0, 0)' for x in root.locator('pre code').evaluate_all("els=>els.map(e=>getComputedStyle(e).backgroundColor)"));assert root.evaluate('e=>e.scrollWidth<=e.clientWidth');checks.append({'id':pid,'tier':tier,'lang':lang,'width':width,'visible_without_hint_action':True,'prepared_local_statement':True})
    if pid=='task-899'and width==375 and theme=='dark':root.screenshot(path=str(images/'medium-mobile.png'))
    if pid=='task-899'and width==1200 and theme=='light':root.screenshot(path=str(images/'high-desktop.png'))

  roundtrips=page.evaluate("""async()=>{const {setupProblemStatementEditor}=await import('./problem-statement.js?v=94');const host=document.createElement('div');document.body.append(host);let n=0;for(const id of ['task-721','task-723','task-896','task-897','task-898','task-899']){const p=publicCatalog.problems.find(p=>p.id===id);const ui=setupProblemStatementEditor(host,{locked:()=>false,user:()=>({id:'fixture'}),client:()=>testClient,problems:()=>publicCatalog.problems,progress:()=>({})});await ui.edit(p);if(JSON.stringify(ui.collect())!==JSON.stringify(publicDocs[id].body))throw Error('initial roundtrip');const select=host.querySelector('select');select.value='en';select.dispatchEvent(new Event('change'));select.value='mn';select.dispatchEvent(new Event('change'));const saved=structuredClone(ui.collect());publicDocs[id].body=saved;ui.markSaved();await ui.edit(p);if(JSON.stringify(ui.collect())!==JSON.stringify(saved))throw Error('reload');ui.invalidate();host.replaceChildren();n++;}host.remove();return n;}""")
  assert roundtrips==6
  page.evaluate(r'''async()=>{const {renderBlock,typeset}=await import('./tutorials.js?v=94');window.literalSample='  $x$ \\(y\\) <img src=x onerror=alert(1)>\t\n\nend\n';window.literalHost=document.createElement('article');literalHost.className='tutorial-content';document.body.append(literalHost);renderBlock({type:'code',language:'Input',text:literalSample},literalHost,'en');await typeset([literalHost]);window.copyResult=null;Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>copyResult=text},configurable:true});}''')
  assert page.locator('article').last.locator('mjx-container,img').count()==0
  assert page.locator('article').last.locator('pre code').text_content()==page.evaluate('literalSample')
  page.locator('article').last.get_by_role('button',name='Copy Input',exact=True).click()
  page.wait_for_function('copyResult===literalSample')
  trace={'page_errors':errors,'mathjax_script_elements':page.locator('script[src*="vendor/mathjax/tex-svg.js"]').count(),'mathjax_bundle_loads':page.evaluate("performance.getEntriesByType('resource').filter(x=>x.name.includes('/vendor/mathjax/tex-svg.js')).map(x=>x.name)"),'tutorial_module_urls':page.evaluate("performance.getEntriesByType('resource').filter(x=>x.name.includes('/tutorials.js?')).map(x=>x.name)")};(capture/'mathjax-trace.json').write_text(json.dumps(trace,indent=2)+'\n')
  assert trace['mathjax_script_elements']==1,trace;assert len(trace['tutorial_module_urls'])==1,trace;assert trace['tutorial_module_urls'][0].endswith('tutorials.js?v=94'),trace
  assert not errors,errors;browser.close()
finally:server.shutdown()
report={'status':'passed','native_editor_roundtrips':roundtrips,'plain_delimiter_and_clipboard_test':True,'existing_target_priority_counts':tiers,'prepared_local_route_cases':len(checks),'user_facing_example':'https://erdeneclub.com/#problem/task-899','existing_config_used_without_override':True,'actual_app_entry_and_lazy_reader':True,'checks':checks,'limits':'Fresh anonymous JOI data with six local statement proposals; actual app/editor/math components with synthetic read-only SDK transport. Not deployed or production-saved; no real-user authenticated mutation or new priority changes.'};(ROOT/'audit/joi-input-format/browser.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'}))
