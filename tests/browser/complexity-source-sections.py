"""All four source-section links in the actual native reader, including mobile anchors."""
import functools,http.server,json,threading,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];d=json.loads((ROOT/'audit/package03-lessons/complexity.json').read_text())['body'];rows=[x for x in json.loads((ROOT/'audit/PART04-BASELINE.json').read_text())['tutorials']if x['id']!='mongolia']
for row in rows:
 if row['id']=='complexity':row['body']=d
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';cases=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for width,theme in [(393,'light'),(1200,'dark')]:
  page=b.new_page(viewport={'width':width,'height':950},is_mobile=width<600,has_touch=width<600)
  page.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if'/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_());page.goto(base+'/index.html#tutorial/complexity',wait_until='networkidle')
  page.evaluate('''async p=>{const{setupTutorials}=await import('/tutorials.js?v=54');document.documentElement.dataset.theme=p.theme;const section=document.getElementById('tutorial-reader').closest('section');for(const e of document.querySelectorAll('main>section'))e.hidden=e!==section;window.app=setupTutorials({client:()=>({rpc:async name=>{if(name==='get_tutorials')return{data:p.rows};throw Error(name)}}),user:()=>null,learning:()=>null,isAdmin:()=>false});await app.connected();}''',{'rows':rows,'theme':theme})
  for lang in ['mn','en']:
   page.select_option('#tutorial-language',lang);page.wait_for_function("l=>document.getElementById('tutorial-content').lang===l&&document.getElementById('tutorial-content').getAttribute('aria-busy')==='false'",arg=lang)
   for i in range(len(d['sections'])):
    panel=page.locator('#tutorial-contents-panel')
    if not panel.evaluate('(e)=>e.open'):panel.locator('summary').click()
    page.locator('#tutorial-toc a').nth(i).click();page.wait_for_function("i=>location.hash.endsWith('/part/'+i)",arg=i);page.wait_for_timeout(120)
    result=page.evaluate('''i=>{const target=document.getElementById('tutorial-complexity-'+i);return{target:target.id,top:target.getBoundingClientRect().top,title:target.querySelector('h2,h3').textContent,tocCount:document.querySelectorAll('#tutorial-toc a').length,errors:document.querySelectorAll('#tutorial-content mjx-merror,[data-mjx-error]').length,pageOverflow:document.documentElement.scrollWidth>innerWidth,mobileContentsClosed:!document.getElementById('tutorial-contents-panel').open};}''',i)
    assert result['tocCount']==len(d['sections']) and result['errors']==0 and not result['pageOverflow'],result
    assert -5<=result['top']<250,result
    if width<600:assert result['mobileContentsClosed'],result
    if lang=='mn':page.screenshot(path=f'/tmp/complexity-chapter2-{width}-{i}.png')
    cases.append({'lang':lang,'width':width,'section':i,**result})
  b.close()if False else page.close()
 b.close()
server.shutdown();(ROOT/'audit/PACKAGE03-COMPLEXITY-TOC-BROWSER.json').write_text(json.dumps({'status':'passed','cases':cases,'nested_tutorial_feature':False,'production_writes':0},indent=2)+'\n');print(json.dumps({'status':'passed','anchor_cases':len(cases)}))
