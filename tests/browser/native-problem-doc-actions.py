"""Actual admin/tutorial block components and independent document persistence.
Synthetic transport and actors only: never writes a real user's records.
"""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
row=next(x for x in json.loads((ROOT/'audit/atcoder-io-format/before-targets.json').read_text())if x['body']['id']=='task-749')
body=row['body'];body['statement']=next(x['after_statement']for x in json.loads((ROOT/'audit/atcoder-io-format/patches.json').read_text())if x['id']=='task-749');body['editorial']=json.loads((ROOT/'audit/native-problem-editorials/batch01.json').read_text())[0]['editorial'];body.update(number=749,revision=3,hasEditorial=True,hasStatement=True)
checks=[];errors=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/app.js?'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='')
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={problemBackendVersion:32,problemStatementStorage:"catalog-inline-v1",problemEditorialStorage:"catalog-inline-v1"};')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#admin-section',wait_until='networkidle')
  page.evaluate('''async body=>{
   window.actor={id:'00000000-0000-0000-0000-000000000001'};window.record=structuredClone(body);window.saved=[];window.failEditorial=false;window.pauseSave=false;window.reads=[];
   window.meta=()=>{let p={...record};delete p.statement;delete p.statementProvenance;delete p.editorial;return p;};
   window.client={from(table){return{select(columns){return{eq(field,id){return{maybeSingle:async()=>{reads.push({table,columns,field,id});return{data:{body:structuredClone(record),revision:record.revision}};}};}};}};},rpc:async(name,args)=>{
    if(name==='is_admin')return{data:true};if(name==='get_admin_catalog')return{data:[meta()]};
    if(name==='admin_import_learning_problems')return{error:{code:'22023',message:'Priority must be low, medium or high.'}};
    if(name==='admin_save_problem'){
     if(args.p_body.statementProvenance?.capabilityProbe)return{error:{code:'22023',message:'NATIVE_STATEMENT_PROVENANCE_WITHOUT_BODY'}};
     if(args.p_body.editorial?.__nativeEditorialProbe)return failEditorial?{error:{code:'22023',message:'not installed'}}:{error:{code:'22023',message:'NATIVE_EDITORIAL_VALIDATOR_READY'}};
     if(args.p_revision!==record.revision)return{error:{code:'40001',message:'REVISION_CONFLICT'}};
     if(pauseSave)await new Promise(r=>window.releaseSave=r);
     saved.push(structuredClone(args));record={...record,...args.p_body,revision:record.revision+1};return{data:structuredClone(record)};
    }return{data:[]};}};
   const{setupAdmin}=await import('./admin.js?v=86');window.adminUI=setupAdmin({client:()=>client,user:()=>actor,sources:()=>['AtCoder'],progress:()=>({}),refreshCatalog:async()=>{}});adminUI.connected();
  }''',body)
  page.wait_for_function("document.querySelector('#admin-choose').options.length===2")
  page.evaluate("document.querySelector('#admin-choose').value='749';document.querySelector('#admin-choose').onchange()")
  page.wait_for_function("document.querySelector('#admin-editorial-document input').value.includes('Yokan')&&document.querySelector('#admin-statement-document input').value.length>0")
  for kind in ['statement','editorial']:page.locator(f'#admin-{kind}-document >details>summary').click()
  def title(kind):return page.locator(f'#admin-{kind}-document >details>label input')
  title('statement').fill('Statement unsaved draft');page.locator('#admin-statement-document fieldset input[type=checkbox]').check()
  title('editorial').fill('Editorial independently saved');page.locator('#admin-title').fill('Metadata unsaved draft')
  page.locator('#admin-save-editorial').click();page.wait_for_function('saved.length===1');page.wait_for_function("!document.querySelector('#admin-save-editorial').disabled")
  assert title('statement').input_value()=='Statement unsaved draft';assert page.locator('#admin-title').input_value()=='Metadata unsaved draft'
  assert page.evaluate("!('statement'in saved[0].p_body)&&!('statementProvenance'in saved[0].p_body)&&saved[0].p_body.title!== 'Metadata unsaved draft'&&saved[0].p_revision===3")
  page.locator('#admin-save-statement').click();page.wait_for_function('saved.length===2');page.wait_for_function("!document.querySelector('#admin-save-statement').disabled")
  assert page.evaluate("saved[1].p_revision===4&&!('editorial'in saved[1].p_body)&&record.editorial.title==='Editorial independently saved'&&record.statement.title==='Statement unsaved draft'")
  checks.append('both real tutorial editors; independent document payloads and compatible CAS advance; sibling and metadata drafts retained')
  title('editorial').fill('Still unsaved editorial');title('statement').fill('Still unsaved statement')
  # Invalid unreviewed statement draft must not block metadata-only submit.
  page.locator('#admin-save').click();page.wait_for_function('saved.length===3');page.wait_for_function("!document.querySelector('#admin-save').disabled")
  assert page.evaluate("!('statement'in saved[2].p_body)&&!('editorial'in saved[2].p_body)&&record.title==='Metadata unsaved draft'&&saved[2].p_revision===5")
  assert title('editorial').input_value()=='Still unsaved editorial';assert title('statement').input_value()=='Still unsaved statement'
  checks.append('metadata-only save ignores invalid unsaved native draft, preserves both editors and their undo-capable components')
  # External change + reload only editorial must not silently rebase stale statement/metadata.
  page.evaluate("record.revision++;record.editorial.title='External editorial';record.title='External metadata'");page.on('dialog',lambda d:d.accept())
  page.locator('#admin-reload-editorial').click();page.wait_for_function("document.querySelector('#admin-editorial-document input').value==='External editorial'")
  assert title('statement').input_value()=='Still unsaved statement';assert page.locator('#admin-title').input_value()=='Metadata unsaved draft'
  page.locator('#admin-statement-document fieldset input[type=checkbox]').check();page.locator('#admin-save-statement').click();page.wait_for_function("document.querySelector('#admin-save-statement').parentElement.nextSibling.textContent.includes('REVISION_CONFLICT')")
  assert page.evaluate('saved.length')==3;assert title('statement').input_value()=='Still unsaved statement'
  checks.append('external sibling reload preserves dirty drafts and keeps stale bases: conflicting statement save rejected without data loss')
  page.locator('#admin-editorial-document >details>summary').click();title('editorial').fill('Probe failure retains this');page.evaluate('failEditorial=true');page.locator('#admin-save-editorial').click();page.wait_for_function("document.querySelector('#admin-save-editorial').parentElement.nextSibling.textContent.includes('баталгаажаагүй')")
  assert page.evaluate('saved.length')==3;assert title('editorial').input_value()=='Probe failure retains this'
  checks.append('missing039 fails closed before real write; unsaved editorial retained')
  page.evaluate('actor=null;adminUI.accountChanged()');assert page.locator('#admin-editorial-document .block-rich-input').count()==0;assert page.locator('#admin-statement-document .block-rich-input').count()==0
  assert page.locator('#admin-save-editorial').is_disabled();assert page.locator('#admin-nav').is_hidden()
  checks.append('logout invalidates both documents and all action buttons; existing RLS route used for bounded lazy reads')
  assert not errors,errors;browser.close()
finally:server.shutdown()
report={'status':'passed','checks':checks,'limitations':'Synthetic admin transport/auth with actual native components, not authenticated live-user interaction.'};(ROOT/'audit/native-problem-editorials/native-actions-browser.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
