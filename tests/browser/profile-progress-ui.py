"""Actual profile renderer with synthetic public RPC/owner records; no live writes."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as pw:
  browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(viewport={'width':1200,'height':950});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  def route(r):
   u=r.request.url
   if not u.startswith(base):r.abort()
   elif '/app.js?'in u or'/navigation.js?'in u:r.fulfill(status=200,content_type='text/javascript',body='')
   else:r.continue_()
  page.route('**/*',route);page.add_init_script("""const RealDate=Date;window.Date=class extends RealDate{constructor(...a){super(...(a.length?a:['2026-10-31T12:00:00Z']));}static now(){return new RealDate('2026-10-31T12:00:00Z').getTime();}};""");page.goto(base+'/index.html#profile',wait_until='networkidle')
  page.evaluate('''async()=>{
   const{setupLearning}=await import('/learning.js?v=89');window.alice='00000000-0000-0000-0000-000000000001';window.bob='00000000-0000-0000-0000-000000000002';window.privateReads=[];window.writes=0;
   window.ratings=[800,1100,1199,1200,1300,1399,1400,1500,1599,1600,1800,1899,1900,2000,2099,2100,2300,2399,2400,2900,2999,3000,4000];window.problems=ratings.map((rating,i)=>({id:'p'+rating,number:i+1,title:'Rated '+rating,source:'Fixture',ref:String(rating),url:'https://example.com/'+rating,rating,ratingKind:i%2?'estimated':'official',tags:[],priorityLevel:'medium'}));problems.push({id:'prev',title:'Previous week',rating:1000,ratingKind:'estimated',tags:[]},{id:'undated',title:'Undated solved',rating:900,ratingKind:'estimated',tags:[]},{id:'unrated',title:'Unknown rating',rating:null,ratingKind:'unrated',tags:[]},{id:'trying',title:'Trying',rating:1200,ratingKind:'estimated',tags:[]});
   window.progress=Object.fromEntries(problems.map(p=>[p.id,{status:p.id==='trying'?'trying':'solved'}]));progress.archived={status:'solved'};
   window.rows=Object.entries(progress).map(([problem_id,{status}])=>({problem_id,status,first_solved_at:problem_id==='prev'?'2026-10-20T00:00:00Z':problem_id==='undated'||status==='trying'?null:'2026-10-28T00:00:00Z',first_attempted_at:problem_id==='prev'?'2026-10-20T00:00:00Z':problem_id==='undated'?null:'2026-10-27T00:00:00Z'}));
   window.tutorialRecords={legacy:{readSections:[0,1],checks:['purpose'],unknown:'keep'},view:{viewedAt:'2026-10-30T00:00:00Z',viewedDays:['2026-10-20','2026-10-27','2026-10-30']},done:{viewedAt:'2026-10-31T00:00:00Z',viewedDays:['2026-10-31'],completedAt:'2026-10-31T00:00:00Z'},previous:{viewedAt:'2026-10-20T00:00:00Z',viewedDays:['2026-10-20'],completedAt:'2026-10-20T00:00:00Z'}};
   const client={rpc:async(name,args)=>({data:name==='get_learning_profile'?{profile:{user_id:args.p_user_id,full_name:args.p_user_id===alice?'Alice fixture':'Bob fixture'},progress:args.p_user_id===alice?rows:[rows[0]],plan:{completedDays:7}}:[],error:null}),from:()=>({select:()=>({eq:async(_,uid)=>{privateReads.push(uid);return{data:Object.entries(tutorialRecords).map(([key,value])=>({kind:'tutorial',key,value})),error:null};}}),upsert:async()=>{writes++;return{error:null};}})};
   window.learning=await setupLearning({client:()=>client,user:()=>({id:alice}),profile:()=>({full_name:'Alice fixture'}),problems:()=>problems,progress:()=>progress,openProblem:p=>location.hash='#problem/'+p.id});document.getElementById('profile').hidden=false;
  }''')
  page.wait_for_selector('.weekly-highest[href="#problem/p4000"]');panel=page.locator('.weekly-progress')
  def metric(label):return page.evaluate("label=>{const rows=[...document.querySelectorAll('.weekly-metrics>div')],row=rows.find(r=>r.querySelector('dt').textContent===label)||rows.find(r=>r.querySelector('dt').textContent.startsWith(label));return row.querySelector('dd').textContent}",label)
  assert metric('Шинээр оролдсон')=='26';assert metric('Бодсон')=='25';assert metric('Өмнөх 7 хоногоос')=='+24';assert metric('Үзсэн хичээл')=='2';assert metric('Бүрэн уншиж дуусгасан')=='1';assert metric('100 хоног')=='0/100';assert'4000'in metric('Хамгийн өндөр');assert metric('Бодсон бодлогуудын дундаж')==str(round(sum(page.evaluate('ratings'))/23));assert'Огноо тодорхойгүй өмнөх уншилтын тэмдэглэл: 1'in panel.inner_text()
  total=sum(map(int,page.locator('.rating-column-count').all_text_contents()));assert total==25;assert'Rating / metadata тодорхойгүй: 2'in page.locator('.profile-rating-panel').inner_text()
  colors={800:'grey',1100:'grey',1200:'green',1300:'green',1400:'cyan',1500:'cyan',1600:'blue',1800:'blue',1900:'magenta',2000:'magenta',2100:'orange',2300:'orange',2400:'red',2900:'red',3000:'black',4000:'black'}
  for rating,color in colors.items():assert page.locator(f'.rating-column[data-rating="{rating}"]').get_attribute('data-color')==color
  panel.get_by_role('button',name='← Өмнөх 7 хоног').click();assert metric('Бодсон')=='1';assert metric('Үзсэн хичээл')=='2';assert metric('Бүрэн уншиж дуусгасан')=='1';assert panel.locator('.weekly-highest').get_attribute('href')=='#problem/prev';panel.get_by_role('button',name='Дараагийн →').click();assert metric('Бодсон')=='25'
  states=[];out=Path('/workspace/ui-followup/profile-screenshots');out.mkdir(exist_ok=True)
  for width,theme in[(375,'light'),(1200,'light'),(375,'dark'),(1200,'dark')]:
   page.set_viewport_size({'width':width,'height':950});page.evaluate('t=>document.documentElement.dataset.theme=t',theme);assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth'),(width,theme)
   assert page.evaluate("()=>{const e=document.querySelector('.rating-chart-scroll');e.scrollLeft=0;e.focus();return e.scrollWidth>e.clientWidth}");page.locator('.rating-chart-scroll').press('ArrowRight');page.wait_for_timeout(100);assert page.evaluate("document.querySelector('.rating-chart-scroll').scrollLeft>0")
   computed=page.evaluate("""()=>{const e=document.querySelector('.method.home-sections'),other=document.createElement('section');other.className='method';document.body.append(other);const result={surface:getComputedStyle(e).backgroundColor,otherMethod:getComputedStyle(other).backgroundColor,gradient:getComputedStyle(e).backgroundImage,before:getComputedStyle(e,'::before').content,after:getComputedStyle(e,'::after').content};other.remove();return result;}""")
   if theme=='light':assert computed['surface']=='rgb(255, 255, 255)'and computed['otherMethod']=='rgb(248, 250, 252)'
   else:assert computed['surface']=='rgba(0, 0, 0, 0)'
   assert computed['gradient']=='none'and computed['before']==computed['after']=='none'
   black=page.locator('.rating-column[data-rating="3000"] .rating-column-bar');palette=black.evaluate("e=>({fill:getComputedStyle(e).backgroundColor,border:getComputedStyle(e).borderColor,text:getComputedStyle(e.closest('.rating-column')).color})")
   assert palette['fill']==('rgb(5, 5, 5)'if theme=='dark'else'rgb(17, 17, 17)');assert theme!='dark'or palette['border']==palette['text'];computed['black_bar']=palette
   page.evaluate("document.querySelector('.rating-chart-scroll').scrollLeft=99999");page.locator('.profile-rating-panel').screenshot(path=str(out/f'chart-end-{width}-{theme}.png'));page.evaluate("document.querySelector('.rating-chart-scroll').scrollLeft=0")
   states.append({'width':width,'theme':theme,**computed});page.locator('#learning-profile-body').screenshot(path=str(out/f'profile-{width}-{theme}.png'));page.locator('.home-sections').screenshot(path=str(out/f'home-{width}-{theme}.png'))
  page.evaluate("location.hash='#profile/'+bob");page.wait_for_function("document.querySelector('#learning-profile-body h2')?.textContent==='Bob fixture'");assert metric('Үзсэн хичээл')=='Хувийн мэдээлэл';assert metric('Бүрэн уншиж дуусгасан')=='Хувийн мэдээлэл';assert metric('100 хоног')=='7/100';assert page.evaluate('privateReads.every(id=>id===alice)&&writes===0');assert errors==[],errors
  result={'status':'passed','actual_profile_renderer':True,'rating_total_known':25,'rating_unknown':2,'weekly_current_solved':25,'weekly_previous_solved':1,'highest_actual_problem_link':'#problem/p4000','tutorials_viewed_week':2,'tutorials_completed_week':1,'legacy_unknown_dates_not_counted':True,'view_days_preserve_previous_week_after_revisit':True,'challenge_cumulative_rule_count':'0/100; public other profile7/100','other_profile_tutorial_dates_private':True,'owner_records_never_requested_for_other_user':True,'writes':0,'light_home_before':'rgb(248, 250, 252)','states':states,'limitations':'Synthetic public RPC/owner records; actual renderer/CSS. No live-user writes or new access.'};(ROOT/'audit/ui-followup/profile-progress-browser.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));browser.close()
finally:server.shutdown()
