"""Actual tutorial-library acknowledgement in both languages/themes, local read-only fixtures."""
import functools,http.server,json,subprocess,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];rows=json.loads((ROOT/'audit/PART04-BASELINE.json').read_text())['tutorials'];candidate=json.loads((ROOT/'audit/package03-lessons/complexity.json').read_text())['body']
for r in rows:
 if r['id']=='complexity':r['body']=candidate
rows=[r for r in rows if r['published']];problems=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import{proposalProblems}from'./tools/package02_tutorial_proposals.mjs';console.log(JSON.stringify(proposalProblems()))"],cwd=ROOT,text=True))
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';cases=[]
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  for width in [375,1200]:
   for theme in ['light','dark']:
    page=browser.new_page(viewport={'width':width,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if'/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_());page.goto(base+'/index.html#tutorials',wait_until='networkidle')
    page.evaluate('''async p=>{document.documentElement.dataset.theme=p.theme;for(const s of document.querySelectorAll('main>section'))s.hidden=s.id!=='tutorials';const{setupTutorials}=await import('/tutorials.js?v=53');window.app=setupTutorials({client:()=>({rpc:async name=>{if(name==='get_tutorials')return{data:p.rows};throw Error(name)}}),user:()=>null,learning:()=>null,isAdmin:()=>false});await app.connected();}''',{'rows':rows,'theme':theme})
    for lang in ['mn','en']:
     page.select_option('#tutorial-language',lang);page.wait_for_function("p=>document.getElementById('tutorial-source-credit').textContent.includes(p==='mn'?'үе шаттай':'being revised')",arg=lang)
     result=page.evaluate('''()=>{const e=document.getElementById('tutorial-source-credit'),a=e.querySelector('a');const lum=s=>{const v=s.match(/[0-9.]+/g).slice(0,3).map(Number).map(v=>v/255).map(v=>v<=0.04045?v/12.92:((v+0.055)/1.055)**2.4);return .2126*v[0]+.7152*v[1]+.0722*v[2]};const bg=lum(getComputedStyle(document.body).backgroundColor),contrast=x=>{const c=lum(getComputedStyle(x).color);return(Math.max(c,bg)+.05)/(Math.min(c,bg)+.05)};return{count:document.querySelectorAll('#tutorial-source-credit').length,text:e.textContent,href:a.href,rel:a.rel,contrast:contrast(e),linkContrast:contrast(a),overflow:document.documentElement.scrollWidth>innerWidth}}''')
     assert result['count']==1 and result['href']=='https://cses.fi/book/index.php'and'noopener'in result['rel'];assert result['contrast']>=4.5 and result['linkContrast']>=4.5,result;assert not result['overflow'],result;assert'Antti Laaksonen'in result['text'];cases.append({'width':width,'theme':theme,'language':lang,**result})
    assert not errors,errors;page.screenshot(path=f'/tmp/p03-credit-{width}-{theme}.png');page.close()
  browser.close()
finally:server.shutdown()
(ROOT/'audit/PACKAGE03-HANDBOOK-CREDIT-BROWSER.json').write_text(json.dumps({'status':'passed','cases':cases,'network':'Local fixtures only; official book link previously verified by web read; no user-data requests'},indent=2)+'\n');print(json.dumps({'status':'passed','cases':len(cases)}))
