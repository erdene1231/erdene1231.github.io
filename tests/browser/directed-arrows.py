import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}';cases=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
  p=b.new_page(viewport={'width':1200,'height':900});p.route('**/*',lambda r:r.abort()if not r.request.url.startswith(base)else r.fulfill(status=200,content_type='text/javascript',body='')if '/app.js?'in r.request.url or'/navigation.js?'in r.request.url else r.continue_());p.goto(base+'/index.html',wait_until='networkidle')
  for theme in ['light','dark']:
   for width in [1200,390,800]:
    p.set_viewport_size({'width':width,'height':900})
    if width==1200:
     p.evaluate('''async theme=>{document.documentElement.dataset.theme=theme;document.body.innerHTML='<main style="max-width:820px"><article></article></main>';const{renderExtendedBlock}=await import('/tutorial-block-renderer.js?v=63');renderExtendedBlock({type:'diagram',kind:'graph',directed:true,nodes:[{id:'1',label:'1',x:15,y:20},{id:'2',label:'2',x:85,y:20},{id:'3',label:'3',x:85,y:80},{id:'4',label:'4',x:15,y:80}],edges:[['1','2'],['2','1'],['2','3'],['3','4'],['4','1'],['1','3']],edgeStyles:[{color:'#c2410c'}]},document.querySelector('article'));}''',theme)
    if width==800:p.locator('.diagram-node').nth(1).evaluate("n=>n.textContent='target vertex'")
    p.wait_for_timeout(100)
    out=p.evaluate('''()=>{const g=document.querySelector('.diagram-graph'),svg=g.querySelector('svg'),box=g.getBoundingClientRect(),nodes=[...g.querySelectorAll('.diagram-node')].map(n=>n.getBoundingClientRect()),edges=[[0,1],[1,0],[1,2],[2,3],[3,0],[0,2]];return{polygons:[...g.querySelectorAll('.graph-arrow')].map((p,i)=>{const point=p.points[0],x=box.left+point.x/600*box.width,y=box.top+point.y/320*box.height,target=nodes[edges[i][1]],source=nodes[edges[i][0]],ux=(target.x+target.width/2)-(source.x+source.width/2),uy=(target.y+target.height/2)-(source.y+source.height/2),dx=(x-target.x-target.width/2),dy=(y-target.y-target.height/2);return{outside:x<target.left||x>target.right||y<target.top||y>target.bottom,points:p.points.numberOfItems,toward:dx*ux+dy*uy<0,fill:getComputedStyle(p).fill}}),overflow:document.documentElement.scrollWidth>innerWidth};}''')
    assert len(out['polygons'])==6 and all(x['outside']and x['toward']and x['points']==3 for x in out['polygons'])and not out['overflow'],out
    p.locator('.tutorial-diagram').screenshot(path=f'/tmp/directed-arrows-{width}-{theme}.png');cases.append({'width':width,'theme':theme,**out})
  b.close()
finally:server.shutdown()
(R/'audit/PACKAGE03-DIRECTED-ARROWS.json').write_text(json.dumps({'status':'passed','cases':cases,'scope':'Actual responsive native renderer; visible endpoint polygons outside fixed-size nodes; no data changes'},indent=2)+'\n');print(json.dumps({'cases':len(cases),'status':'passed'}))
