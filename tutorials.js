import {orderTutorials,handbookChapterNumbers} from './tutorial-order.js?v=76';
import {renderGridRows,prepareGridTable} from './tutorial-grid.js?v=62';
import {refreshInlineMath} from './tutorial-math-layout.js?v=56';
import {priorityLevel,priorityLabel,priorityRank} from './priority.js?v=52';
import {renderExtendedBlock} from './tutorial-block-renderer.js?v=63';
import {clearMediaCache} from './tutorial-media.js?v=63';
import {loadLearningContent,bodyHash} from './learning-model.js?v=76';
import {algorithmDemo} from './algorithm-demos.js?v=52';
import {segmentTreeDemo} from './segment-tree-demo.js?v=52';
import {levels,levelNames,validateTutorial,view} from './tutorial-model.js?v=63';
import {setupTutorialEditor} from './tutorial-editor.js?v=76';
const $=id=>document.getElementById(id);
export const node=(tag,text,cls)=>{const el=document.createElement(tag);if(text!==undefined)el.textContent=text;if(cls)el.className=cls;return el;};
let mathPromise=null,mathQueue=Promise.resolve();
function mathjax(){
 if(window.MathJax?.typesetPromise)return Promise.resolve(window.MathJax);
 if(mathPromise)return mathPromise;
 mathPromise=new Promise((resolve,reject)=>{
  window.MathJax={loader:{paths:{mathjax:new URL('./vendor/mathjax',location.href).href},load:['ui/safe']},options:{safeOptions:{allow:{URLs:'none',classes:'none',cssIDs:'none',styles:'none'}}},tex:{packages:['base','ams','newcommand','noundefined','configmacros'],inlineMath:[['\\(','\\)'],['$','$']],displayMath:[['\\[','\\]'],['$$','$$']],processEscapes:true,maxBuffer:20000},svg:{fontCache:'local'},startup:{typeset:false}};
  const script=document.createElement('script');script.src='./vendor/mathjax/tex-svg.js';script.async=true;
  const timer=setTimeout(fail,15000);
  function fail(){clearTimeout(timer);script.remove();mathPromise=null;reject(new Error('MathJax ачаалсангүй / Could not load MathJax.'));}
  script.onerror=fail;script.onload=()=>{clearTimeout(timer);if(!window.MathJax?.startup?.promise)return fail();window.MathJax.startup.promise.then(()=>resolve(window.MathJax)).catch(fail);};document.head.append(script);
 });return mathPromise;
}
export function renderBlock(b,parent,lang='mn',options={}){
 if(renderExtendedBlock(b,parent,lang,options))return;
 if(b.type==='p')parent.append(node('p',b.text));
 else if(b.type==='note'){const a=node(b.collapsible?'details':'aside',undefined,'tutorial-note'+(b.collapsible?' tutorial-disclosure':''));if(b.collapsible)a.append(node('summary',b.label||(lang==='en'?'Show explanation':'Тайлбар харах')));a.append(node('p',b.text));parent.append(a);}
 else if(b.type==='math')parent.append(node('div','$$'+b.tex+'$$','tutorial-math'));
 else if(b.type==='list'||b.type==='ordered'){const list=node(b.type==='list'?'ul':'ol');for(const x of b.items)list.append(node('li',x));parent.append(list);}
 else if(b.type==='table'){const wrap=node('div',undefined,'tutorial-table-wrap'),table=node('table'),head=node('thead'),row=node('tr');for(const h of b.headers){const th=node('th',h);th.scope='col';row.append(th);}head.append(row);table.append(head);const body=node('tbody');if(b.gridPresentation!==undefined){prepareGridTable(table,b);renderGridRows(body,b);}else for(const cells of b.rows){const tr=node('tr');for(const c of cells)tr.append(node('td',c));body.append(tr);}table.append(body);wrap.append(table);parent.append(wrap);}
 else if(b.type==='code'&&['Input','Output'].includes(b.language))renderSample(b,parent,lang);
 else if(b.type==='code'){const cpp=!b.language||['C++17','cpp','C++'].includes(b.language),wrap=node('div',undefined,'tutorial-code'),bar=node('div',undefined,'code-toolbar'),pre=node('pre'),code=node('code',b.text||'',cpp?'language-cpp':'language-plaintext'),button=node('button',lang==='en'?(cpp?'Copy code':'Copy'):(cpp?'Код хуулах':'Хуулах'));button.type='button';button.onclick=()=>void copy(b.text||'',button,lang==='en'?'Copied':'Хуулагдлаа');bar.append(node('span',cpp?'C++17':b.language||'Text'),button);pre.append(code);wrap.append(bar,pre);parent.append(wrap);if(cpp)try{window.hljs?.highlightElement(code);}catch{/* Plain code remains readable. */}}
 else if(b.type==='links'){const list=node('ul',undefined,'tutorial-reading-links');for(const x of b.items){let u;try{u=new URL(x.url);}catch{continue;}if(u.protocol!=='https:'||u.username||u.password)continue;const li=node('li'),a=node('a',x.label);a.href=u.href;a.target='_blank';a.rel='noopener noreferrer';li.append(a);list.append(li);}parent.append(list);}
 else parent.append(node('aside',lang==='en'?'Unsupported block; editor review required.':'Дэмжигдээгүй block: editor дээр шалгана уу.','tutorial-note'));
}
function renderSample(b,parent,lang){
 const english=lang==='en',input=b.language==='Input',panel=node('figure',undefined,'tutorial-sample-panel sample-'+(input?'input':'output'));
 const bar=node('figcaption',undefined,'sample-toolbar'),label=node('span',undefined,'sample-label'),dot=node('span',undefined,'sample-dot');dot.setAttribute('aria-hidden','true');
 label.append(dot,node('strong',b.language));if(!english)label.append(node('span',input?'Оролт':'Гаралт','sample-label-local'));
 const button=node('button',english?'Copy':'Хуулах','sample-copy');button.type='button';button.setAttribute('aria-label',english?'Copy '+b.language:b.language+' хуулах');
 const status=node('span',undefined,'sample-copy-status');status.setAttribute('role','status');
 let reset;button.onclick=async()=>{clearTimeout(reset);try{await navigator.clipboard.writeText(b.text);button.textContent=english?'Copied':'Хуулагдлаа';status.textContent=english?b.language+' copied.':b.language+' хуулагдлаа.';reset=setTimeout(()=>{button.textContent=english?'Copy':'Хуулах';status.textContent='';},1800);}catch{button.textContent=english?'Copy':'Хуулах';status.textContent=english?'Copy unavailable. Select the sample text to copy it.':'Хуулах боломжгүй байна. Жишээний текстийг сонгон хуулна уу.';}};
 const pre=node('pre'),code=node('code',b.text||'','language-plaintext');pre.tabIndex=0;pre.setAttribute('aria-label',english?b.language+' sample':b.language+' жишээ');pre.append(code);
 bar.append(label,button);panel.append(bar,pre,status);parent.append(panel);
}
export function drawArticle(t,parent,lang,options={}){const v=view(t,lang);parent.replaceChildren();for(const [i,s] of v.sections.entries()){
 const draw=(b,target)=>{if(!options.draftPreview){renderBlock(b,target,lang,options);return;}try{renderBlock(b,target,lang,options);}catch{target.append(node('aside','Дутуу '+(b?.type||'block')+' — editor дээр бөглөнө үү.','tutorial-note'));}};
 const part=node('section');part.id='tutorial-'+t.id+'-'+i;if(s.title?.trim())part.append(node('h3',s.title));
 for(let j=0;j<s.blocks.length;j++){
  const b=s.blocks[j],next=s.blocks[j+1];
  if(b?.type==='code'&&b.language==='Input'&&next?.type==='code'&&next.language==='Output'){
   const pair=node('div',undefined,'tutorial-samples');pair.setAttribute('role','group');pair.setAttribute('aria-label',lang==='en'?'Sample input and output':'Жишээ оролт ба гаралт');draw(b,pair);draw(next,pair);part.append(pair);j++;
  }else draw(b,part);
 }
 if(t.id==='segment-tree'&&i===3)part.append(segmentTreeDemo(lang,typeset));if(i===3&&t.automaticDemo!==false){const demo=algorithmDemo(t.id,lang,typeset);if(demo)part.append(demo);}parent.append(part);
}}
export function typeset(elements,build,valid=()=>true){
 mathQueue=mathQueue.catch(()=>{}).then(async()=>{if(!valid())return;window.MathJax?.typesetClear?.(elements);if(build&&build()===false)return;const mj=await mathjax();if(!valid())return;await mj.typesetPromise(elements);if(!valid())mj.typesetClear?.(elements);else refreshInlineMath(elements);});return mathQueue;
}
async function copy(text,button,success){try{await navigator.clipboard.writeText(text);const previous=button.textContent;button.textContent=success;setTimeout(()=>button.textContent=previous,1800);}catch{$('tutorial-message').textContent='Хуулах боломжгүй байна / Copy unavailable.';}}
export function setupTutorials(ctx){
 const requiresOnline=ctx.requiresOnline??!!ctx.client();
 const lessonSeed=fetch('./tutorials.json?v=24').then(r=>{if(!r.ok)throw new Error('Tutorials ачаалсангүй.');return r.json();}).then(d=>d.tutorials),contentReady=Promise.all([loadLearningContent().catch(()=>({curriculum:{order:[]},editions:{editions:{}}})),lessonSeed]);let acceptTurn=0;

 let topics=[],current=null,renderTurn=0,resultTurn=0,loadTurn=0,lang='mn',readingMode='full',activePart=0,requestedPart,onlineReady=false,hasLive=false,editor,mediaAccountId=ctx.user()?.id||null;
 try{lang=localStorage.getItem('erdene:tutorial-language')==='en'?'en':'mn';}catch{}$('tutorial-language').value=lang;
 try{readingMode=localStorage.getItem('erdene:tutorial-reading-mode')==='step'?'step':'full';}catch{}$('tutorial-reading-mode').value=readingMode;
 const tr=(mn,en)=>lang==='en'?en:mn;
 // Compact and touch readers use an explicitly collapsible contents panel.
 const tocPanel=node('details',undefined,'tutorial-contents'),tocSummary=node('summary');
 tocPanel.id='tutorial-contents-panel';$('tutorial-toc').before(tocPanel);tocPanel.append(tocSummary,$('tutorial-toc'));
 const compactContents=matchMedia('(max-width:900px), (hover:none) and (pointer:coarse)');
 let contentsCompact=compactContents.matches;tocPanel.open=!contentsCompact;
 compactContents.addEventListener('change',event=>{if(event.matches===contentsCompact)return;contentsCompact=event.matches;tocPanel.open=!contentsCompact;});
 $('tutorial-toc').addEventListener('click',event=>{if(contentsCompact&&event.target.closest('a'))tocPanel.open=false;});
 const categories={'Суурь':'Fundamentals','Array ба search':'Arrays & searching'};
 const categoryMN={'Array ба search':'Дараалал ба хайлт','DP':'Динамик програмчлал'};
 const categoryName=c=>lang==='en'?(categories[c]||c):(categoryMN[c]||c);
 const priorityName=(t,selected=lang)=>selected==='en'?priorityLabel(t):'Ач холбогдол: '+({low:'бага',medium:'дунд',high:'өндөр'}[priorityLevel(t)]);
 const labels=()=>{const credit=$('tutorial-source-credit');if(credit){const book=node('a',"Competitive Programmer’s Handbook");book.href='https://cses.fi/book/index.php';book.target='_blank';book.rel='noopener noreferrer';const license=node('a','CC BY-NC-SA 4.0');license.href='https://creativecommons.org/licenses/by-nc-sa/4.0/';license.target='_blank';license.rel='noopener noreferrer';credit.replaceChildren(document.createTextNode(tr('Хичээлүүдийг Antti Laaksonen-ийн ','Tutorials are being revised using Antti Laaksonen’s ')),book,document.createTextNode(tr(' номыг жишиг болгон үе шаттай шинэчилж байна. Түүнд тулгуурласан MN/EN найруулга, жишээнүүд ',' as a benchmark. Adapted MN/EN prose and examples are under ')),license,document.createTextNode(tr(' нөхцөлтэй. Кодын тайлбар, дасгалууд нэмсэн; албан ёсны орчуулга биш.','; code walkthroughs and practice have been added. Not an official translation.')));} $('tutorial-learning-guide').replaceChildren(node('strong',tr('Хаанаас эхлэх вэ?','Where should I start?')),node('p',tr('Шинээр эхэлж байгаа бол Анхан шатны хичээлүүдийг дугаараар нь үз. Жишээг гараар дагаж, кодоо уншаад, бүтэн программыг ажиллуул. Санамж нээхээс өмнө дасгалаа өөрөө оролд. Урт хичээлийг “Хэсэг хэсгээр” горимоор уншиж болно. Дунд, ахисан шатанд орохын өмнө урьдчилсан хичээлүүдээ шалга.','Start with the Beginner lessons in numbered order. Trace the example, read the code and run the complete program. Try the exercises before opening hints. Use section-by-section mode for a long lesson. Check prerequisites before moving to Intermediate or Advanced.')));for(const o of $('tutorial-category').options)o.textContent=o.value?categoryName(o.value):tr('Бүх бүлэг','All categories');document.documentElement.lang=location.hash.startsWith('#tutorial')?lang:'mn';$('tutorial-copy-link').textContent=tr('Холбоос хуулах','Copy link');$('tutorial-search').placeholder=tr('Хоёртын хайлт, динамик програмчлал, мод…','Binary search, dp, tree, shortest path…');$('tutorial-reading-label').textContent=tr('Унших горим','Reading mode');$('tutorial-reading-mode').options[0].textContent=tr('Бүтэн хичээл','Full lesson');$('tutorial-reading-mode').options[1].textContent=tr('Хэсэг хэсгээр','Section by section');$('tutorial-section-prev').textContent=tr('← Өмнөх хэсэг','← Previous section');$('tutorial-section-next').textContent=tr('Дараагийн хэсэг →','Next section →');tocSummary.textContent=tr('Хичээлийн агуулга','Lesson contents');$('tutorial-toc').setAttribute('aria-label',tr('Хичээлийн агуулга','Lesson contents'));$('tutorial-section-nav').setAttribute('aria-label',tr('Хэсгийн дараалал','Section navigation'));document.querySelectorAll('.tutorial-back').forEach(a=>a.textContent=tr('← Бүх хичээл','← All tutorials'));};
 function reading(part,scroll=false){
  if(!current)return;const sections=[...$('tutorial-content').children],count=sections.length;if(!count){activePart=0;$('tutorial-section-nav').hidden=true;$('tutorial-toc').hidden=true;tocPanel.hidden=true;readButton.disabled=true;$('tutorial-section-position').textContent='';return;}$('tutorial-toc').hidden=false;tocPanel.hidden=false;
  activePart=Number.isInteger(part)&&part>=0&&part<count?part:0;readButton.disabled=!ctx.learning();readButton.textContent=tr('Энэ хэсгийг уншсан','Mark section read');
  sections.forEach((section,i)=>section.hidden=readingMode==='step'&&i!==activePart);
  $('tutorial-section-nav').hidden=readingMode!=='step';$('tutorial-section-prev').disabled=activePart===0;$('tutorial-section-next').disabled=activePart===count-1;
  const readCount=(ctx.learning()?.lessonRecord(current.id).readSections||[]).filter(i=>Number.isInteger(i)&&i>=0&&i<count).length;$('tutorial-section-position').textContent=tr('Хэсэг ','Section ')+(activePart+1)+' / '+count+' · '+tr('Уншсан ','Read ')+readCount+'/'+count;
  [...$('tutorial-toc').querySelectorAll('a')].forEach((a,i)=>{if(i===activePart)a.setAttribute('aria-current','step');else a.removeAttribute('aria-current');});
  if(scroll){const target=sections[activePart];target.scrollIntoView({block:'start',behavior:'instant'});const heading=target.querySelector('h3');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}}
 }
 const readButton=node('button',tr('Энэ хэсгийг уншсан','Mark section read'));readButton.type='button';readButton.dataset.readCurrent='true';readButton.onclick=()=>{if(!current||!ctx.learning())return;const previous=ctx.learning().lessonRecord(current.id);ctx.learning().store.set('tutorial',current.id,{...previous,readSections:[...new Set([...(previous.readSections||[]),activePart])]});reading(activePart);};$('tutorial-section-nav').append(readButton);
 function goPart(part){if(!current)return;const hash='#tutorial/'+current.id+'/part/'+part;if(location.hash===hash)reading(part,true);else location.hash=hash;}
 function learningLinks(t,selectedLang){
  const isEn=selectedLang==='en',pre=$('tutorial-prerequisite-links'),nav=$('tutorial-lesson-navigation');pre.replaceChildren();nav.replaceChildren();
  const prerequisites=(t.prerequisiteIds||[]).map(id=>topics.find(x=>x.id===id)).filter(Boolean);
  if(prerequisites.length){pre.append(node('strong',isEn?'Read these first:':'Эхлээд эдгээрийг уншаарай:'));for(const p of prerequisites){const a=node('a',view(p,selectedLang).title);a.href='#tutorial/'+p.id;pre.append(a);}}
  const index=topics.findIndex(x=>x.id===t.id);
  for(const [offset,label] of [[-1,isEn?'← Previous lesson: ':'← Өмнөх хичээл: '],[1,isEn?'Next lesson: ':'Дараагийн хичээл: ']]){const next=offset===1&&ctx.learning()?.relationsFor(t.id)?.next?topics.find(x=>x.id===ctx.learning().relationsFor(t.id).next):topics[index+offset];if(next){const a=node('a',label+view(next,selectedLang).title);a.href='#tutorial/'+next.id;nav.append(a);}}
 }
 async function accept(list,authoritative=false){const turn=++acceptTurn,[content,seed]=await contentReady;
  const rows=list.map(x=>x.body?x:{body:x,revision:0}),ids=new Set(rows.map(x=>x.body.id));for(const body of seed)if(!authoritative&&!ids.has(body.id))rows.push({body,revision:0});
  const valid=await Promise.all(rows.map(async row=>{let body=row.body;const edition=content.editions.editions[body.id];if(edition&&body.contentEdition!==edition.body.contentEdition){try{if(edition.baseHashes.includes(await bodyHash(body)))body=edition.body;}catch{}}
   try{const t=validateTutorial(body);return {...t,revision:row.revision||0,searchText:JSON.stringify(t).toLowerCase()};}catch{return null;}
  }));if(turn!==acceptTurn)return;const input=valid.filter(Boolean);if(!input.length&&!authoritative)throw new Error('Published tutorial олдсонгүй.');
  topics=orderTutorials(input,content.curriculum.order);ctx.learning()?.setTopics(topics);
  const old=$('tutorial-category').value,all=node('option',tr('Бүх бүлэг','All categories'));all.value='';$('tutorial-category').replaceChildren(all);for(const c of new Set(topics.map(t=>t.category).filter(Boolean))){const option=node('option',categoryName(c));option.value=c;$('tutorial-category').append(option);}$('tutorial-category').value=[...$('tutorial-category').options].some(o=>o.value===old)?old:'';editor?.refresh();route();results();
 }
 function results(){
  const words=$('tutorial-search').value.trim().toLowerCase().split(/\s+/).filter(Boolean),category=$('tutorial-category').value,level=$('tutorial-level').value;
  const matches=topics.filter(t=>(!category||t.category===category)&&(!level||t.levelKey===level)&&(!$('tutorial-priority-filter').value||priorityLevel(t)===$('tutorial-priority-filter').value)&&words.every(w=>t.searchText.includes(w)));
  $('tutorial-count').textContent=matches.length+' / '+topics.length+tr(' хичээл',' tutorials');
  const snapshot=$('tutorial-priority-sort').value==='priority'?[...matches].sort((a,b)=>priorityRank(b)-priorityRank(a)||topics.indexOf(a)-topics.indexOf(b)):matches,selectedLang=lang,turn=++resultTurn;
  void typeset([$ ('tutorial-grid')],()=>{if(turn!==resultTurn)return false;const grid=$('tutorial-grid');grid.replaceChildren();for(const key of ['all']){const group=key==='all'?snapshot:snapshot.filter(t=>t.levelKey===key);if(!group.length)continue;const title=node('h3',key==='all'?($('tutorial-priority-sort').value==='priority'?(selectedLang==='en'?'Priority order':'Ач холбогдлоор'):(selectedLang==='en'?'Handbook learning order':'Номын сургалтын дарааллаар')):levelNames[selectedLang][levels.indexOf(key)],'tutorial-level-heading');grid.append(title);for(const t of group){const v=view(t,selectedLang),a=node('a',undefined,'tutorial-card');a.href='#tutorial/'+t.id;a.append(node('span',priorityName(t,selectedLang),'priority-badge priority-'+priorityLevel(t)));a.append(node('p',selectedLang==='en'?(categories[t.category]||t.category):t.category,'eyebrow'),node('h4',(handbookChapterNumbers[t.id]?handbookChapterNumbers[t.id]+'. ':(selectedLang==='en'?'Supplement · ':'Нэмэлт · '))+v.title),node('p',v.summary||''),node('small',selectedLang==='en'?'Small example · Walkthrough · Code · Practice →':'Жижиг жишээ · Алхамууд · Код · Дасгал →'));const mastery=ctx.learning()?.mastery(t);if(mastery)a.append(node('span',mastery.mastered?(selectedLang==='en'?'✓ Self-check + practice':'✓ Өөрийн үнэлгээ + дадлага'):mastery.read?(selectedLang==='en'?'Read':'Уншсан'):(selectedLang==='en'?'Not read':'Уншаагүй'),'tutorial-learning-state'));a.append(node('small','≈ '+Math.max(10,Math.round(JSON.stringify(v.sections).length/1500))+(selectedLang==='en'?' min':' минут')));const prerequisiteCount=(t.prerequisiteIds||[]).length;a.append(node('small',prerequisiteCount?(selectedLang==='en'?'Prerequisites: ':'Урьдчилсан хичээл: ')+prerequisiteCount:(selectedLang==='en'?'No prerequisite lessons':'Урьдчилсан хичээл шаардлагагүй')));for(const p of a.querySelectorAll('p'))if(!p.textContent.trim())p.hidden=true;if(!v.sections.length){for(const small of a.querySelectorAll('small'))if(small.textContent.includes('≈')||small.textContent.includes('→'))small.hidden=true;}grid.append(a);}}if(!snapshot.length)grid.append(node('p',selectedLang==='en'?'No matching tutorials. Try another keyword.':'Тохирох хичээл олдсонгүй. Өөр түлхүүр үгээр хайгаарай.','muted'));}).catch(()=>{});
 }
 function renderTopic(t,part){
  current=t;requestedPart=part;const turn=++renderTurn,selectedLang=lang==='en'&&!t.translations?.en?'mn':lang,v=view(t,selectedLang);labels();$('tutorial-browser').hidden=true;$('tutorial-reader').hidden=false;$('tutorial-level').closest('label').hidden=true;
  document.title=v.title+' — Erdene Club';$('tutorial-message').textContent='';$('tutorial-content').setAttribute('aria-busy','true');$('tutorial-math-message').textContent=tr('Томъёог дүрсэлж байна…','Rendering mathematics…');$('tutorial-math-retry').hidden=true;
  const elements=[$('tutorial-title'),$('tutorial-summary'),$('tutorial-prerequisites'),$('tutorial-prerequisite-links'),$('tutorial-lesson-navigation'),$('tutorial-content'),$('tutorial-learning-extras')];
  void typeset(elements,()=>{if(turn!==renderTurn)return false;$('tutorial-title').textContent=v.title;$('tutorial-summary').textContent=v.summary||'';$('tutorial-summary').hidden=!v.summary?.trim();$('tutorial-prerequisites').textContent=v.prerequisites?(selectedLang==='en'?'Prerequisites: ':'Урьдчилан мэдэх: ')+v.prerequisites:'';$('tutorial-prerequisites').hidden=!v.prerequisites?.trim();$('tutorial-meta').textContent=(lang==='en'&&!t.translations?.en?'English translation is not published yet. Монгол хувилбар · ':'')+(t.category?categoryName(t.category)+' · ':'')+levelNames[selectedLang][levels.indexOf(t.levelKey)]+' · '+priorityName(t,selectedLang)+(v.sections.length?' · ≈ '+Math.max(10,Math.round(JSON.stringify(v.sections).length/1500))+(selectedLang==='en'?' min reading':' минут унших'):'');learningLinks(t,selectedLang);drawArticle(t,$('tutorial-content'),selectedLang,{client:ctx.client(),viewerId:ctx.user()?.id||'public',learning:ctx.learning()});$('tutorial-learning-extras').replaceChildren();ctx.learning()?.renderTutorial(t,selectedLang,$('tutorial-learning-extras'));$('tutorial-content').lang=selectedLang;$('tutorial-toc').replaceChildren(node('strong',selectedLang==='en'?'In this tutorial':'Энэ хичээлд'));v.sections.forEach((s,i)=>{const a=node('a',s.title||((selectedLang==='en'?'Section ':'Хэсэг ')+(i+1)));a.href='#tutorial/'+t.id+'/part/'+i;$('tutorial-toc').append(a);});$('tutorial-related').replaceChildren(node('h3',selectedLang==='en'?'Related topics':'Холбоотой сэдвүүд'));$('tutorial-related').hidden=!(t.related||[]).length;for(const id of t.related||[]){const o=topics.find(x=>x.id===id);if(o){const a=node('a',view(o,selectedLang).title);a.href='#tutorial/'+id;$('tutorial-related').append(a);}}})
  .then(()=>{if(turn!==renderTurn)return false;$('tutorial-math-message').textContent='';reading(requestedPart);const target=Number.isInteger(requestedPart)?$('tutorial-'+t.id+'-'+activePart):$('tutorial-title');target?.scrollIntoView({block:'start',behavior:'instant'});$('tutorial-title').focus({preventScroll:true});})
  .catch(e=>{if(turn===renderTurn){$('tutorial-math-message').textContent=e.message+tr(' Томъёог түр LaTeX хэлбэрээр харуулж байна.',' Showing raw LaTeX temporarily.');$('tutorial-math-retry').hidden=false;}}).finally(()=>{if(turn===renderTurn)$('tutorial-content').setAttribute('aria-busy','false');});
 }
 function route(){
  labels();if(!topics.length){++renderTurn;current=null;$('tutorial-reader').hidden=true;$('tutorial-browser').hidden=false;results();return;}const m=location.hash.match(/^#tutorial\/([a-z0-9-]+)(?:\/part\/(\d+))?$/);
  if(m){const t=topics.find(x=>x.id===m[1]);if(t){const part=m[2]===undefined?undefined:Number(m[2]);if(current?.id===t.id&&part!==undefined){requestedPart=part;reading(part,true);}else renderTopic(t,part);return;}$('tutorial-message').textContent=tr('Хичээл олдсонгүй. Жагсаалтаас сонгоно уу.','Tutorial not found. Choose from the list.');}
  ++renderTurn;current=null;if(location.hash==='#tutorials'||m){$('tutorial-browser').hidden=false;$('tutorial-reader').hidden=true;$('tutorial-level').closest('label').hidden=false;results();}
 }
 async function connected(){
  if(!ctx.client())return;const turn=++loadTurn;
  try{const {data,error}=await ctx.client().rpc('get_tutorials');if(error)throw error;if(turn!==loadTurn)return;if(!Array.isArray(data))throw new Error('Tutorial data missing');onlineReady=true;hasLive=true;await accept(data,true);}
  catch{if(turn===loadTurn){onlineReady=false;editor?.refresh();if(!hasLive){await accept([],true);$('tutorial-message').textContent=tr('Хичээлийн санг баталгаажуулж чадсангүй. Холболтоо шалгаад хуудсаа дахин ачаална уу.','Could not verify the tutorial library. Check your connection and reload.');}}}
  editor?.accountChanged(true);
 }
 $('tutorial-language').onchange=()=>{lang=$('tutorial-language').value;try{localStorage.setItem('erdene:tutorial-language',lang);}catch{}current=null;results();route();};$('tutorial-search').addEventListener('input',results);$('tutorial-category').onchange=results;$('tutorial-level').onchange=results;$('tutorial-priority-filter').onchange=results;$('tutorial-priority-sort').onchange=results;
 $('tutorial-reading-mode').onchange=()=>{readingMode=$('tutorial-reading-mode').value;try{localStorage.setItem('erdene:tutorial-reading-mode',readingMode);}catch{}requestedPart=activePart;reading(activePart,true);};$('tutorial-section-prev').onclick=()=>goPart(activePart-1);$('tutorial-section-next').onclick=()=>goPart(activePart+1);
 $('tutorial-copy-link').onclick=()=>void copy(location.href,$('tutorial-copy-link'),tr('Хуулагдлаа','Copied'));$('tutorial-math-retry').onclick=()=>{if(current)renderTopic(current,activePart);};window.addEventListener('hashchange',route);
 editor=setupTutorialEditor({...ctx,topics:()=>topics,ready:()=>onlineReady,reload:connected,saved(row){accept([...topics.filter(t=>t.id!==row.body.id).map(t=>({body:t,revision:t.revision})),...(row.published===false?[]:[row])],true);},deleted(id){accept(topics.filter(t=>t.id!==id).map(t=>({body:t,revision:t.revision})),true);}});
 if(requiresOnline)$('tutorial-message').textContent=tr('Хичээлийн санг ачаалж байна…','Loading the tutorial library…');
 void lessonSeed.then(list=>{if(!requiresOnline&&!hasLive&&!ctx.client())return accept(list);}).catch(()=>{$('tutorial-grid').textContent='Tutorials ачаалсангүй / Could not load tutorials.';});
 return {connected,refreshStatus(){if(!current)results();},refreshLearning(){ctx.learning()?.setTopics(topics);if(current)renderTopic(current,activePart);else results();},accountChanged(){editor.accountChanged();const id=ctx.user()?.id||null;if(id!==mediaAccountId){mediaAccountId=id;clearMediaCache();if(current)renderTopic(current,activePart);}}};
}
