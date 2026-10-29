import functools,http.server,threading,json
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2]
class Q(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
s=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Q,directory=str(R)));threading.Thread(target=s.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{s.server_port}';results=[]
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for theme in ['light','dark']:
  for width in [375,1200]:
   page=b.new_page(viewport={'width':width,'height':800});page.route('**/*',lambda x:x.abort()if not x.request.url.startswith(base)or'/app.js?'in x.request.url else x.continue_());page.goto(base+'/index.html',wait_until='networkidle')
   result=page.evaluate(r'''async p=>{document.documentElement.dataset.theme=p.theme;const{typeset}=await import('/tutorials.js?v=56');const a=document.createElement('article');a.className='tutorial-content';a.style.width='min(100%, 650px)';document.body.replaceChildren(a);await typeset([a],()=>{const para=document.createElement('p');para.textContent='Номын жишээ $n/2$, $n+5$, $O(n^2)$. '+('$x_1+x_2+'+'x_3+'.repeat(100)+'x_4$');a.append(para);});const boxes=[...a.querySelectorAll('mjx-container')];const first=boxes[0];first.style.width=(first.querySelector('svg').getBoundingClientRect().width+1)+'px';first.style.overflowX='auto';const roundingReproduction={scrollWidth:first.scrollWidth,clientWidth:first.clientWidth};first.style.removeProperty('overflow-x');const{refreshInlineMath}=await import('/tutorial-math-layout.js?v=56');refreshInlineMath([a]);return{roundingReproduction,short:boxes.slice(0,3).map(x=>({overflow:getComputedStyle(x).overflowX,scroll:x.classList.contains('inline-math-scroll')})),wide:{scroll:boxes[3].classList.contains('inline-math-scroll'),scrollWidth:boxes[3].scrollWidth,clientWidth:boxes[3].clientWidth},pageOverflow:document.documentElement.scrollWidth>innerWidth};}''',{'theme':theme})
   assert result['roundingReproduction']['scrollWidth']>result['roundingReproduction']['clientWidth'],result
   assert all(x['overflow']=='visible'and not x['scroll']for x in result['short']),result
   assert result['wide']['scroll']and result['wide']['scrollWidth']>result['wide']['clientWidth']and not result['pageOverflow'],result
   page.evaluate("document.querySelector('article').style.width='10px'");page.wait_for_function("document.querySelector('mjx-container').classList.contains('inline-math-scroll')");page.evaluate("document.querySelector('article').style.width='min(100%,650px)'");page.wait_for_function("!document.querySelector('mjx-container').classList.contains('inline-math-scroll')");result['resize_reclassified']=True
   page.screenshot(path=f'/tmp/math-scroll-{theme}-{width}.png');results.append({'theme':theme,'width':width,**result});page.close()
 b.close()
s.shutdown();(R/'audit/INLINE-MATH-SCROLL.json').write_text(json.dumps({'status':'passed','cases':results},indent=2)+'\n');print(json.dumps(results))
