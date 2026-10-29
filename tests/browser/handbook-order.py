import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
rows=[r for r in json.loads((ROOT/'audit/PART04-BASELINE.json').read_text())['tutorials']if r['id']!='mongolia']
for id in ['introduction','scc','paths-circuits','flows-cuts','number-theory','matrices','probability','game-theory','sqrt-algorithms']:
 b=json.loads((ROOT/f'audit/package03-lessons/{id}.json').read_text())['body'];rows=[r for r in rows if r['id']!=id]+[{'id':id,'body':b,'revision':1}]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';results=[]
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width,theme in [(390,'light'),(1200,'dark')]:
   p=browser.new_page(viewport={'width':width,'height':900});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
   p.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if '/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_())
   p.goto(base+'/index.html#tutorials',wait_until='networkidle')
   p.evaluate('''async ({rows,theme})=>{const{setupTutorials}=await import('/tutorials.js?v=67');for(const e of document.querySelectorAll('main>section'))e.hidden=e.id!=='tutorials';document.documentElement.dataset.theme=theme;window.a=setupTutorials({client:()=>({rpc:async n=>{if(n==='get_tutorials')return{data:rows};throw Error(n)}}),user:()=>null,isAdmin:()=>false,learning:()=>null});await a.connected();}''',{'rows':rows,'theme':theme})
   p.wait_for_function('n=>document.querySelectorAll("#tutorial-grid .tutorial-card").length===n',arg=len(rows))
   r=p.evaluate('''async()=>{const{orderTutorials,handbookChapterNumbers}=await import('/tutorial-order.js?v=67');const ids=[...document.querySelectorAll('#tutorial-grid .tutorial-card')].map(e=>e.hash.split('/')[1]);const expected=orderTutorials(ids.map(id=>({id}))).map(t=>t.id);if(JSON.stringify(ids)!==JSON.stringify(expected))throw Error('Visible order mismatch');for(const e of document.querySelectorAll('#tutorial-grid .tutorial-card')){const id=e.hash.split('/')[1],h=e.querySelector('h4').textContent,n=handbookChapterNumbers[id];if(n?!h.startsWith(n+'. '):!h.startsWith('Нэмэлт · '))throw Error('Chapter/supplement numbering mismatch '+id);}return{ids,numbering:true,overflow:document.documentElement.scrollWidth>innerWidth}}''')
   assert r['ids'][:2]==['introduction','complexity'] and not r['overflow']
   p.locator('#tutorial-priority-sort').select_option('priority');p.wait_for_timeout(150)
   assert p.locator('#tutorial-grid .tutorial-level-heading').inner_text()=='Ач холбогдлоор'
   assert p.evaluate("()=>{const a=[...document.querySelectorAll('#tutorial-grid .priority-badge')].map(e=>e.classList.contains('priority-high')?2:e.classList.contains('priority-medium')?1:0);return a.every((x,i)=>i===0||x<=a[i-1])}")
   p.locator('#tutorial-priority-sort').select_option('');p.locator('#tutorial-priority-filter').select_option('high');p.wait_for_timeout(150)
   assert p.locator('#tutorial-grid .tutorial-card').count()>0 and p.locator('#tutorial-grid .priority-badge:not(.priority-high)').count()==0
   p.locator('#tutorial-priority-filter').select_option('');p.wait_for_timeout(150)
   p.screenshot(path=f'/tmp/handbook-order-{width}.png');assert not errors,errors
   results.append({'width':width,'theme':theme,'visible_lessons':len(rows),'default_exact_order':r['ids'],'source_chapter_numbers_and_unnumbered_supplements':True,'explicit_priority_sort_and_filter':True,'no_document_overflow':True});p.close()
  browser.close()
finally:server.shutdown()
(ROOT/'audit/PACKAGE03-HANDBOOK-ORDER-BROWSER.json').write_text(json.dumps({'status':'passed','cases':results,'scope':'Native listing with all 60 published lesson identities; local readonly fixtures, no production writes'},indent=2)+'\n');print('Native handbook order, numbering and explicit priority controls passed')
