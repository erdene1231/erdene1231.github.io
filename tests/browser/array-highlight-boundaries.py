"""Collapsed-border regression through native diagram authoring and reader rendering."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';cases=[]
with sync_playwright()as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for theme in ['light','dark']:
  for width in [375,1000]:
   page=browser.new_page(viewport={'width':width,'height':700},device_scale_factor=1)
   page.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)or'/app.js?'in r.request.url else r.continue_());page.goto(base+'/index.html',wait_until='networkidle')
   for keys in [['0:2'],['0:1','0:2','0:3'],['0:0','0:1'],['0:4','0:5'],['0:0','0:2','0:3','0:5'],['0:1','1:1','1:2']]:
    result=page.evaluate('''async p=>{const{renderExtendedBlock}=await import('/tutorial-block-renderer.js?v=54'),{mountBlockEditor}=await import('/tutorial-block-editor.js');document.documentElement.dataset.theme=p.theme;document.body.replaceChildren();const editor=document.createElement('div');document.body.append(editor);const diagram={type:'diagram',kind:p.keys.some(k=>k.startsWith('1:'))?'dp':'array',rows:[['-4','5','-1','3','-8','6'],['1','2','3','4','5','6']],highlights:[],caption:'Native saved diagram'};let sections=[{key:'array',title:'Array',blocks:[diagram]}];const mounted=mountBlockEditor(editor,sections,{changed:()=>{},locked:()=>false});editor.querySelector('details').open=true;await new Promise(r=>setTimeout(r,30));const field=[...editor.querySelectorAll('label')].find(x=>x.textContent.startsWith('Тодруулах ID'))?.querySelector('input');if(!field)throw Error('Highlight input missing');field.value=p.keys.join(', ');field.dispatchEvent(new Event('input',{bubbles:true}));const saved=JSON.stringify(sections);mounted.destroy();sections=JSON.parse(saved);if(JSON.stringify(sections[0].blocks[0].highlights)!==JSON.stringify(p.keys))throw Error('Selection not saved');const reload=mountBlockEditor(editor,sections,{changed:()=>{},locked:()=>false});reload.destroy();editor.remove();const article=document.createElement('article');article.className='tutorial-content';document.body.append(article);renderExtendedBlock(sections[0].blocks[0],article);const table=article.querySelector('table'),cells=[...table.rows].map(r=>[...r.cells]),high=new Set(p.keys),green=getComputedStyle(cells[0][0]).getPropertyValue('--green').trim();const ref=document.createElement('span');ref.style.color=green;article.append(ref);const expected=getComputedStyle(ref).color;ref.remove();const edges=[];for(let i=0;i<cells.length;i++)for(let j=0;j<cells[i].length;j++){const c=cells[i][j],s=getComputedStyle(c),r=c.getBoundingClientRect();for(const[side,di,dj]of[['left',0,-1],['right',0,1],['top',-1,0],['bottom',1,0]])if(high.has(i+':'+j)||high.has((i+di)+':'+(j+dj))){const cap=side[0].toUpperCase()+side.slice(1);if(s['border'+cap+'Color']!==expected||s['border'+cap+'Width']!=='1px')throw Error('Boundary mismatch '+i+':'+j+' '+side);if(high.has(i+':'+j))edges.push({side,x:side==='left'?r.left:side==='right'?r.right:r.left+r.width/2,y:side==='top'?r.top:side==='bottom'?r.bottom:r.top+r.height/2});}}return{theme:p.theme,width:p.width,keys:p.keys,green:expected,highlightBackground:getComputedStyle(cells[Number(p.keys[0].split(':')[0])][Number(p.keys[0].split(':')[1])]).backgroundColor,edges,roundtrip:true,collapse:getComputedStyle(table).borderCollapse,overflow:document.documentElement.scrollWidth>innerWidth};}''',{'keys':keys,'theme':theme,'width':width})
    assert not result['overflow'] and result['collapse']=='collapse',result
    path='/tmp/array-boundaries-after.png';page.screenshot(path=path);im=Image.open(path).convert('RGB');rgb=tuple(map(int,result['green'][4:-1].split(',')))
    def lum(rgb):
     v=[c/255 for c in rgb];v=[c/12.92 if c<=0.04045 else((c+0.055)/1.055)**2.4 for c in v];return sum(a*b for a,b in zip(v,[0.2126,0.7152,0.0722]))
    bg=tuple(map(int,result['highlightBackground'][4:-1].split(',')));a,b=sorted([lum(rgb),lum(bg)]);result['boundaryContrast']=(b+0.05)/(a+0.05);assert result['boundaryContrast']>=3,result
    for e in result['edges']:
     x,y=round(e['x']),round(e['y']);pixels=[im.getpixel((a,b))for a in range(max(0,x-1),min(im.width,x+2))for b in range(max(0,y-1),min(im.height,y+2))];assert rgb in pixels,(result,e,pixels)
    cases.append({k:v for k,v in result.items()if k!='edges'})
   page.close()
 browser.close()
server.shutdown();report={'status':'passed','cases':cases,'pixel_edges_verified':True,'native_edit_serialize_reload':True,'production_content_writes':0};(ROOT/'audit/ARRAY-HIGHLIGHT-BOUNDARIES.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','cases':len(cases)}))
