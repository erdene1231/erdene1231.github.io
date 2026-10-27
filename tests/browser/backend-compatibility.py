import http.server,threading,functools,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/app.js?'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='')
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#admin-section',wait_until='networkidle')
  page.evaluate('''async()=>{window.actor={id:'00000000-0000-0000-0000-000000000001'};window.calls=[];window.row={id:'stable',number:1,revision:1,title:'Original',source:'Codeforces',ref:'1A',url:'https://codeforces.com/contest/1/problem/A',rating:800,ratingKind:'official',priority:true,tags:['math'],hints:['Original hint','Second','Third'],hintsEn:['Original hint','Second','Third'],level:'Practice'};window.saved=[];window.client={rpc:async(name,args)=>{calls.push(name);if(name==='is_admin')return{data:true};if(name==='get_admin_catalog')return{data:[row]};if(name==='admin_save_problem'){saved.push(args);row={...args.p_body,id:'stable',number:1,revision:2};return{data:row};}if(name==='get_problem_editorial'||name==='get_problem_statement')throw Error('Uninstalled RPC must not be called');return{data:[]};}};const{setupAdmin}=await import('./admin.js?v=49');window.ui=setupAdmin({client:()=>client,user:()=>actor,sources:()=>['Codeforces'],refreshCatalog:async()=>{}});ui.connected();}''')
  page.wait_for_function('document.querySelector("#admin-choose").options.length===2');page.evaluate("ui.editProblem('stable')");page.locator('#admin-title').fill('Edited safely');assert page.locator('#admin-priority').is_disabled();assert page.locator('#admin-new').is_disabled();assert page.locator('#admin-import-file').is_disabled();assert page.locator('#admin-editorial-document').is_hidden();assert page.locator('#admin-statement-document').is_hidden();page.locator('#admin-save').click();page.wait_for_function('saved.length===1');assert page.evaluate('saved[0].p_body.priority')is True;assert page.evaluate('"priorityLevel" in saved[0].p_body')is False;assert page.evaluate('row.id')=='stable';assert page.evaluate('row.hints[0]')=='Original hint';assert page.evaluate('calls.some(x=>x.startsWith("get_problem_"))')is False
  for theme,width in [('light',375),('dark',1200)]:
   page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme);assert page.locator('#admin-form').evaluate('e=>e.scrollWidth<=e.clientWidth')
  assert not errors,errors;browser.close()
finally:server.shutdown()
report={'status':'passed','scope':'Local browser with installed-031-shaped mock RPC;actual SQL contract checked separately in Node','checks':['existing edit works without uninstalled RPCs','stable ID/legacy priority/hints preserved','new priority/rich content/bulk writes gated','mobile light/desktop dark no overflow','no browser errors']};(ROOT/'audit/PART04-BACKEND-COMPATIBILITY-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
