import {safeLink,validateExtendedBlock} from './tutorial-blocks.js?v=40';
import {tutorialImageUrl} from './tutorial-media.js?v=40';
const node=(tag,text,cls)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
export function appendInline(parent,content){
 for(const run of content||[]){let e=document.createTextNode(run.text);for(const mark of run.marks||[]){const tag={bold:'strong',italic:'em',underline:'u',strike:'s',code:'code'}[mark];if(tag){const wrap=node(tag);wrap.append(e);e=wrap;}}
  const href=run.href&&safeLink(run.href);if(href){const a=node('a');a.href=href;if(!href.startsWith('#')){a.target='_blank';a.rel='noopener noreferrer';}a.append(e);e=a;}parent.append(e);
 }
}
export function renderExtendedBlock(b,parent,lang='mn',options={}){
 if(!b||typeof b!=='object'){parent.append(node('aside',lang==='en'?'This content needs a review.':'Энэ агуулгын хэсгийг шалгах шаардлагатай.','tutorial-note'));return true;}
 if(!['rich','heading','quote','callout','checklist','divider','image','diagram','problem','tutorial'].includes(b.type))return false;
 try{validateExtendedBlock(b);}catch{parent.append(node('aside',lang==='en'?'This block needs an editor review.':'Энэ block-ийн тохиргоог editor дээр шалгана уу.','tutorial-note'));return true;}
 if(b.type==='rich'){const p=node('p',undefined,'rich-text');appendInline(p,b.content);parent.append(p);}
 else if(b.type==='heading'){// Article title remains the only page-level H1.
  const h=node('h'+Math.max(2,b.level),b.text,'block-heading level-'+b.level);parent.append(h);
 }
 else if(b.type==='quote'){const q=node('blockquote');if(b.content)appendInline(q,b.content);else q.textContent=b.text;parent.append(q);}
 else if(b.type==='callout'){const box=node('aside',undefined,'tutorial-callout tone-'+b.tone);if(b.title)box.append(node('strong',b.title));const p=node('p');if(b.content)appendInline(p,b.content);else p.textContent=b.text;box.append(p);parent.append(box);}
 else if(b.type==='divider')parent.append(node('hr'));
 else if(b.type==='checklist'){const list=node('ul',undefined,'content-checklist');for(const item of b.items){const li=node('li'),input=node('input');input.type='checkbox';input.disabled=true;input.checked=item.checked;li.append(input,node('span',item.text));list.append(li);}parent.append(list);}
 else if(b.type==='image'){
  const figure=node('figure',undefined,'tutorial-image align-'+b.align);figure.style.width=b.width+'%';const img=node('img');img.alt=b.alt;img.loading='lazy';img.decoding='async';const status=node('p',lang==='en'?'Loading image…':'Зургийг ачаалж байна…','muted');figure.append(img,status);if(b.caption)figure.append(node('figcaption',b.caption));parent.append(figure);
  function showFailure(){status.replaceChildren(node('span',lang==='en'?'Image unavailable. ':'Зураг одоогоор боломжгүй. '));if(!status.isConnected)figure.append(status);const retry=node('button',lang==='en'?'Retry':'Дахин оролдох');retry.type='button';retry.onclick=load;status.append(retry);}
  function load(){status.textContent=lang==='en'?'Loading image…':'Зургийг ачаалж байна…';void tutorialImageUrl(options.client,b.path,options.viewerId,options.adminPreview).then(url=>{if(!figure.isConnected)return;img.onload=()=>status.remove();img.onerror=showFailure;img.src=url;}).catch(showFailure);}load();
 }
 else if(b.type==='tutorial'){const a=node('a',b.label||b.tutorialId,'inline-tutorial-link');a.href='#tutorial/'+b.tutorialId;parent.append(a);}
 else if(b.type==='problem'){if(options.learning?.renderEmbeddedProblem)options.learning.renderEmbeddedProblem(b.problemKey,parent,lang);else parent.append(node('p',(lang==='en'?'Linked problem is unavailable: ':'Холбосон бодлого одоогоор боломжгүй: ')+b.problemKey,'learning-note'));}
 else if(b.type==='diagram'){
  const figure=node('figure',undefined,'tutorial-diagram');figure.setAttribute('aria-label',b.caption||b.kind);const high=new Set(b.highlights||[]);
  if(['array','dp'].includes(b.kind)){const wrap=node('div',undefined,'diagram-grid-wrap'),table=node('table',undefined,'diagram-grid');b.rows.forEach((row,i)=>{const tr=node('tr');row.forEach((text,j)=>{const td=node('td',text);if(high.has(i+':'+j))td.className='highlight';tr.append(td);});table.append(tr);});wrap.append(table);figure.append(wrap);}
  else {const canvas=node('div',undefined,'diagram-graph'),svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 600 320');svg.setAttribute('preserveAspectRatio','none');svg.setAttribute('aria-hidden','true');const positions=new Map();b.nodes.forEach((n,i)=>{const angle=2*Math.PI*i/b.nodes.length-Math.PI/2;positions.set(n.id,{x:n.x??50+38*Math.cos(angle),y:n.y??50+35*Math.sin(angle)});});for(const[a,z]of b.edges){const p=positions.get(a),q=positions.get(z),line=document.createElementNS('http://www.w3.org/2000/svg','line');line.setAttribute('x1',p.x*6);line.setAttribute('y1',p.y*3.2);line.setAttribute('x2',q.x*6);line.setAttribute('y2',q.y*3.2);svg.append(line);}canvas.append(svg);for(const n of b.nodes){const p=positions.get(n.id),item=node('span',n.label,'diagram-node'+(high.has(n.id)?' highlight':''));item.style.left=p.x+'%';item.style.top=p.y+'%';canvas.append(item);}figure.append(canvas);}
  if(b.caption)figure.append(node('figcaption',b.caption));parent.append(figure);
 }
 return true;
}
