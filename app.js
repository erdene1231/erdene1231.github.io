import {setupLearning} from './learning.js?v=31';
import {setupTutorials} from './tutorials.js?v=31';
import {setupGroups} from './groups.js?v=20';
let tutorialUI, learningUI=null;
import {EMPTY, cleanEntry, parseBackup} from './progress.js';
import {getSolvers} from './community.js?v=6';
import {setupAdmin} from './admin.js?v=23';
import {parseCatalog,hintTexts,getSources} from './problem-store.js?v=23';
import {rpc} from './accounts.js?v=17';
import {ownProfile,saveOwnProfile,avatarUrl,accountError} from './accounts.js?v=17';
import {setupSocial} from './social.js?v=23';
import {filterProblems, getTags, ratingLabel,difficultyLabel} from './catalog.js?v=23';
const $ = id => document.getElementById(id);
const STATUS = {new:'Эхлээгүй',trying:'Оролдож байгаа',solved:'Бодсон'};
let data, selectedPack='', selectedProblem, state={}, dirty={}, user=null, client=null, loading=false, syncing=false, syncAgain=false, epoch=0;
let username=null, profileLoading=false, profileSaving=false, solverRequest=0, solverNames=[], solverTotal=0;
let detailTagsShown=false,problemPage=0,lastFilterKey='',activityPending={};
const PROBLEMS_PER_PAGE=100;
const hiddenHints=new Set();
let social=null, adminUI=null, groupUI=null, myProfile=null, avatarPreviewUrl=null, catalogLoading=false;
let catalogIds=new Set(),hintLanguage='mn';
const cfg=window.THINK_CP_CONFIG || {};
const configured=Boolean(cfg.supabaseUrl && cfg.supabaseKey);
const key=()=> 'think-cp:v1:'+(user?.id || 'guest');
function notice(message) { $('notice').textContent=message; }
const validProgressId=id=>typeof id==='string'&&/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}$/.test(id)&&!['constructor','prototype'].includes(id);
function readLocal() {
  try { const saved=JSON.parse(localStorage.getItem(key()) || '{}'); state={}; dirty={}; activityPending={}; for(const [id,entry] of Object.entries(saved.progress || {})) if(validProgressId(id)) state[id]=cleanEntry(entry); for(const id of saved.dirty || []) if(state[id]) dirty[id]=state[id];for(const id of Array.isArray(saved.activityPending)?saved.activityPending:[])if(validProgressId(id)&&dirty[id])activityPending[id]={}; }
  catch {state={};dirty={};activityPending={};notice('Өмнөх хадгалалтыг уншиж чадсангүй. Progress татах боломжийг ашиглаарай.');}
}
function persist() {
  try {localStorage.setItem(key(),JSON.stringify({progress:state,dirty:Object.keys(dirty),activityPending:Object.keys(activityPending)}));return true;}
  catch {notice('Browser хадгалалт боломжгүй байна. Хуудсаа хаахаас өмнө progress-оо татаж аваарай.');return false;}
}
function entry(id) {return state[id] || {...EMPTY};}
function setEntry(id, patch) {if(loading)return; const before=entry(id).status;state[id]=cleanEntry({...entry(id),...patch});learningUI?.progressChanged(id,before,state[id].status);if(before!==state[id].status){if(['trying','solved'].includes(state[id].status))activityPending[id]={};else delete activityPending[id];}dirty[id]=state[id];const saved=persist();render();if(user)void sync();else if(saved)notice('Progress энэ browser-т хадгалагдлаа.');}
function el(tag, cls, text) {const node=document.createElement(tag); if(cls)node.className=cls;if(text!==undefined)node.textContent=text;return node;}
function renderHome() {
  const active=data.problems.filter(problem=>entry(problem.id).status==='trying');
  const list=$('home-continue-list');if(!list)return;list.replaceChildren();
  $('home-trying-count').textContent=active.length+' бодлого';
  for(const problem of active.slice(0,3)) {
    const button=el('button','home-recent');button.type='button';button.disabled=loading||catalogLoading;
    const info=el('span','home-recent-info');
    info.append(el('strong','',problem.title),el('small','',problem.source+' · '+ratingLabel(problem)));
    const arrow=el('span','home-recent-arrow','↗');arrow.setAttribute('aria-hidden','true');
    button.append(info,arrow);button.onclick=()=>openProblem(problem);list.append(button);
  }
  if(!active.length) {
    const empty=el('div','home-empty');
    empty.append(el('strong','','Оролдож байгаа бодлого алга.'),el('p','','“Оролдож байгаа” гэж тэмдэглэсэн бодлогууд энд харагдана.'));
    list.append(empty);
  }
}
function render() {
  const solved=data.problems.filter(p=>entry(p.id).status==='solved').length;
  const trying=data.problems.filter(p=>entry(p.id).status==='trying').length;
  const percent=(data.problems.length?Math.round(solved/data.problems.length*100):0);
  $('total').textContent=data.problems.length;$('solved').textContent=solved;$('trying').textContent=trying;$('percent').textContent=percent+'%';$('progress').value=percent;
  renderHome();learningUI?.render();
  const filters={query:$('search').value,source:$('source').value,status:$('status-filter').value,pack:selectedPack,tag:$('tag-filter').value,ratingBand:$('rating-filter').value,minRating:$('min-rating').value,maxRating:$('max-rating').value,priorityOnly:$('priority-only').checked,sort:$('sort').value};
  const filterKey=JSON.stringify(filters);if(filterKey!==lastFilterKey){problemPage=0;lastFilterKey=filterKey;}
  $('packs').replaceChildren();
  for(const pack of [{id:'',title:'Бүгд'},...data.packs]) {
    const b=el('button',pack.id===selectedPack?'active':'',pack.title);b.setAttribute('aria-pressed',String(pack.id===selectedPack));b.onclick=()=>{selectedPack=pack.id;render();};$('packs').append(b);
  }
  $('pack-note').textContent=data.packs.find(p=>p.id===selectedPack)?.description || '★ Priority бодлогууд нь observation болон creative reasoning-д онцгой анхаарсан сонголт. Rating бол чиг баримжаа; өөрийн түвшинд тохируулж сонго.';
  $('problems').classList.toggle('compact',$('problem-density').value==='compact');$('problems').replaceChildren();
  const invalidRange=!$('min-rating').checkValidity()||!$('max-rating').checkValidity()||($('min-rating').value!==''&&$('max-rating').value!==''&&Number($('min-rating').value)>Number($('max-rating').value));
  const filtered=invalidRange?[]:filterProblems(data.problems,state,filters);
  $('results-count').textContent=filtered.length+' / '+data.problems.length+' бодлого';
  const pageCount=Math.ceil(filtered.length/PROBLEMS_PER_PAGE);problemPage=Math.max(0,Math.min(problemPage,pageCount-1));
  const start=problemPage*PROBLEMS_PER_PAGE,end=Math.min(start+PROBLEMS_PER_PAGE,filtered.length);
  $('problem-prev').disabled=problemPage===0||!pageCount;$('problem-next').disabled=!pageCount||problemPage>=pageCount-1;
  $('problem-page').textContent=pageCount?(problemPage+1)+' / '+pageCount+' хуудас · '+(start+1)+'–'+end+' / '+filtered.length+' бодлого':'0 бодлого';
  $('rating-range-message').textContent=invalidRange?'Rating хязгаар 0–4000 бүхэл тоо байна. Min rating нь Max rating-аас их байж болохгүй.':'';
  for(const p of filtered.slice(start,end)) {
    const row=el('article','problem'+(p.priority?' is-priority':'')), n=el('span','number','#'+String(p.number).padStart(3,'0')), b=el('button','open');b.disabled=loading||catalogLoading;
    const heading=el('h3','',p.title);
    if(p.priority){const star=el('span','priority-star','★');star.title='Priority бодлого';star.setAttribute('aria-label','Priority');heading.prepend(star);}
    const meta=el('div','problem-meta');const rating=el('span','rating rating-'+Math.floor(p.rating/100),ratingLabel(p));rating.title=p.ratingKind==='official'?'Codeforces-ийн албан rating':(p.ratingBasis||'Зохиогчийн CF difficulty-ийн estimate; official биш');
    meta.append(rating,el('small','',p.source+' · '+p.ref+' · '+difficultyLabel(p)+(p.level==='Interactive'?' · Interactive':'')));
    b.append(heading,meta);b.onclick=()=>openProblem(p);
    if($('show-tags').checked||entry(p.id).status==='solved'){const tags=el('div','tag-chips');for(const tag of p.tags)tags.append(el('span','tag-chip',tag));b.append(tags);}
    const badge=el('span','badge '+entry(p.id).status,STATUS[entry(p.id).status]);
    const arrow=el('button','arrow','↗');arrow.setAttribute('aria-label',p.title+' нээх');arrow.disabled=loading||catalogLoading;arrow.onclick=()=>openProblem(p);
    if(entry(p.id).hints&&p.hints?.length) b.append(el('span','hint-used','Hint '+Math.min(entry(p.id).hints,p.hints.length)+'/'+p.hints.length));
    row.append(n,b,badge,arrow);const learningLinks=el('div','problem-learning-links');for(const t of learningUI?.linksForProblem(p)||[]){const a=el('a','',(t.primary?'Үндсэн · ':'')+t.title);a.href='#tutorial/'+t.id;learningLinks.append(a);}const days=learningUI?.planDaysFor(p)||[];if(days.length){const a=el('a','','Өдөр '+days.slice(0,3).join(', ')+(days.length>3?'…':''));a.href='#plan/'+days[0];learningLinks.append(a);}if(learningLinks.children.length)row.append(learningLinks);$('problems').append(row);
  }
  if(!filtered.length)$('problems').append(el('p','muted','Тохирох бодлого олдсонгүй. Шүүлтүүрээ өөрчлөөрэй.'));
}
function openProblem(p) {selectedProblem=p;detailTagsShown=false;$('detail-title').textContent=(p.priority?'★ ':'')+p.title;$('detail-source').textContent='#'+p.number+' · '+p.source+' · '+p.ref;$('detail-note').textContent=ratingLabel(p)+(p.ratingKind==='official'?' · CF албан rating':' · CF difficulty-ийн баримжаа'+(p.ratingConfidence==='rough'?' · Урьдчилсан үнэлгээ':''))+(p.level==='Interactive'?' · Interactive':'')+(p.source==='EGOI'?' · Full task; subtask-аас эхэл':'')+(p.priority?' · Priority':'');$('problem-link').href=p.url;$('notes').value=entry(p.id).notes;$('detail-feedback').textContent='';renderDetail();$('detail').showModal();void loadSolvers();}
function renderDetail() {
  if(!selectedProblem)return;const learningLinks=$('detail-learning-links');learningLinks.replaceChildren();for(const t of learningUI?.linksForProblem(selectedProblem)||[]){const a=el('a','',(t.primary?'Үндсэн · ':'')+t.title);a.href='#tutorial/'+t.id;a.onclick=()=>$('detail').close();learningLinks.append(a);}learningUI?.renderProblemLinks(selectedProblem,learningLinks);const p=selectedProblem,e=entry(p.id),hintCount=p.hints?.length||0;$('hint-language').closest('label').hidden=!hintCount;$('problem-status').value=e.status;$('hint-list').replaceChildren();
  hintTexts(p,hintLanguage).slice(0,e.hints).forEach((hint,i)=>{const h=el('div','hint');h.append(el('b','','HINT '+(i+1)),el('span','',hint));$('hint-list').append(h);});
  const hintsVisible=!hiddenHints.has(p.id);
  $('hint-list').hidden=!hintsVisible;
  $('toggle-hints').hidden=!hintCount||e.hints===0;
  $('toggle-hints').textContent=hintsVisible?'Hint-үүдийг нуух':'Нээсэн hint-үүдийг харуулах';
  $('toggle-hints').setAttribute('aria-expanded',String(hintsVisible&&e.hints>0));
  $('next-hint').hidden=e.hints>=hintCount;$('next-hint').textContent='Hint '+(e.hints+1)+' нээх';$('reflection').hidden=e.status!=='solved';$('tags').textContent='Сэдэв: '+p.tags.join(' · ');$('lesson').textContent=p.lesson||'';$('lesson').hidden=!p.lesson;
  const tagsVisible=$('show-tags').checked||detailTagsShown||e.status==='solved';$('detail-tags').hidden=!tagsVisible;$('detail-tags').replaceChildren();for(const tag of p.tags)$('detail-tags').append(el('span','tag-chip',tag));
  $('reveal-detail-tags').hidden=$('show-tags').checked||e.status==='solved';$('reveal-detail-tags').textContent=detailTagsShown?'Tags нуух':'Tags харуулах';
  $('editorial-link').hidden=!p.editorialUrl;if(p.editorialUrl)$('editorial-link').href=p.editorialUrl;
}
async function switchUser(next) {
  if(user?.id===next?.id)return;
  const turn=++epoch;user=next;username=null;myProfile=null;if(avatarPreviewUrl){URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;}for(const id of ['full-name','first-name','last-name','school','avatar-file'])$(id).value='';$('legacy-name-note').textContent='';$('remove-avatar').checked=false;renderOwnAvatar();profileLoading=false;profileSaving=false;$('username').value='';$('profile-feedback').textContent='';loading=!!user;$('detail').close();readLocal();render();updateAccount();
  if(user) {
    void loadProfile();
    try {
      const {data:rows,error}=await client.from('progress').select('problem_id,status,hints,notes').eq('user_id',user.id);
      if(error)throw error;if(turn!==epoch)return;
      const remote={};for(const row of rows)if(validProgressId(row.problem_id))remote[row.problem_id]=cleanEntry(row);
      state={...remote,...dirty};persist();notice('Account-ын progress ачаалагдлаа.');
    } catch(error) {if(turn===epoch)notice('Онлайн progress ачаалагдсангүй. Энэ төхөөрөмжийн хуулбарыг ашиглаж байна: '+error.message);}
    finally {if(turn===epoch){loading=false;render();void sync();}}
  } else {notice('Зочин горим. Progress энэ browser-т хадгалагдана.');}
}
async function sync() {
  if(!user || !client || loading)return;
  if(syncing){syncAgain=true;return;}if(!Object.keys(dirty).length)return;
  syncing=true;const turn=epoch,uid=user.id, batch={...dirty},activityBatch={...activityPending};notice('Онлайнаар хадгалж байна…');
  try {
    let result=await client.from('progress').upsert(Object.entries(batch).map(([problem_id,e])=>({user_id:uid,problem_id,...e,record_activity:Boolean(activityBatch[problem_id])})),{onConflict:'user_id,problem_id'});
    if(result.error&&String(result.error.message).includes('record_activity')&&['PGRST204','42703'].includes(result.error.code))result=await client.from('progress').upsert(Object.entries(batch).map(([problem_id,e])=>({user_id:uid,problem_id,...e})),{onConflict:'user_id,problem_id'});
    if(result.error)throw result.error;if(turn!==epoch)return;
    for(const id of Object.keys(batch)){if(dirty[id]===batch[id])delete dirty[id];if(activityPending[id]===activityBatch[id])delete activityPending[id];}persist();notice(Object.keys(dirty).length?'Өөрчлөлтийг хадгалж байна…':'Онлайн progress хадгалагдлаа.');
    if($('detail').open && batch[selectedProblem?.id])void loadSolvers();learningUI?.profileUpdated();
  } catch(error) {if(turn===epoch)notice('Онлайн хадгалалт амжилтгүй. Browser-т хадгалсан; дахин оролдох боломжтой. '+error.message);}
  finally {syncing=false;updateAccount();if(syncAgain){syncAgain=false;void sync();}}
}
function renderOwnAvatar() {
  const url=avatarPreviewUrl||avatarUrl(client,myProfile);$('own-avatar').hidden=!url;if(url)$('own-avatar').src=url;else $('own-avatar').removeAttribute('src');$('own-avatar-fallback').hidden=!!url;$('own-avatar-fallback').textContent=((myProfile?.full_name||myProfile?.username||'?')[0]||'?').toUpperCase();
}
function updateAccount() {
  social?.accountChanged();adminUI?.accountChanged();tutorialUI?.accountChanged();groupUI?.accountChanged();learningUI?.accountChanged();
  for(const id of ['full-name','first-name','last-name','school','avatar-file','remove-avatar'])$(id).disabled=profileLoading||profileSaving||!myProfile;
  $('reload-profile').hidden=!user||!!myProfile;$('reload-profile').disabled=profileLoading;
  $('account').textContent=user?(username?'@'+username:'Миний account'):'Нэвтрэх';$('storage-label').textContent=user?'Account-д хадгална':'Энэ төхөөрөмжид хадгална';
  $('auth-form').hidden=!client||!!user;$('signout').hidden=!user;$('retry-sync').hidden=!user||!Object.keys(dirty).length;
  $('profile-form').hidden=!client||!user;$('save-username').disabled=profileLoading||profileSaving||!myProfile;$('username').disabled=profileLoading||profileSaving||!myProfile;
  $('current-username').textContent=username?'Одоогийн нэр: @'+username:'Username-ээ тохируулсны дараа бодсон хүмүүсийн жагсаалтад гарна.';
  $('auth-info').textContent=user?'Нэвтэрсэн: '+user.email:client?'Email-аар бүртгүүлж, бусад төхөөрөмжөөс progress-оо үргэлжлүүлээрэй. Зочин progress автоматаар account руу шилжихгүй; татаж аваад нэвтэрсний дараа сэргээж болно.':'Account хараахан идэвхжээгүй. Одоогоор зочин горимоор ашиглаж, progress-оо энэ browser-т хадгалах эсвэл файл болгож татах боломжтой.';
}
async function loadProfile() {
  const turn=epoch, uid=user?.id;if(!client||!uid)return;
  profileLoading=true;updateAccount();
  try {const profile=await ownProfile(client,uid);if(turn!==epoch)return;myProfile=profile;username=myProfile.username;$('username').value=username||'';$('full-name').value=myProfile.full_name||'';$('first-name').value=myProfile.first_name||'';$('last-name').value=myProfile.last_name||'';$('legacy-name-note').textContent=!myProfile.first_name&&!myProfile.last_name&&myProfile.full_name?'Өмнө хадгалсан овог нэр: '+myProfile.full_name+'. Excel тайланд овог, нэрээ тусад нь гаргахын тулд дээрх хоёр талбарыг бөглөөрэй.':'';$('school').value=myProfile.school||'';renderOwnAvatar();}
  catch(error){if(turn===epoch)$('profile-feedback').textContent=accountError(error);}
  finally {if(turn===epoch){profileLoading=false;updateAccount();}}
}
async function saveProfile(event) {
  event.preventDefault();if(!user||!client||!myProfile||profileLoading||profileSaving||!$('profile-form').reportValidity())return;
  const turn=epoch, uid=user.id;profileSaving=true;updateAccount();$('profile-feedback').textContent='Profile хадгалж байна…';
  try {const saved=await saveOwnProfile(client,uid,{username:$('username').value,full_name:(myProfile.first_name||myProfile.last_name)?'':$('full-name').value,first_name:$('first-name').value,last_name:$('last-name').value,school:$('school').value,avatar_path:$('remove-avatar').checked?null:myProfile?.avatar_path},$('remove-avatar').checked?null:$('avatar-file').files?.[0],myProfile?.avatar_path);if(turn!==epoch)return;myProfile=saved;username=saved.username;$('username').value=username;$('full-name').value=saved.full_name;$('legacy-name-note').textContent='';$('avatar-file').value='';$('remove-avatar').checked=false;if(avatarPreviewUrl){URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;}renderOwnAvatar();$('profile-feedback').textContent='Profile хадгалагдлаа.';social?.connected();groupUI?.connected();learningUI?.profileUpdated();}
  catch(error){if(turn===epoch)$('profile-feedback').textContent=accountError(error);}
  finally {if(turn===epoch){profileSaving=false;updateAccount();}}
}
async function loadSolvers(append=false) {
  if(!selectedProblem || !$('detail').open)return;
  const request=++solverRequest, pid=selectedProblem.id, turn=epoch, offset=append?solverNames.length:0;
  if(!append){solverNames=[];solverTotal=0;$('solver-list').replaceChildren();$('solver-count').textContent='';}
  $('more-solvers').hidden=true;$('refresh-solvers').disabled=true;
  if(!client){$('solvers-message').textContent='Бодсон хүмүүсийг харахад онлайн холболт шаардлагатай.';$('refresh-solvers').disabled=false;return;}
  $('solvers-message').textContent='Бодсон хүмүүсийг ачаалж байна…';
  try {
    const result=await getSolvers(client,pid,offset);
    if(request!==solverRequest||turn!==epoch||selectedProblem.id!==pid||!$('detail').open)return;
    solverNames=[...new Set([...solverNames,...result.names])];solverTotal=result.total||solverNames.length;
    $('solver-list').replaceChildren();for(const name of solverNames){const li=el('li',name===username?'mine':''),button=el('button','','@'+name+(name===username?' · чи':''));button.onclick=()=>{ $('detail').close();void social?.byUsername(name);};li.append(button);$('solver-list').append(li);}
    $('solver-count').textContent='('+solverTotal+')';$('solvers-message').textContent=solverNames.length?'':'Одоогоор username-тай хэрэглэгч “Бодсон” гэж тэмдэглээгүй байна.';
    $('more-solvers').hidden=!result.names.length||solverNames.length>=solverTotal;
  } catch(error){if(request===solverRequest&&turn===epoch){$('solvers-message').textContent='Жагсаалтыг ачаалж чадсангүй. Шинэчлэх товчоор дахин оролдоорой.';}}
  finally {if(request===solverRequest&&turn===epoch)$('refresh-solvers').disabled=false;}
}
async function authAction(signup) {
  if(!$('auth-form').reportValidity())return;const buttons=$('auth-form').querySelectorAll('button');buttons.forEach(b=>b.disabled=true);$('auth-feedback').textContent='Түр хүлээнэ үү…';
  try {
    const credentials={email:$('email').value.trim(),password:$('password').value};
    const result=signup?await client.auth.signUp({...credentials,options:{emailRedirectTo:location.origin+location.pathname}}):await client.auth.signInWithPassword(credentials);
    if(result.error)throw result.error;$('password').value='';$('auth-feedback').textContent=result.data.session?'Амжилттай нэвтэрлээ.':'Email баталгаажуулах холбоосоо шалгаад нэвтэрнэ үү.';await switchUser(result.data.session?.user || null);
  } catch(error){$('auth-feedback').textContent=error.message;}finally{buttons.forEach(b=>b.disabled=false);}
}
function populateSources(){for(const id of ['source','admin-source']){const chosen=$(id).value;$(id).replaceChildren();if(id==='source'){const option=el('option','','Бүгд');option.value='';$(id).append(option);}for(const source of getSources(data.problems,data.sources||[])){const option=el('option','',source);option.value=source;$(id).append(option);}$(id).value=[...$(id).options].some(o=>o.value===chosen)?chosen:(id==='source'?'':'Codeforces');}adminUI?.sourcesChanged();}
function populateTags(){const chosen=$('tag-filter').value;$('tag-filter').replaceChildren(el('option','','Бүх tags'));$('tag-filter').children[0].value='';for(const tag of getTags(data.problems)){const option=el('option','',tag);option.value=tag;$('tag-filter').append(option);}$('tag-filter').value=getTags(data.problems).includes(chosen)?chosen:'';}
async function refreshCatalog(){if(!client){catalogLoading=false;render();notice('Онлайн бодлогын сангийн холболт шаардлагатай.');return false;}catalogLoading=true;render();
 try{const document=parseCatalog(await rpc(client,'get_catalog'));data.problems=document.problems;data.sources=document.sources||[];for(const id of document.knownIds)catalogIds.add(id);try{localStorage.setItem('think-cp:online-catalog',JSON.stringify(document));}catch{}populateTags();populateSources();
  if(selectedProblem){selectedProblem=data.problems.find(p=>p.id===selectedProblem.id);if(selectedProblem)renderDetail();else $('detail').close();}social?.connected();return true;
 }catch(error){notice('Онлайн бодлогын сан шинэчлэгдсэнгүй. Одоогийн хуулбарыг харуулж байна. '+accountError(error));return false;}
 finally{catalogLoading=false;render();}
}
async function init() {
  const response=await fetch('./problems.json?v=16', {cache:'no-store'});if(!response.ok)throw new Error('Бодлогын санг ачаалж чадсангүй.');data=await response.json();catalogIds=new Set(data.problems.map(p=>p.id));catalogLoading=configured;
  try{const cached=parseCatalog(JSON.parse(localStorage.getItem('think-cp:online-catalog')||'null'));data.problems=cached.problems;data.sources=cached.sources||[];for(const id of cached.knownIds)catalogIds.add(id);}catch{}
  readLocal();render();updateAccount();
  populateTags();populateSources();
  try{hintLanguage=localStorage.getItem('think-cp:hint-language')==='en'?'en':'mn';}catch{}$('hint-language').value=hintLanguage;
  $('hint-language').onchange=()=>{hintLanguage=$('hint-language').value;try{localStorage.setItem('think-cp:hint-language',hintLanguage);}catch{}renderDetail();};
  $('refresh-catalog').onclick=()=>void refreshCatalog();
  try {const prefs=JSON.parse(localStorage.getItem('think-cp:catalog-preferences')||'{}');$('show-tags').checked=prefs.showTags===true;if(['rating-asc','rating-desc','priority','title','number-asc'].includes(prefs.sort))$('sort').value=prefs.sort;}catch{}
  const savePreferences=()=>{try{localStorage.setItem('think-cp:catalog-preferences',JSON.stringify({showTags:$('show-tags').checked,sort:$('sort').value}));}catch{}};
  for(const id of ['search','source','status-filter','tag-filter','rating-filter','min-rating','max-rating','priority-only'])$(id).addEventListener('input',render);
  for(const [id,delta] of [['problem-prev',-1],['problem-next',1]])$(id).onclick=()=>{problemPage+=delta;render();$('packs').scrollIntoView({block:'start'});};
  $('sort').addEventListener('change',()=>{savePreferences();render();});
  $('show-tags').addEventListener('change',()=>{savePreferences();render();if(selectedProblem)renderDetail();});
  $('reveal-detail-tags').onclick=()=>{detailTagsShown=!detailTagsShown;renderDetail();};
  $('reset-filters').onclick=()=>{selectedPack='';for(const id of ['search','source','status-filter','tag-filter','rating-filter','min-rating','max-rating'])$(id).value='';$('priority-only').checked=false;$('sort').value='rating-asc';savePreferences();render();};
  render();
  document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>$(b.dataset.close).close());
  $('account').onclick=()=>{updateAccount();$('auth').showModal();};
  tutorialUI=setupTutorials({client:()=>client,user:()=>user,learning:()=>learningUI});
  groupUI=setupGroups({client:()=>client,user:()=>user,openAccount:()=>{$('account').onclick();}});
  social=setupSocial({client:()=>client,user:()=>user,problems:()=>data.problems,openProblem,viewProfile:id=>{if(learningUI)location.hash='#profile/'+id;else void social?.openProfile(id);},openAccount:()=>{$('account').onclick();},notice});
  adminUI=setupAdmin({client:()=>client,user:()=>user,refreshCatalog,sources:()=>getSources(data.problems,data.sources||[])});
  try{learningUI=await setupLearning({client:()=>client,user:()=>user,profile:()=>myProfile,problems:()=>data.problems,progress:()=>state,openProblem,refreshCatalog,redraw:render,refreshDetail:renderDetail,refreshTutorialLibrary:()=>tutorialUI?.refreshStatus(),openAccount:()=>{$('account').onclick();},socialProfile:id=>social.openProfile(id)});tutorialUI.refreshLearning();render();}catch{for(const id of ['learning-profile-body','study-plan-body','learning-admin-body'])$(id).textContent='Сургалтын хэсэг түр ачаалсангүй. Хуудсаа дахин ачаална уу.';}
  try{const density=localStorage.getItem('erdene:problem-density');$('problem-density').value=density==='compact'?'compact':'comfortable';}catch{}$('problem-density').onchange=()=>{try{localStorage.setItem('erdene:problem-density',$('problem-density').value);}catch{}render();};render();
  $('avatar-file').onchange=()=>{if(avatarPreviewUrl)URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;const file=$('avatar-file').files?.[0];if(file){avatarPreviewUrl=URL.createObjectURL(file);$('remove-avatar').checked=false;}renderOwnAvatar();};
  $('remove-avatar').onchange=()=>{if($('remove-avatar').checked){$('avatar-file').value='';if(avatarPreviewUrl)URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;$('own-avatar').hidden=true;$('own-avatar-fallback').hidden=false;}else renderOwnAvatar();};
  $('profile-form').onsubmit=event=>void saveProfile(event);
  $('reload-profile').onclick=()=>void loadProfile();
  $('refresh-solvers').onclick=()=>void loadSolvers();$('more-solvers').onclick=()=>void loadSolvers(true);
  $('detail').addEventListener('close',()=>{solverRequest++;selectedProblem=null;});
  $('problem-status').onchange=()=>{setEntry(selectedProblem.id,{status:$('problem-status').value});renderDetail();};
  $('toggle-hints').onclick=()=>{const id=selectedProblem.id;if(hiddenHints.has(id))hiddenHints.delete(id);else hiddenHints.add(id);renderDetail();};
  $('next-hint').onclick=()=>{if(!selectedProblem.hints?.length)return;hiddenHints.delete(selectedProblem.id);const e=entry(selectedProblem.id);setEntry(selectedProblem.id,{hints:Math.min(e.hints+1,selectedProblem.hints.length),status:e.status==='new'?'trying':e.status});renderDetail();};
  $('save-note').onclick=()=>{setEntry(selectedProblem.id,{notes:$('notes').value});$('detail-feedback').textContent='Тэмдэглэлийг progress-д нэмлээ. Хадгалалтын төлөвийг үндсэн хуудаснаас харна уу.';};
  $('export').onclick=()=>{const blob=new Blob([JSON.stringify({version:1,progress:state},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download='erdene-club-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  $('import').onchange=async event=>{
    const file=event.target.files[0],turn=epoch;if(!file)return;
    try {if(loading)throw new Error('Account ачаалагдаж байна. Түр хүлээгээд дахин сонгоно уу.');if(file.size>2_000_000)throw new Error('Файл хэт том байна.');const imported=parseBackup(JSON.parse(await file.text()),catalogIds);if(turn!==epoch)throw new Error('Account солигдлоо. Файлаа дахин сонгоно уу.');if(!confirm('Файлд байгаа бодлогуудын progress-ийг сэргээх үү? Одоогийн ижил бодлогын төлөв солигдоно.'))return;for(const [id,e] of Object.entries(imported)){state[id]=e;dirty[id]=e;delete activityPending[id];}const saved=persist();render();if(saved)notice('Progress сэргээгдлээ.');void sync();}
    catch(error){notice(error.message);}finally{event.target.value='';}
  };
  $('auth-form').onsubmit=event=>{event.preventDefault();void authAction(false);};$('signup').onclick=()=>void authAction(true);
  $('signout').onclick=async()=>{if(syncing){$('auth-feedback').textContent='Хадгалалт дуусахыг хүлээгээрэй.';return;}const {error}=await client.auth.signOut();if(error){$('auth-feedback').textContent=error.message;return;}await switchUser(null);$('auth-feedback').textContent='Account-аас гарлаа.';};
  $('retry-sync').onclick=()=>void sync();window.addEventListener('online',()=>void sync());
  if(configured) {
    try {
      const {createClient}=await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm');client=createClient(cfg.supabaseUrl,cfg.supabaseKey);
      client.auth.onAuthStateChange((event,session)=>{social.authEvent(event,session);setTimeout(()=>void switchUser(session?.user || null),0);});
      await refreshCatalog();
      const {data:sessionData,error}=await client.auth.getSession();if(error)throw error;await switchUser(sessionData.session?.user || null);updateAccount();social.connected();adminUI.connected();tutorialUI.connected();groupUI.connected();
    } catch(error){client=null;catalogLoading=false;render();updateAccount();notice('Account холболт ажилласангүй: '+error.message);}
  }
}
init().catch(error=>{$('problems').textContent=error.message;notice('Хуудсаа дахин ачаалаарай.');});
