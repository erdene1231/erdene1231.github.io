"""Canonical priority/filter/rating UI in Chromium; no production services."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';report={}
data=json.loads((ROOT/'problems.json').read_text());data['problems']=data['problems'][:9]
for i,p in enumerate(data['problems']):p.update(priorityLevel=['low','medium','high'][i%3],priority=False,rating=[800,1200,1400,1600,1900,2100,2400,3000,4000][i],ratingKind='estimated')
data['problems'][0]['ratingKind']='official'
data['problems'][8].update(rating=None,ratingKind='unrated')
data['problems'][0].update(hints=['Hidden one','Hidden two','Hidden three'],hintsEn=['Hidden A','Hidden B','Hidden C'])
lessons=json.loads((ROOT/'tutorials.json').read_text());lessons['tutorials']=lessons['tutorials'][:3]
for i,t in enumerate(lessons['tutorials']):t.update(priorityLevel=['low','medium','high'][i],priorityReason='Fixture rationale',prerequisiteIds=[],related=[])
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});page.set_default_timeout(10000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/config.js' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   elif '/problems.json' in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps(data))
   elif '/tutorials.json' in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps(lessons))
   else:r.continue_()
  page.route('**/*',route);page.add_init_script('window.MathJax={startup:{promise:Promise.resolve()},typesetClear:()=>{},typesetPromise:async()=>{}};')
  page.add_init_script("localStorage.setItem('think-cp:catalog-preferences',JSON.stringify({showTags:false,sort:'rating-asc',priorityOnly:true}));")
  page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_selector('#problems .priority-badge')
  assert page.locator('#priority-only').count()==0 and page.locator('#problems .problem').count()==9
  assert not page.evaluate("Object.hasOwn(JSON.parse(localStorage.getItem('think-cp:catalog-preferences')),'priorityOnly')")
  page.locator('#priority-filter').select_option('low');assert page.locator('#problems .problem').count()==3
  for mode in ['comfortable','compact','minimalist']:
   page.locator('#problem-density').select_option(mode);assert page.locator('#problems .hint-meter:visible').count()==0
  page.locator('#problem-density').select_option('comfortable')
  page.locator('#problems .open').first.click();assert page.locator('#detail .hints').is_hidden();assert page.locator('#hint-list .hint').count()==0
  before=page.evaluate("localStorage.getItem('think-cp:v1:guest')")
  page.evaluate("document.querySelector('#next-hint').onclick()")
  assert page.evaluate("localStorage.getItem('think-cp:v1:guest')")==before
  page.locator('[data-close=detail]').click();report['low_hint_suppression_all_modes_without_progress_mutation']='PASS'

  assert page.locator('#problems .priority-low').count()==3
  page.locator('#reset-filters').click();page.locator('#sort').select_option('priority')
  assert 'High' in page.locator('#problems .priority-badge').first.inner_text()
  page.locator('#priority-filter').select_option('high');assert page.locator('#problems .problem').count()==3
  page.locator('#reset-filters').click();report['canonical_main_filter_sort_and_obsolete_toggle_removed']='PASS'
  assert page.locator('#problems .rating-legendary').count()==1
  assert page.locator('#problems .rating-candidate-master').count()==1
  for index,problem in enumerate(data['problems']):
   page.locator('#problems .problem .open').nth(index).click()
   assert page.locator('#detail-note .rating').count()==1
   label=page.locator('#detail-note .rating').inner_text()
   assert ('Unrated' in label) if problem['ratingKind']=='unrated' else ('≈' in label)==(problem['ratingKind']=='estimated')
   page.locator('[data-close=detail]').click()
  report['rating_detail_official_estimated_unrated']='PASS'
  page.evaluate('(p)=>window.fixturePool=p',data['problems'])
  page.evaluate('''async()=>{const {openProblemSelection}=await import('/problem-selection-dialog.js?v=41');openProblemSelection({problems:()=>fixturePool,onSelect:()=>{}})}''')
  page.locator('[data-filter=priorityLevel]').select_option('medium')
  assert page.locator('[data-selection-available] input').count()==3
  assert page.locator('[data-selection-available] [data-priority-level=medium]').count()==3
  page.locator('[data-select-filtered]').click();page.locator('[data-reset-filters]').click()
  assert page.locator('[data-selection-chosen] input').count()==3
  page.get_by_role('button',name='Болих',exact=True).click();report['popup_priority_filter_preserves_selection']='PASS'
  for width in [375,1200]:
   for theme in ['light','dark']:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    assert page.locator('.rating-legendary').first.evaluate('(e)=>getComputedStyle(e).backgroundColor')!=page.locator('.rating-pupil').first.evaluate('(e)=>getComputedStyle(e).backgroundColor')
    contrast=page.locator('#problems .rating').evaluate_all(r'''els=>{const lum=c=>{const a=c.match(/[\d.]+/g).slice(0,3).map(Number).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4});return a[0]*.2126+a[1]*.7152+a[2]*.0722};return els.map(e=>{const s=getComputedStyle(e),a=lum(s.color),b=lum(s.backgroundColor);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)})}''')
    assert min(contrast)>=4.5,(theme,contrast)
    page.locator('#library').screenshot(path=str(ROOT/f'audit/browser/priority-catalog-{width}-{theme}.png'))
  report['rating_light_dark_text_contrast']='PASS'
  page.evaluate("location.hash='#tutorials'");page.wait_for_selector('#tutorial-grid .tutorial-card')
  page.locator('#tutorial-priority-filter').select_option('high');page.wait_for_function("document.querySelectorAll('#tutorial-grid .tutorial-card').length===1")
  assert 'High' in page.locator('#tutorial-grid .priority-badge').inner_text()
  page.locator('#tutorial-priority-filter').select_option('');page.locator('#tutorial-priority-sort').select_option('priority')
  page.wait_for_function("document.querySelector('#tutorial-grid .priority-badge').textContent.includes('High')")
  report['tutorial_priority_filter_and_sort']='PASS'
  # Real admin form payload with fixture RPC; canonical field beats legacy boolean.
  page.evaluate('''async()=>{document.querySelector('#admin-priority-reason')?.closest('label').remove();const {setupAdmin}=await import('/admin.js?v=41');window.adminPayload=null;const client={rpc:async(name,args)=>{if(name==='is_admin')return {data:true};if(name==='get_admin_catalog')return {data:fixturePool};if(name==='admin_list')return {data:[]};if(name==='admin_save_problem'){adminPayload=args.p_body;return {data:{...args.p_body,number:999}};}return {data:[]};}};window.testAdmin=setupAdmin({user:()=>({id:'fixture'}),client:()=>client,sources:()=>[],refreshCatalog:async()=>{}});testAdmin.connected();location.hash='#admin-section';}''')
  page.wait_for_function("document.querySelector('#admin-choose').options.length>1")
  page.locator('#admin-title').fill('Priority fixture');page.locator('#admin-ref').fill('fixture');page.locator('#admin-url').fill('https://example.com/task');page.locator('#admin-tags').fill('math');page.locator('#admin-priority').select_option('high');page.locator('#admin-priority-reason').fill('Necessary mastery observation')
  page.locator('#admin-save').click();page.wait_for_function('adminPayload!==null')
  assert page.evaluate("adminPayload.priorityLevel==='high'&&adminPayload.priority===true&&adminPayload.priorityReason==='Necessary mastery observation'")
  report['admin_canonical_priority_payload']='PASS'
  assert not errors,errors;report['responsive_light_dark_no_runtime_errors']='PASS';browser.close()
finally:server.shutdown()
(ROOT/'audit/PART04-PRIORITY-BROWSER.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
