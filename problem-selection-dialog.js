import {filterProblems,getTags,ratingLabel} from './catalog.js?v=23';
import {canonicalKey} from './learning-model.js?v=23';
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
export function openProblemSelection({problems,progress=()=>({}),selected=[],valid=()=>true,multiple=true,includeArchived=false,maxSelected=Infinity,onSelect}){
 const dialog=el('dialog'),heading=el('h2','Бодлого сонгох'),filters=el('div'),list=el('div'),status=el('p');dialog.className='problem-selection-dialog';dialog.setAttribute('aria-label','Бодлого сонгох');filters.className='problem-selection-filters';list.className='problem-selection-list';status.setAttribute('role','status');
 const chosen=new Set(selected),fields={};let rows=[];const pool=[...new Map(problems().filter(p=>includeArchived||!p.archived).map(p=>[canonicalKey(p),p])).values()];
 function field(key,label,choices){const wrap=el('label',label),input=el(choices?'select':'input');if(choices)for(const [value,text]of choices){const o=el('option',text);o.value=value;input.append(o);}else{input.type=key==='query'?'search':'number';if(input.type==='number'){input.min=0;input.max=4000;input.step=1;}}input.dataset.filter=key;wrap.append(input);filters.append(wrap);fields[key]=input;input.oninput=render;}
 field('query','Хайлт');fields.query.placeholder='Нэр, ID эсвэл tag: binary search, grid, dp…';
 field('source','Эх сурвалж',[['','Бүгд'],...[...new Set(pool.map(p=>p.source))].sort().map(s=>[s,s])]);
 field('status','Миний төлөв',[['','Бүгд'],['new','Эхлээгүй'],['trying','Оролдож байгаа'],['solved','Бодсон'],['hinted','Hint ашигласан']]);
 field('tag','Tag',[['','Бүх tags'],...getTags(pool).map(t=>[t,t])]);
 field('ratingBand','Rating',[['','Бүх түвшин'],...['800-1100','1200-1500','1600-1800','1900-2100','2200-4000'].map(b=>[b,b])]);field('minRating','Min rating');field('maxRating','Max rating');
 field('sort','Эрэмбэ',[['rating-asc','Rating ↑'],['rating-desc','Rating ↓'],['priority','Priority эхэнд'],['title','Нэрээр'],['number-asc','Нэмсэн дарааллаар']]);
 function button(text,fn){const b=el('button',text);b.type='button';b.onclick=fn;return b;}
 const apply=button('Сонгосныг нэмэх',()=>{if(chosen.size>maxSelected)return;if(!valid()){close();return;}onSelect(pool.filter(p=>chosen.has(canonicalKey(p))),[...chosen]);close();});apply.dataset.selectionApply='true';
 function render(){if(!valid()){close();return;}const f=Object.fromEntries(Object.entries(fields).map(([k,v])=>[k,v.value]));rows=filterProblems(pool,progress()||{},f);list.replaceChildren();status.textContent=rows.length+' / '+pool.length+' бодлого · '+chosen.size+' сонгосон';apply.disabled=!chosen.size||chosen.size>maxSelected;if(chosen.size>maxSelected)status.textContent+=' · Энэ хэсэгт хамгийн ихдээ '+maxSelected+' бодлого сонгоно.';
  if(!rows.length)list.append(el('p','Тохирох бодлого олдсонгүй. Rating-ийн хязгаараа мөн шалгана уу.'));
  for(const p of rows){const row=el('label'),check=el('input');check.type='checkbox';check.checked=chosen.has(canonicalKey(p));check.value=canonicalKey(p);check.onchange=()=>{if(check.checked){if(!multiple){chosen.clear();for(const input of list.querySelectorAll('input'))input.checked=input===check;}chosen.add(check.value);}else chosen.delete(check.value);status.textContent=rows.length+' / '+pool.length+' бодлого · '+chosen.size+' сонгосон';apply.disabled=!chosen.size||chosen.size>maxSelected;if(chosen.size>maxSelected)status.textContent+=' · Энэ хэсэгт хамгийн ихдээ '+maxSelected+' бодлого сонгоно.';};row.append(check,el('span',p.title+' · '+p.id+' · '+p.source+' '+p.ref+' · '+ratingLabel(p)));list.append(row);}}
 const selectAll=button('Шүүгдсэн бүх бодлогыг сонгох',()=>{for(const p of rows)chosen.add(canonicalKey(p));render();});selectAll.dataset.selectFiltered='true';selectAll.hidden=!multiple;
 const clear=button('Сонголтыг цэвэрлэх',()=>{chosen.clear();render();}),cancel=button('Болих',close);
 let watcher;function close(){clearInterval(watcher);if(dialog.open)dialog.close();dialog.remove();}dialog.oncancel=()=>close();dialog.onclose=close;
 dialog.append(heading,filters,status,selectAll,clear,list,apply,cancel);document.body.append(dialog);render();if(!dialog.isConnected)return;dialog.showModal();fields.query.focus();watcher=setInterval(()=>{if(!valid())close();},250);return {close};
}
