"""Actual app routes/config with captured anonymous data; synthetic read-only SDK transport."""
import functools,http.server,json,threading,sys,copy
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];capture=Path(sys.argv[1])if len(sys.argv)>1 else Path('/workspace/joi-statements/public-example');catalog=json.loads((capture/'public-catalog.json').read_text());documents=json.loads((capture/'public-native-documents.json').read_text());docs={p['id']:p for p in documents}
actual={p['id']:p for p in catalog['problems']};tiers={k:sum(actual[p['id']].get('priorityLevel','high'if actual[p['id']].get('priority')else'medium')==k for p in documents)for k in['low','medium','high']}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
checks=[];images=Path('/workspace/joi-statements/public-example/browser');images.mkdir(exist_ok=True)
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
  for pid,tier in [('task-899',actual['task-899'].get('priorityLevel','high'if actual['task-899'].get('priority')else'medium'))]:
   page.goto(base+'/index.html#problem/'+pid,wait_until='networkidle');page.wait_for_selector('#problem-statement article section');root=page.locator('#problem-statement');assert root.is_visible();assert page.evaluate("THINK_CP_CONFIG.problemStatementStorage")=='catalog-inline-v1';assert page.evaluate("THINK_CP_CONFIG.problemBackendVersion")==32
   assert page.evaluate("calls.filter(c=>c.name==='get_problem_editorial').length")==0;assert page.evaluate("calls.some(c=>c.name==='native_table_read'&&c.id==='"+pid+"')")
   for width,theme in[(375,'light'),(1200,'dark')]:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    for lang in['mn','en']:
     root.locator('select').select_option(lang);page.wait_for_function("document.querySelectorAll('#problem-statement mjx-container').length>0");assert root.locator('mjx-merror,[data-mjx-error]').count()==0
     expected=docs[pid]['body']if lang=='mn'else docs[pid]['body']['translations']['en'];assert root.locator('pre code').all_text_contents()==[b['text']for s in expected['sections']for b in s['blocks']if b['type']=='code'];assert root.evaluate('e=>e.scrollWidth<=e.clientWidth');checks.append({'id':pid,'tier':tier,'lang':lang,'width':width,'visible_without_hint_action':True,'actual_public_data':pid!='synthetic-low-statement'})
    if pid=='task-899'and width==375:root.screenshot(path=str(images/'medium-mobile.png'))
    if pid=='task-899'and width==1200:root.screenshot(path=str(images/'high-desktop.png'))
  trace={'page_errors':errors,'mathjax_script_elements':page.locator('script[src*="vendor/mathjax/tex-svg.js"]').count(),'mathjax_bundle_loads':page.evaluate("performance.getEntriesByType('resource').filter(x=>x.name.includes('/vendor/mathjax/tex-svg.js')).map(x=>x.name)"),'tutorial_module_urls':page.evaluate("performance.getEntriesByType('resource').filter(x=>x.name.includes('/tutorials.js?')).map(x=>x.name)")};(capture/'mathjax-trace.json').write_text(json.dumps(trace,indent=2)+'\n')
  assert trace['mathjax_script_elements']==1,trace;assert len(trace['tutorial_module_urls'])==1,trace;assert trace['tutorial_module_urls'][0].endswith('tutorials.js?v=94'),trace
  assert not errors,errors;browser.close()
finally:server.shutdown()
report={'status':'passed','existing_target_priority_counts':tiers,'actual_public_example_route_cases':sum(x['actual_public_data']for x in checks),'synthetic_low_gate_cases':sum(not x['actual_public_data']for x in checks),'user_facing_example':'https://erdeneclub.com/#problem/task-899','deployed_config_used_without_override':True,'actual_app_entry_and_lazy_reader':True,'checks':checks,'limits':'Anonymous data were retrieved from production and are exact; browser uses synthetic read-only SDK transport. No live authenticated browser or new priority changes.'};(ROOT/'audit/joi-statements/public-example-flow.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='checks'}))
