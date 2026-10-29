import {priorityLevel,priorityLabel,isHighPriority,ratingClass} from './priority.js?v=52';
import {filterProblems,getTags,ratingLabel} from './catalog.js?v=52';
import {problemReferenceKey as canonicalKey,problemIndex} from './learning-model.js?v=66';
const el=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
export function openProblemSelection({problems,progress=()=>({}),selected=[],valid=()=>true,multiple=true,includeArchived=false,maxSelected=Infinity,onSelect}){
 const dialog=el('dialog'),heading=el('h2','Бодлого сонгох'),filters=el('div'),status=el('p');
 dialog.className='problem-selection-dialog';dialog.setAttribute('aria-label','Бодлого сонгох');filters.className='problem-selection-filters';status.setAttribute('role','status');
 const pool=[...new Map(problems().filter(p=>includeArchived||!p.archived).map(p=>[canonicalKey(p),p])).values()],lookup=problemIndex(problems()),byKey=new Map(pool.map(p=>[canonicalKey(p),p]));
 const chosen=new Set(selected.map(k=>lookup.has(String(k))?canonicalKey(lookup.get(String(k))):String(k))),marked=new Set(),fields={};let rows=[];
 function field(key,label,choices){const wrap=el('label',label),input=el(choices?'select':'input');if(choices)for(const [value,text]of choices){const o=el('option',text);o.value=value;input.append(o);}else{input.type=key==='query'?'search':'number';if(input.type==='number'){input.min=0;input.max=4000;input.step=1;}}input.dataset.filter=key;wrap.append(input);filters.append(wrap);fields[key]=input;input.oninput=render;}
 field('query','Хайлт');fields.query.placeholder='Нэр, #дугаар эсвэл tag: binary search, grid, dp…';
 field('source','Эх сурвалж',[['','Бүгд'],...[...new Set(pool.map(p=>p.source))].sort().map(s=>[s,s])]);
 field('status','Миний төлөв',[['','Бүгд'],['new','Эхлээгүй'],['trying','Оролдож байгаа'],['solved','Бодсон']]);
 field('priorityLevel','Priority',[['','Бүгд'],['high','High'],['medium','Medium'],['low','Low']]);
 field('tag','Tag',[['','Бүх tags'],...getTags(pool).map(t=>[t,t])]);field('minRating','Min rating');field('maxRating','Max rating');
 field('sort','Эрэмбэ',[['rating-asc','Rating ↑'],['rating-desc','Rating ↓'],['priority','Priority эхэнд'],['title','Нэрээр'],['number-asc','Нэмсэн дарааллаар']]);
 function button(text,fn){const b=el('button',text);b.type='button';b.onclick=fn;return b;}
 const columns=el('div');columns.className='problem-selection-columns';
 const left=el('section'),right=el('section'),list=el('div'),picked=el('div'),leftTitle=el('h3'),rightTitle=el('h3');list.className=picked.className='problem-selection-list';list.dataset.selectionAvailable='true';picked.dataset.selectionChosen='true';left.setAttribute('aria-label','Шүүгдсэн сонгогдоогүй бодлогууд');right.setAttribute('aria-label','Бүх сонгогдсон бодлогууд');
 const selectAll=button('Шүүгдсэн бүх бодлогыг сонгох',()=>{for(const p of rows)chosen.add(canonicalKey(p));render();});selectAll.dataset.selectFiltered='true';selectAll.hidden=!multiple;
 const markAll=button('Бүгдийг сонгох',()=>{for(const key of chosen)marked.add(key);render();});markAll.dataset.markChosen='true';
 const remove=button('Сонгосныг болиулах',()=>{for(const key of marked)chosen.delete(key);marked.clear();render();});remove.dataset.removeChosen='true';
 const clear=button('Бүх сонголтыг болиулах',()=>{chosen.clear();marked.clear();render();});clear.dataset.clearChosen='true';
 const reset=button('Шүүлтүүр арилгах',()=>{for(const [key,input]of Object.entries(fields))input.value=key==='sort'?'rating-asc':'';render();});reset.dataset.resetFilters='true';
 const apply=button('Сонголтыг хадгалах',()=>{if((!multiple&&!chosen.size)||chosen.size>maxSelected)return;if(!valid()){close();return;}onSelect(pool.filter(p=>chosen.has(canonicalKey(p))),[...chosen]);close();});apply.dataset.selectionApply='true';
 const cancel=button('Болих',close),footer=el('div');footer.className='problem-selection-footer';footer.append(apply,cancel);
 left.append(leftTitle,selectAll,list);right.append(rightTitle,el('p','Буцаах бодлогуудыг тэмдэглээд “Сонгосныг болиулах” дарна уу.'),markAll,remove,clear,picked);columns.append(left,right);
 const description=(p,key)=>p?(p.number!=null?'#'+p.number+' · ':'')+(isHighPriority(p)?'★ ':'')+priorityLabel(p)+' · '+p.title+' · '+p.source+' '+p.ref+' · '+ratingLabel(p):'Одоогоор боломжгүй: '+key;
 function row(p,key,removal){const wrap=el('label'),check=el('input');wrap.dataset.priority=String(isHighPriority(p));wrap.dataset.priorityLevel=priorityLevel(p);check.type='checkbox';check.value=key;check.checked=removal?marked.has(key):false;check.setAttribute('aria-label',(removal?'Буцаахаар тэмдэглэх: ':'Сонгох: ')+description(p,key));check.onchange=()=>{if(!valid()){close();return;}if(removal){if(check.checked)marked.add(key);else marked.delete(key);}else{if(!multiple){chosen.clear();marked.clear();}chosen.add(key);}render();};const text=el('span',description(p,key));if(p){const rating=el('span',ratingLabel(p));rating.className='rating '+ratingClass(p);text.append(document.createTextNode(' · '),rating);}wrap.append(check,text);return wrap;}
 function render(){if(!valid()){close();return;}rows=filterProblems(pool,progress()||{},Object.fromEntries(Object.entries(fields).map(([k,v])=>[k,v.value])));const available=rows.filter(p=>!chosen.has(canonicalKey(p)));list.replaceChildren();picked.replaceChildren();leftTitle.textContent='Сонгогдоогүй · '+available.length;rightTitle.textContent='Сонгогдсон · '+chosen.size;
  for(const p of available)list.append(row(p,canonicalKey(p),false));if(!available.length)list.append(el('p','Шүүлтүүрт тохирох сонгогдоогүй бодлого алга.'));
  for(const key of chosen)picked.append(row(byKey.get(key),key,true));if(!chosen.size)picked.append(el('p','Зүүн талаас бодлого сонгоорой.'));
  status.textContent=rows.length+' / '+pool.length+' бодлого · '+chosen.size+' сонгосон';apply.disabled=(!multiple&&!chosen.size)||chosen.size>maxSelected;if(chosen.size>maxSelected)status.textContent+=' · Энэ хэсэгт хамгийн ихдээ '+maxSelected+' бодлого сонгоно.';
  selectAll.disabled=!available.length;markAll.disabled=clear.disabled=!chosen.size;remove.disabled=!marked.size;
 }
 let watcher;function close(){clearInterval(watcher);if(dialog.open)dialog.close();dialog.remove();}dialog.oncancel=()=>close();dialog.onclose=close;
 dialog.append(heading,filters,reset,status,columns,footer);document.body.append(dialog);render();if(!dialog.isConnected)return;dialog.showModal();fields.query.focus();watcher=setInterval(()=>{if(!valid())close();},250);return {close};
}
