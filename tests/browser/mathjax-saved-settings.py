"""Real mobile runtime + published payloads, persisted MathJax menus and missing components.
Only the public RPC transport and injected network faults are intercepted. No fake typesetter.
"""
import argparse,functools,http.server,json,pathlib,threading,urllib.request
from playwright.sync_api import sync_playwright
ap=argparse.ArgumentParser();ap.add_argument('--payload-dir',required=True);a=ap.parse_args()
R=pathlib.Path(__file__).resolve().parents[2];W=pathlib.Path(a.payload_dir)
raw={n:(W/(n+'.json')).read_bytes() for n in ['get_catalog','get_tutorials']}
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)))
threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';cache={};results=[]
cases=[('default',{}),('chtml',{'renderer':'CHTML'}),('explorer',{'explorer':True}),('collapsible',{'collapsible':True}),('combined',{'renderer':'CHTML','explorer':True,'collapsible':True,'locale':'fr','scale':1.2}),('component-failure',{'renderer':'CHTML'}),('component-delay',{'explorer':True}),('menu-switch',{})]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for mode,settings in cases:
   page=b.new_page(**pw.devices['Pixel 7'],color_scheme='dark' if mode in ['explorer','combined','component-delay'] else 'light');page.clock.install()
   saved=json.dumps(settings);page.add_init_script('localStorage.setItem("MathJax-Menu-Settings",'+json.dumps(saved)+');')
   requests=[];failures=[];errors=[];held=[];released=False;attempts=0
   page.on('pageerror',lambda e:errors.append(str(e)))
   def route(r):
    global attempts
    u=r.request.url
    if u.startswith(base):
     if '/vendor/mathjax/'in u:
      requests.append(u.removeprefix(base));path=u.split('/vendor/mathjax/')[1].split('?')[0]
      assert (R/'vendor/mathjax'/path).is_file(),path
      if mode=='component-failure'and path=='output/chtml.js':
       attempts+=1
       if attempts==1:return r.fulfill(status=503,body='injected temporary component failure')
      if mode=='component-delay'and path=='a11y/sre.js'and not released:held.append(r);return
     return r.continue_()
    if u.startswith('https://cdn.jsdelivr.net/') and 'mathjax' not in u and 'speech-rule' not in u:
     if u not in cache:cache[u]=urllib.request.urlopen(u,timeout=30).read()
     return r.fulfill(status=200,content_type='text/javascript',body=cache[u])
    for n in raw:
     if u.endswith('/rpc/'+n):return r.fulfill(status=200,content_type='application/json',body=raw[n])
    if '/rpc/get_leaderboard'in u:return r.fulfill(status=503,content_type='application/json',body='{"message":"unrelated unavailable read"}')
    failures.append(u);return r.abort()
   page.route('**/*',route);page.goto(base+'/#tutorial/introduction',wait_until='domcontentloaded');page.wait_for_selector('#tutorial-content section')
   if mode=='component-failure':
    page.locator('#tutorial-math-retry').wait_for(state='visible');assert page.locator('#tutorial-content mjx-container').count()==0
    page.locator('#tutorial-math-retry').click()
   if mode=='component-delay':
    for _ in range(150):
     if held:break
     page.wait_for_timeout(20)
    assert held;page.clock.fast_forward(31000);page.locator('#tutorial-math-retry').wait_for(state='visible')
    page.locator('#tutorial-math-retry').click();assert requests.count('/vendor/mathjax/tex-svg.js')==1
    released=True
    for r in held:r.fulfill(status=200,content_type='text/javascript',body=(R/'vendor/mathjax/a11y/sre.js').read_bytes())
   page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container").length===209',timeout=20000)
   page.wait_for_function('document.querySelector("#tutorial-math-message").textContent===""')
   if mode=='menu-switch':
    page.evaluate('MathJax.startup.document.menu.settings.renderer="CHTML";MathJax.startup.document.menu.setRenderer("CHTML")')
    page.wait_for_function('document.querySelectorAll("#tutorial-content mjx-container[jax=CHTML]").length===209')
    page.evaluate('MathJax.startup.document.menu.settings.explorer=true;MathJax.startup.document.menu.setExplorer(true)')
    page.wait_for_function('MathJax._.a11y.explorer && !MathJax.startup.document.menu.isLoading && document.querySelectorAll("#tutorial-content mjx-container").length===209 && [...document.querySelectorAll("#tutorial-content .tutorial-math")].every(x=>x.querySelector("mjx-container"))')
   assert page.locator('#tutorial-content mjx-merror').count()==0
   assert page.locator('#tutorial-content .tutorial-math').evaluate_all('(xs)=>xs.every(x=>x.querySelector("mjx-container"))')
   assert page.locator('script[src*="vendor/mathjax/tex-svg.js"]').count()==1
   assert page.evaluate('localStorage.getItem("MathJax-Menu-Settings")')==saved
   assert page.evaluate('MathJax.startup.document.options.safeOptions.allow.URLs')=='none'
   assert page.locator('#tutorial-content mjx-assistive-mml').count()>0
   page.screenshot(path=str(W/('math-menu-'+mode+'.png')),full_page=False)
   page.locator('#tutorial-language').select_option('en');page.wait_for_function('document.querySelector("#tutorial-content").lang==="en" && document.querySelectorAll("#tutorial-content mjx-container").length>100 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
   page.evaluate('location.hash="#tutorial/complexity"');page.wait_for_function('document.querySelector("#tutorial-complexity-0") && document.querySelectorAll("#tutorial-content mjx-container").length>20 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
   page.evaluate('''async()=>{const {renderBlock,typeset}=await import('./tutorials.js?v=100');const e=document.createElement('div');e.id='literal-sample-test';document.body.append(e);for(const language of ['Input','Output'])renderBlock({type:'code',language,text:'$n$\\n1  2\\n'},e,'mn');await typeset([e]);}''')
   assert page.locator('#literal-sample-test mjx-container').count()==0
   assert page.locator('#literal-sample-test code').all_text_contents()==['$n$\n1  2\n']*2
   if mode in ['chtml','combined']:
    page.reload(wait_until='domcontentloaded');page.wait_for_function('document.querySelector("#tutorial-complexity-0") && document.querySelectorAll("#tutorial-content mjx-container").length>20 && document.querySelector("#tutorial-content").getAttribute("aria-busy")==="false"')
   assert not failures,failures;assert not errors,errors
   print('passed '+mode,flush=True);results.append({'mode':mode,'introduction_rendered':209,'preferences_unchanged':True,'native_math_plain_io_navigation':True,'math_requests':sorted(set(requests))});page.close()
  b.close()
finally:s.shutdown()
report={'cases':results,'limits':'Local real Chromium with Pixel7 emulation and current public payloads; not physical Android or authenticated live-browser verification.'}
(W/'mathjax-saved-settings.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
