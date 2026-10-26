"""Real editor controls and learning catalog adapter; synthetic data, no RPC writes."""
import functools
import http.server
import json
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args): pass
server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Quiet, directory=str(ROOT)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
report = {}
try:
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
  page = browser.new_page(viewport={'width':1200,'height':900})
  errors = []
  page.on('pageerror', lambda e: errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base): r.abort(); return
   if '/app.js?' in r.request.url or '/navigation.js?' in r.request.url:
    r.fulfill(status=200, content_type='text/javascript', body=''); return
   r.continue_()
  page.route('**/*', route)
  page.goto(base+'/index.html', wait_until='networkidle')
  page.evaluate('''async()=>{
   window.MathJax={startup:{promise:Promise.resolve()},typesetPromise:async()=>{},typesetClear:()=>{}};
   const {mountBlockEditor}=await import('/tutorial-block-editor.js?v=33');
   const {setupLearning}=await import('/learning.js?v=33');
   window.catalog=Array.from({length:747},(_,i)=>({id:'stable-'+i,number:i+1,title:'Problem '+i,source:'Judge',ref:String(1000+i)}));
   catalog.push({id:'legacy-cses',number:748,title:'Weird Algorithm',source:'CSES',ref:'Old descriptive ref',sourceId:'1068',url:'https://cses.fi/problemset/task/1068/'});
   window.learning=await setupLearning({client:()=>null,user:()=>null,profile:()=>null,problems:()=>catalog,progress:()=>({}),openProblem:()=>{}});
   window.sections=[{title:'Problem chooser',blocks:[{type:'problem',problemKey:'cses|1068'}]}];window.changes=0;
   const root=document.createElement('section');root.id='picker-test';root.style.cssText='max-width:900px;margin:24px';document.body.replaceChildren(root);
   window.editor=mountBlockEditor(root,sections,{problems:()=>learning.problemsForRelations(),changed:()=>changes++});
  }''')
  search=page.get_by_role('searchbox',name='Embedded бодлого хайх')
  choice=page.get_by_role('listbox',name='Embedded бодлого')
  assert page.evaluate('learning.problemsForRelations()===catalog'), 'editor must receive the current catalog, not seed duplicates'
  assert choice.locator('option:not([disabled])').count()==748
  assert page.locator('[data-problem-matches]').inner_text()=='748 / 748 бодлого'
  report['complete_active_catalog_beyond_first_30_without_seed_duplicates']='PASS'
  for query,key in [('stable-746','judge|1746'),('judge|1746','judge|1746'),('747','judge|1746'),('legacy-cses','cses|1068'),('1068','cses|1068'),('Judge 1746','judge|1746')]:
   search.fill(query)
   assert choice.locator(f'option[value="{key}"]').count()==1, query
  report['stable_id_number_source_id_canonical_key_and_multiword_search']='PASS'
  search.fill('stable-746');choice.select_option('judge|1746')
  assert page.evaluate('sections[0].blocks[0].problemKey')=='judge|1746'
  search.fill('no matching problem')
  assert choice.input_value()=='judge|1746'
  assert '0 / 748' in page.locator('[data-problem-matches]').inner_text()
  assert page.evaluate('changes')==1, 'typing or changing filters must not alter the draft'
  search.fill('legacy-cses');choice.select_option('cses|1068')
  assert page.evaluate('sections[0].blocks[0].problemKey')=='cses|1068'
  report['selection_uses_canonical_key_and_filtering_keeps_existing_reference']='PASS'
  page.locator('[data-undo]').click()
  assert page.evaluate('sections[0].blocks[0].problemKey')=='judge|1746'
  page.locator('[data-redo]').click()
  assert page.evaluate('sections[0].blocks[0].problemKey')=='cses|1068'
  report['picker_selection_participates_in_editor_undo_redo']='PASS'
  page.evaluate("catalog=catalog.concat({id:'late-id',number:749,title:'Late catalog entry',source:'Judge',ref:'late'})")
  search.fill('late-id');choice.select_option('judge|late')
  assert page.evaluate('sections[0].blocks[0].problemKey')=='judge|late'
  report['catalog_refresh_is_used_without_reopening_editor']='PASS'
  page.evaluate("sections[0].blocks[0].problemKey='judge|missing';editor.refresh()")
  assert choice.input_value()=='judge|missing'
  assert choice.locator('option[value="judge|missing"]').is_disabled()
  assert 'Одоогоор боломжгүй' in choice.locator('option[value="judge|missing"]').inner_text()
  search.fill('stable-746');choice.select_option('judge|1746')
  assert page.evaluate('sections[0].blocks[0].problemKey')=='judge|1746'
  report['unavailable_saved_reference_is_preserved_and_can_be_replaced']='PASS'
  for width in [375,1200]:
   page.set_viewport_size({'width':width,'height':900})
   assert page.locator('#picker-test').evaluate('e=>e.scrollWidth<=e.clientWidth'), 'picker overflows viewport'
  report['desktop_and_mobile_picker_fit']='PASS'
  assert not errors, errors
  browser.close()
finally: server.shutdown()
(ROOT/'audit/TUTORIAL-PROBLEM-PICKER-BROWSER.json').write_text(json.dumps({'checks':report},indent=2)+'\n')
print(json.dumps({'checks':report}))
