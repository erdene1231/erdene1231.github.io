"""Actual app.js catalog UI with local synthetic progress; no connected services."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
data=json.loads((ROOT/'problems.json').read_text());data['problems']=data['problems'][:8]
for p in data['problems']:p['hints']=['Hint one','Hint two','Hint three'];p['tags']=['test-tag']
progress={p['id']:{'status':'solved' if i in [0,3] else 'trying' if i==2 else 'new','hints':i if i<4 else 0,'notes':''} for i,p in enumerate(data['problems'])}
checks={}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/config.js' in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   elif '/problems.json' in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps(data))
   else:r.continue_()
  page.route('**/*',route);page.add_init_script('localStorage.setItem("think-cp:v1:guest",'+json.dumps(json.dumps({'progress':progress,'dirty':[]}))+');localStorage.setItem("think-cp:catalog-preferences",JSON.stringify({showTags:false}));window.MathJax={startup:{promise:Promise.resolve()},typesetClear:()=>{},typesetPromise:async()=>{}};')
  page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_selector('#problems .problem');page.wait_for_function("typeof document.querySelector('#show-tags').onchange==='function'||document.querySelector('#problem-density').onchange!==null")
  assert page.locator('#packs').count()==0;checks['pack_tabs_removed']='PASS'
  assert page.locator('#problems .tag-chip').count()==0;checks['solved_tags_hidden_when_toggle_off']='PASS'
  page.locator('#show-tags').check();assert page.locator('#problems .tag-chip').count()==8
  page.locator('#show-tags').uncheck();assert page.locator('#problems .tag-chip').count()==0;checks['toggle_hides_all_tags_again']='PASS'
  for i in range(4):
   row=page.locator('#problems .problem').filter(has=page.locator('.number',has_text='#'+str(data['problems'][i]['number']).zfill(3)))
   assert row.locator('.hint-meter').inner_text()==f'Hint {i}/3'
   assert row.locator('.hint-meter').get_attribute('class').endswith('hint-level-'+str(i))
   assert row.locator('.hint-meter').evaluate('e=>e.nextElementSibling.classList.contains("badge")')
  checks['hint_0_to_3_boxes_before_status']='PASS'
  row=page.locator('#problems .problem').filter(has=page.locator('.number',has_text='#'+str(data['problems'][0]['number']).zfill(3)))
  row.locator('button.open').click();assert page.locator('#detail-tags').is_hidden();assert page.locator('#tags').is_hidden();checks['solved_detail_tags_hidden']='PASS'
  page.locator('#reveal-detail-tags').click();assert page.locator('#detail-tags').is_visible();page.evaluate("document.querySelector('#detail').close()")
  page.locator('#show-tags').check();page.locator('#show-tags').uncheck();row.locator('button.open').click();assert page.locator('#detail-tags').is_hidden();page.evaluate("document.querySelector('#detail').close()")
  checks['explicit_detail_reveal_and_global_reset']='PASS'
  for width in [375,1200]:
   for theme in ['light','dark']:
    page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
    assert page.locator('#library').evaluate('e=>e.scrollWidth<=e.clientWidth')
    page.locator('#library').screenshot(path=str(ROOT/f'audit/browser/catalog-ui-{width}-{theme}.png'))
  checks['desktop_mobile_light_dark']='PASS';assert not errors,errors;browser.close()
finally:server.shutdown()
(ROOT/'audit/CATALOG-UI-BROWSER.json').write_text(json.dumps({'checks':checks,'errors':errors},indent=2)+'\n');print(json.dumps(checks))
