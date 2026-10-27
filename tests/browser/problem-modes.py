"""Synthetic offline browser QA for modes, persistence and shared UI surfaces."""
import functools,http.server,json,threading,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
seed=json.loads((ROOT/'problems.json').read_text())['problems'][0]
pool=[{**seed,'id':f'ui-{i}','number':i+1,'ref':f'fixture-{i}','title':('Уртгарчиг'*15 if i==0 else f'Fixture {i}'),'tags':[f'tag-{j}-'+'longword'*4 for j in range(20)] if i==0 else ['dp'],'rating':800+i*10,'hints':['One','Two','Three'],'hintsEn':['One','Two','Three']}for i in range(125)]
checks={}
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});page.set_default_timeout(10000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   elif '/problems.json'in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps({'problems':pool}))
   else:r.continue_()
  page.route('**/*',route);page.emulate_media(color_scheme='light')
  page.add_init_script('''window.MathJax={startup:{promise:Promise.resolve()},typesetClear:()=>{},typesetPromise:async()=>{}};
  if(!localStorage.getItem('mode-test-seeded')){localStorage.setItem('think-cp:v1:guest',JSON.stringify({progress:{'ui-0':{status:'solved',hints:2,notes:'Keep me'}},dirty:[]}));localStorage.setItem('mode-test-seeded','1');}''')
  page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_selector('#problems .problem');page.locator('#show-tags').check()
  assert page.locator('#problems .problem').count()==100
  for width in [375,768,1200,1440]:
   page.set_viewport_size({'width':width,'height':950})
   for theme in ['light','dark']:
    if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
    heights={}
    for mode in ['comfortable','compact','minimalist']:
     start=time.perf_counter();page.locator('#problem-density').select_option(mode)
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,theme,mode)
     assert page.locator('#library').evaluate('e=>e.scrollWidth<=e.clientWidth'),(width,theme,mode)
     row=page.locator('#problems .problem').first;heights[mode]=row.evaluate('e=>e.getBoundingClientRect().height')
     assert row.locator('.hint-meter').is_hidden()if mode=='minimalist'else row.locator('.hint-meter').is_visible()
     assert row.locator('.hint-meter').inner_text()=='Hint 2/3'
     assert row.locator('.badge.solved').is_visible()
     if mode=='minimalist':
      assert row.locator('h3').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')>row.locator('.rating').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')
      assert row.locator('.tag-chip').first.evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')<row.locator('h3').evaluate('e=>parseFloat(getComputedStyle(e).fontSize)')
     checks[f'{width}-{theme}-{mode}']={'status':'passed','interaction_ms':round((time.perf_counter()-start)*1000,2)}
    assert heights['compact']<heights['comfortable']
  page.set_viewport_size({'width':1200,'height':950});page.locator('#problem-next').click();assert page.locator('#problems .problem').count()==25
  for mode in ['comfortable','compact','minimalist']:
   page.locator('#problem-density').select_option(mode);assert page.locator('#problems .problem').count()==25
  page.locator('#search').fill('no-matching-fixture');assert page.locator('#problems .problem').count()==0
  assert 'Тохирох бодлого' in page.locator('#problems').inner_text()
  page.locator('#reset-filters').click();assert page.locator('#problems .problem').count()==100
  page.locator('#problems .open').first.click();assert page.locator('#notes').input_value()=='Keep me';page.locator('[data-close=detail]').click()
  for theme,mode in [('light','compact'),('dark','minimalist'),('light','comfortable')]:
   if page.evaluate('document.documentElement.dataset.theme')!=theme:page.locator('#theme-toggle').click()
   page.locator('#problem-density').select_option(mode);page.reload(wait_until='networkidle');page.wait_for_selector('#problems .problem')
   assert page.locator('#problem-density').input_value()==mode
   assert page.evaluate('document.documentElement.dataset.theme')==theme
  checks['persistence_pagination_empty_state_progress']={'status':'passed'}
  for width in [375,1200,1440]:
   page.set_viewport_size({'width':width,'height':950})
   for route_name in ['home','profile','tutorials','plan','groups','community','friends','following']:
    page.evaluate('(r)=>location.hash="#"+r',route_name);page.wait_for_timeout(50)
    if not page.evaluate('document.documentElement.scrollWidth<=innerWidth'):
     page.screenshot(path='/tmp/erdene-ui-overflow.png',full_page=True)
     raise AssertionError((width,route_name,page.evaluate('''()=>[...document.querySelectorAll('main *')].filter(e=>e.getBoundingClientRect().right>innerWidth).slice(0,12).map(e=>[e.tagName,e.id,e.className,e.getBoundingClientRect().width])''')))
    if route_name in ['friends','following']:
     assert page.locator('.site-nav [data-route=community]').get_attribute('aria-current')=='page'
     assert page.locator('.site-nav [data-route=friends],.site-nav [data-route=following]').count()==0
  checks['main_surface_mobile_desktop_overflow']={'status':'passed'}
  page.evaluate("location.hash='#community'");page.locator('#friends-tab').click();page.wait_for_function("location.hash==='#friends'")
  page.locator('#friends-panel').wait_for(state='visible')
  assert page.locator('.site-nav [data-route=community]').get_attribute('aria-current')=='page'
  page.locator('#following-tab').click();page.wait_for_function("location.hash==='#following'");page.locator('#following-panel').wait_for(state='visible')
  checks['users_subtabs_and_deep_links']={'status':'passed'}
  for width in [375,1440]:
   page.set_viewport_size({'width':width,'height':950})
   for theme in ['light','dark']:
    page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    page.evaluate("async()=>{const nav=await import('/navigation.js?v=43');nav.setAdminRoute(false);location.hash='#admin';}")
    page.locator('#route-message').wait_for(state='visible');assert page.locator('#admin').is_hidden();assert page.locator('#admin-nav').is_hidden()
    page.evaluate("async()=>{const nav=await import('/navigation.js?v=43');nav.setAdminRoute(true);location.hash='#admin';}")
    page.locator('#admin').wait_for(state='visible');assert page.locator('.site-nav [data-route=admin]').count()==1
    for target in ['admin-section','admin-tutorials','learning-admin']:
     page.locator('#admin a[href="#'+target+'"]').click();page.locator('#'+target).wait_for(state='visible')
     assert page.locator('#admin-nav').get_attribute('aria-current')=='page'
     page.locator('#'+target+' .admin-back').click();page.locator('#admin').wait_for(state='visible')
    page.evaluate("async()=>{const nav=await import('/navigation.js?v=43');nav.setAdminRoute(false);location.hash='#admin-tutorials';}")
    page.locator('#route-message').wait_for(state='visible');assert page.locator('#admin-tutorials').is_hidden()
  checks['single_admin_hub_three_routes_and_role_visibility']={'status':'passed','scope':'UI role state only; backend auth unchanged'}

  error_page=browser.new_page()
  def failed_route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   elif '/problems.json'in r.request.url:r.fulfill(status=503,body='Unavailable')
   else:r.continue_()
  error_page.route('**/*',failed_route)
  error_page.goto(base+'/index.html#library',wait_until='networkidle')
  assert 'ачаалж чадсангүй' in error_page.locator('#problems').inner_text()
  checks['catalog_load_error_message']={'status':'passed'};error_page.close()
  loading_page=browser.new_page();pending=[]
  def loading_route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   elif '/problems.json'in r.request.url:pending.append(r)
   else:r.continue_()
  loading_page.route('**/*',loading_route);loading_page.goto(base+'/index.html#library',wait_until='domcontentloaded');loading_page.wait_for_timeout(150)
  assert pending and 'ачаалж байна' in loading_page.locator('#problems').inner_text()
  pending[0].fulfill(status=200,content_type='application/json',body='{"problems":[]}')
  loading_page.wait_for_function("document.querySelector('#problems').textContent.includes('Тохирох бодлого')")
  checks['catalog_loading_and_empty_response']={'status':'passed'};loading_page.close()


  assert not errors,errors;browser.close()
finally:server.shutdown()
(ROOT/'audit/PART04-PROBLEM-MODES.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
