"""Real bundled MathJax for dynamic bilingual hints; no external services."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}'
p=json.loads((ROOT/'problems.json').read_text())['problems'][0]
pool=[{**p,'id':'math-high','number':1,'title':'Math High','priorityLevel':'high','hints':[r'Хувьсагч $a_i$ ба $x\le y$.',r'$$\frac{n(n+1)}{2}$$',r'`$code_only$` бол code. <img src=x onerror=alert(1)>'], 'hintsEn':[r'Variable \(b_j\) and \(u\ge v\).',r'\[\frac{x}{y}\]',r'`$code_only$` remains code.']},{**p,'id':'math-low','number':2,'title':'Math Low','priorityLevel':'low','hints':[r'$hidden$',r'$x$',r'$y$'],'hintsEn':['A','B','C']}]
checks={}
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(viewport={'width':1200,'height':950});page.set_default_timeout(20000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   if not r.request.url.startswith(base):r.abort()
   elif '/config.js'in r.request.url:r.fulfill(status=200,content_type='text/javascript',body='window.THINK_CP_CONFIG={};')
   elif '/problems.json'in r.request.url:r.fulfill(status=200,content_type='application/json',body=json.dumps({'problems':pool}))
   else:r.continue_()
  page.route('**/*',route);page.goto(base+'/index.html#library',wait_until='networkidle');page.wait_for_selector('#problems .open')
  page.get_by_role('button',name='Math High',exact=False).first.click();page.locator('#problem-hints-button').click();page.locator('#next-hint').click();page.locator('#problem-back').click()
  page.get_by_role('button',name='Math Low',exact=False).first.click();assert page.locator('#detail .hints').is_hidden();assert page.locator('#hint-list mjx-container').count()==0;page.locator('#problem-back').click()
  for theme,width in [('light',1200),('dark',375)]:
   page.set_viewport_size({'width':width,'height':950});page.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
   page.get_by_role('button',name='Math High',exact=False).first.click();page.locator('#problem-hints-button').click()
   while page.locator('#next-hint').is_visible():page.locator('#next-hint').click()
   for language in ['mn','en']:
    page.locator('#hint-language').select_option(language)
    page.wait_for_function("document.querySelectorAll('#hint-list mjx-container').length===3")
    assert page.locator('#hint-list .hint').count()==3
    assert page.locator('#hint-list mjx-merror,#hint-list [data-mjx-error]').count()==0
    assert page.locator('#hint-list code').inner_text()=='$code_only$'
    assert page.locator('#hint-list code mjx-container,#hint-list img').count()==0
    assert page.locator('#detail').evaluate('e=>e.scrollWidth<=e.clientWidth')
    page.locator('#toggle-hints').click();assert page.locator('#hint-list').is_hidden()
    page.locator('#toggle-hints').click();page.wait_for_function("document.querySelectorAll('#hint-list mjx-container').length===3")
   page.locator('#problem-back').click();page.wait_for_function("document.querySelectorAll('#hint-list mjx-container').length===0")
  saved=page.evaluate("JSON.parse(localStorage.getItem('think-cp:v1:guest')).progress['math-high'].hints");assert saved==3
  assert not errors,errors;checks={'actual_bundled_mathjax':'passed','inline_display_subscript_fraction_inequality':'passed','mn_en_reveal_repeat_close_reopen':'passed','light_desktop_dark_mobile':'passed','code_spans_and_html_escape':'passed','low_hidden_and_hint_progress_preserved':'passed'};b.close()
finally:s.shutdown()
(ROOT/'audit/PART04-HINT-MATH.json').write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks))
