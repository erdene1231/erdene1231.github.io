"""Real Chromium, synthetic catalog only; no production requests."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='')
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html')
  result=page.evaluate('''async()=>{
   const {openProblemSelection}=await import('/problem-selection-dialog.js?v=36');
   const {filterProblems}=await import('/catalog.js?v=36');
   const pool=Array.from({length:748},(_,i)=>({id:'stable-'+i,number:i+1,title:'Problem '+i,source:i%2?'CSES':'Codeforces',ref:String(1000+i),tags:[i%2?'dp':'math'],rating:800+i,ratingKind:'official'}));
   const progress={'stable-747':{status:'solved',hints:1}};let result=null,active=true;
   const open=()=>openProblemSelection({problems:()=>pool,progress:()=>progress,valid:()=>active,onSelect:r=>result=r});
   const check=(v,m)=>{if(!v)throw Error(m);};open();const root=document.querySelector('dialog[open]');
   check(root.querySelectorAll('input[type=checkbox]').length===748,'entire catalog');
   const field=(key,value)=>{const el=root.querySelector('[data-filter='+key+']');el.value=value;el.dispatchEvent(new Event('input'));};
   field('query','#1');check(root.querySelectorAll('input[type=checkbox]').length===1&&root.querySelector('input[type=checkbox]').value==='1','exact numeric popup lookup');check(!root.querySelector('[data-filter=ratingBand]')&&!document.querySelector('#rating-filter'),'removed rating band');field('query','stable-747');check(root.querySelectorAll('input[type=checkbox]').length===1,'stable ID search');
   field('status','solved');field('source','CSES');field('tag','dp');field('minRating','1500');field('maxRating','1600');
   check(root.querySelectorAll('input[type=checkbox]').length===1,'combined filters use progress');
   root.querySelector('[data-select-filtered]').click();field('query','');field('status','');field('source','');field('tag','');field('minRating','');field('maxRating','900');
   const expected=filterProblems(pool,progress,{maxRating:'900',sort:'rating-asc'});check(root.querySelectorAll('input[type=checkbox]').length===expected.length,'main catalog filter parity');
   root.querySelector('[data-select-filtered]').click();root.querySelector('[data-selection-apply]').click();check(result.length===expected.length+1,'bulk union preserves hidden selection');
   result=null;open();document.querySelector('dialog[open]').dispatchEvent(new Event('cancel'));check(result===null,'cancel makes no edit');
   open();active=false;document.querySelector('dialog[open] [data-selection-apply]').disabled=false;document.querySelector('dialog[open] [data-selection-apply]').click();check(result===null,'actor invalidated');
   return {exact_numeric_popup:'PASS',rating_band_removed:'PASS',all_748:'PASS',id_search:'PASS',combined_filters:'PASS',catalog_filter_parity:'PASS',bulk_selection_across_filters:'PASS',cancel:'PASS',actor_guard:'PASS'};
  }''')
  assert not errors,errors
  page.evaluate('''async()=>{const {mountBlockEditor}=await import('/tutorial-block-editor.js?v=36');window.sections=[{title:'Fixture',blocks:[{type:'problem',problemKey:''}]}];const box=document.createElement('div');box.id='fixture';document.body.append(box);mountBlockEditor(box,sections,{problems:()=>Array.from({length:748},(_,i)=>({number:i+1,id:'p'+i,title:'Task '+i,source:'Judge',ref:String(i),tags:[],rating:1000})),changed:()=>{}});}''')
  page.locator('#fixture').get_by_role('button',name='Бодлого сонгох…').click();page.locator('[data-select-filtered]').click();page.locator('[data-selection-apply]').click()
  assert page.evaluate('sections.reduce((n,s)=>n+s.blocks.length,0)')==748
  assert page.evaluate('sections.every(s=>s.blocks.length<=100)')
  assert page.evaluate('sections.length')==8
  assert page.evaluate('sections[0].blocks[0].problemKey')=='1'
  page.locator('#fixture [data-undo]').click();assert page.evaluate('sections[0].blocks.length')==1
  result['editor_bulk_insert_and_undo']='PASS'
  page.locator('#fixture').get_by_role('button',name='Бодлого сонгох…').click()
  for width in [375,1200]:
   page.set_viewport_size({'width':width,'height':900});assert page.locator('dialog[open]').evaluate('e=>e.scrollWidth<=e.clientWidth');page.locator('dialog[open]').screenshot(path=str(ROOT/f'audit/browser/numeric-problem-dialog-{width}.png'))
  result['responsive']='PASS';browser.close()
finally:server.shutdown()
(ROOT/'audit/NUMERIC-PROBLEM-DIALOG-BROWSER.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
