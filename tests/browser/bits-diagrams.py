import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];doc=json.loads((ROOT/'audit/package03-lessons/bit-operations.json').read_text())['body']
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';results=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,theme in [(1200,'light'),(1200,'dark'),(390,'light'),(390,'dark')]:
   page=b.new_page(viewport={'width':width,'height':900});page.route('**/*',lambda r:r.abort() if not r.request.url.startswith(base) else r.fulfill(status=200,content_type='text/javascript',body='') if '/app.js?'in r.request.url or '/navigation.js?'in r.request.url else r.continue_());page.goto(base+'/index.html',wait_until='networkidle')
   result=page.evaluate('''async p=>{const{drawArticle,typeset}=await import('/tutorials.js?v=61');document.documentElement.dataset.theme=p.theme;document.body.innerHTML='<main style="max-width:850px;padding:16px"><article class="tutorial-content"></article></main>';const root=document.querySelector('article');await typeset([root],()=>drawArticle(p.doc,root,'mn'));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));let collisions=0;for(const graph of root.querySelectorAll('.diagram-graph')){const nodes=[...graph.querySelectorAll('.diagram-node')].map(n=>n.getBoundingClientRect());for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++)if(nodes[i].left<nodes[j].right&&nodes[j].left<nodes[i].right&&nodes[i].top<nodes[j].bottom&&nodes[j].top<nodes[i].bottom)collisions++;}return {graphs:root.querySelectorAll('.diagram-graph').length,gridCells:root.querySelectorAll('.grid-presented td').length,mathErrors:root.querySelectorAll('mjx-merror,[data-mjx-error]').length,collisions,overflow:document.documentElement.scrollWidth>innerWidth};}''',{'doc':doc,'theme':theme})
   assert result['graphs']==0 and result['gridCells']==123 and result['mathErrors']==0 and result['collisions']==0 and not result['overflow'],result
   page.locator('.tutorial-diagram').filter(has=page.locator('.grid-presented')).first.screenshot(path=f'/tmp/bits-grid-{width}-{theme}.png')
   page.locator('.tutorial-diagram').filter(has=page.locator('.grid-presented')).nth(4).screenshot(path=f'/tmp/bits-price-{width}-{theme}.png')
   results.append({'width':width,'theme':theme,**result});page.close()
  b.close()
finally:server.shutdown()
report={'status':'passed','local_native_diagrams':results,'scope':'Actual native renderer; no live writes or certificate bypass'};(ROOT/'audit/PACKAGE03-BITS-DIAGRAMS.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
