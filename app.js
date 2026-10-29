import {setupAdminProfiles} from './admin-profile.js?v=52';
import {createLearningStore} from './learning-store.js?v=52';
import {setupProblemStatement} from './problem-statement.js?v=67';
import {setupProblemEditorial} from './problem-editorial.js?v=67';
import {appendHintText} from './hint-content.js?v=52';
import {canonicalProblemUrl} from './problem-url.js?v=52';
import {priorityLevel,priorityLabel,isHighPriority,ratingClass} from './priority.js?v=52';
import {setupLearning} from './learning.js?v=67';
import {setupTutorials,typeset} from './tutorials.js?v=67';
import {setupGroups} from './groups.js?v=52';
let tutorialUI, learningUI=null,hintRenderTurn=0,problemEditorialUI,problemStatementUI,learningProgressStore;
import {CURRENT_EMPTY,cleanProgress,parseCurrentBackup,progressRows} from './progress.js?v=52';
import {getSolvers} from './community.js?v=52';
import {setupAdmin} from './admin.js?v=67';
import {parseCatalog,hintTexts,getSources} from './problem-store.js?v=63';
import {rpc} from './accounts.js?v=52';
import {ownProfile,saveOwnProfile,avatarUrl,accountError} from './accounts.js?v=52';
import {setupSocial} from './social.js?v=52';
import {filterProblems, getTags, ratingLabel,difficultyLabel} from './catalog.js?v=52';
const $ = id => document.getElementById(id);
const STATUS = {new:'Эхлээгүй',trying:'Оролдож байгаа',solved:'Бодсон'};
let data, selectedProblem, state={}, dirty={}, user=null, client=null, loading=false, syncing=false, syncAgain=false, epoch=0;
let username=null, profileLoading=false, profileSaving=false, solverRequest=0, solverNames=[], solverTotal=0;
let detailTagsShown=false,hintPanelOpen=false,revealedHintCount=0,problemPage=0,lastFilterKey='',activityPending={},problemAdminAllowed=false,previousProblemHash=location.hash;
const PROBLEMS_PER_PAGE=100;
const hiddenHints=new Set();
let adminProfileUI=null,social=null, adminUI=null, groupUI=null, myProfile=null, avatarPreviewUrl=null, catalogLoading=false;
let catalogIds=new Set(),hintLanguage='mn';
const cfg=window.THINK_CP_CONFIG || {};
const configured=Boolean(cfg.supabaseUrl && cfg.supabaseKey);
const key=()=> 'think-cp:v2:'+(user?.id || 'guest');
function notice(message) { $('notice').textContent=message; }
const validProgressId=id=>typeof id==='string'&&/^[a-zA-Z0-9][a-zA-Z0-9_-]{0,99}$/.test(id)&&!['constructor','prototype'].includes(id);
function readLocal() {
  state={};dirty={};activityPending={};let damaged=false;
  const read=name=>{try{const value=JSON.parse(localStorage.getItem(name)||'{}');return value&&typeof value==='object'?value:{};}catch{damaged=true;return{};}};
  const legacy=read('think-cp:v1:'+(user?.id||'guest')),current=read(key());
  for(const saved of [legacy,current])for(const[id,value]of Object.entries(saved.progress||{})){if(!validProgressId(id))continue;try{state[id]=cleanProgress(value);}catch{damaged=true;}}
  for(const id of Array.isArray(legacy.dirty)?legacy.dirty:[])if(state[id]&&!Object.hasOwn(current.progress||{},id))dirty[id]=state[id];
  for(const id of Array.isArray(current.dirty)?current.dirty:[])if(state[id])dirty[id]=state[id];
  for(const id of Array.isArray(current.activityPending)?current.activityPending:[])if(validProgressId(id)&&dirty[id])activityPending[id]={};
  if(damaged)notice('Зарим progress-ийн хуулбарыг уншиж чадсангүй. Хүчинтэй төлөв, тэмдэглэлийг хадгаллаа.');
}
function persist() {
  try {localStorage.setItem(key(),JSON.stringify({progress:state,dirty:Object.keys(dirty),activityPending:Object.keys(activityPending)}));return true;}
  catch {notice('Browser хадгалалт боломжгүй байна. Хуудсаа хаахаас өмнө progress-оо татаж аваарай.');return false;}
}
function entry(id) {return state[id] || {...CURRENT_EMPTY};}
function setEntry(id, patch) {if(loading)return; const before=entry(id).status;state[id]=cleanProgress({...entry(id),...patch});if(learningUI)learningUI.progressChanged(id,before,state[id].status);else learningProgressStore?.recordTransition(id,before,state[id].status);if(before!==state[id].status){if(['trying','solved'].includes(state[id].status))activityPending[id]={};else delete activityPending[id];}dirty[id]=state[id];const saved=persist();render();if(user)void sync();else if(saved)notice('Progress энэ browser-т хадгалагдлаа.');}
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
  const filters={query:$('search').value,source:$('source').value,status:$('status-filter').value,tag:$('tag-filter').value,minRating:$('min-rating').value,maxRating:$('max-rating').value,priorityLevel:$('priority-filter').value,sort:$('sort').value};
  const filterKey=JSON.stringify(filters);if(filterKey!==lastFilterKey){problemPage=0;lastFilterKey=filterKey;}
  $('problems').classList.toggle('compact',$('problem-density').value==='compact');$('problems').classList.toggle('minimalist',$('problem-density').value==='minimalist');$('problems').replaceChildren();
  const invalidRange=!$('min-rating').checkValidity()||!$('max-rating').checkValidity()||($('min-rating').value!==''&&$('max-rating').value!==''&&Number($('min-rating').value)>Number($('max-rating').value));
  const filtered=invalidRange?[]:filterProblems(data.problems,state,filters);
  $('results-count').textContent=filtered.length+' / '+data.problems.length+' бодлого';
  const pageCount=Math.ceil(filtered.length/PROBLEMS_PER_PAGE);problemPage=Math.max(0,Math.min(problemPage,pageCount-1));
  const start=problemPage*PROBLEMS_PER_PAGE,end=Math.min(start+PROBLEMS_PER_PAGE,filtered.length);
  $('problem-prev').disabled=problemPage===0||!pageCount;$('problem-next').disabled=!pageCount||problemPage>=pageCount-1;
  $('problem-page').textContent=pageCount?(problemPage+1)+' / '+pageCount+' хуудас · '+(start+1)+'–'+end+' / '+filtered.length+' бодлого':'0 бодлого';
  $('rating-range-message').textContent=invalidRange?'Rating хязгаар 0–4000 бүхэл тоо байна. Min rating нь Max rating-аас их байж болохгүй.':'';
  for(const p of filtered.slice(start,end)) {
    const row=el('article','problem'+(isHighPriority(p)?' is-priority':'')), n=el('span','number','#'+String(p.number).padStart(3,'0')), b=el('button','open');b.disabled=loading||catalogLoading;
    const heading=el('h3','',p.title);
    if(isHighPriority(p)){const star=el('span','priority-star','★');star.title='Priority бодлого';star.setAttribute('aria-label','Priority');heading.prepend(star);}
    const meta=el('div','problem-meta');const rating=el('span','rating '+ratingClass(p),ratingLabel(p));rating.title=p.ratingKind==='unrated'?'Түвшин тогтоогоогүй':p.ratingKind==='official'?'Codeforces-ийн албан rating':(($('show-tags').checked||entry(p.id).status==='solved')&&p.ratingBasis?p.ratingBasis:'Зохиогчийн CF difficulty-ийн estimate; official биш');
    meta.append(rating,el('span','priority-badge priority-'+priorityLevel(p),priorityLabel(p)),el('small','',p.source+' · '+p.ref+' · '+difficultyLabel(p)+(p.level==='Interactive'?' · Interactive':'')));
    b.dataset.problemId=p.id;b.append(heading,meta);b.onclick=()=>openProblem(p);
    {const tags=el('div','tag-chips');if($('show-tags').checked||entry(p.id).status==='solved'){for(const tag of p.tags)tags.append(el('span','tag-chip',tag));tags.title=p.tags.join(' · ');}else tags.append(el('span','muted','Сэдэв нуусан'));b.append(tags);}
    const badge=el('span','badge '+entry(p.id).status,STATUS[entry(p.id).status]);
    const arrow=el('button','arrow','↗');arrow.setAttribute('aria-label',p.title+' нээх');arrow.disabled=loading||catalogLoading;arrow.onclick=()=>openProblem(p);
    const signals=el('div','problem-signals');signals.append(badge);
    row.append(n,b,signals,arrow);const learningLinks=el('div','problem-learning-links');for(const t of ($('show-tags').checked||entry(p.id).status==='solved'?learningUI?.linksForProblem(p)||[]:[])){const a=el('a','',(t.primary?'Үндсэн · ':'')+t.title);a.href='#tutorial/'+t.id;learningLinks.append(a);}const days=learningUI?.planDaysFor(p)||[];if(days.length){const a=el('a','','Өдөр '+days.slice(0,3).join(', ')+(days.length>3?'…':''));a.href='#plan/'+days[0];learningLinks.append(a);}if(learningLinks.children.length)row.append(learningLinks);$('problems').append(row);
  }
  if(!filtered.length)$('problems').append(el('p','muted','Тохирох бодлого олдсонгүй. Шүүлтүүрээ өөрчлөөрэй.'));
}
const problemFilterIds=['search','source','status-filter','tag-filter','min-rating','max-rating','priority-filter','sort','problem-density'];
function currentProblemId(){try{const m=/^#problem\/([^/]+)\/?$/.exec(location.hash);return m?decodeURIComponent(m[1]):null;}catch{return null;}}
function problemPageActive(){return !!selectedProblem&&currentProblemId()===selectedProblem.id&&!$('detail').hidden;}
function problemSnapshot(){return{hash:location.hash||'#library',scroll:scrollY,page:problemPage,filters:Object.fromEntries(problemFilterIds.map(id=>[id,$(id).value])),showTags:$('show-tags').checked,problemId:selectedProblem?.id};}
function openProblem(p){
 const hash='#problem/'+encodeURIComponent(p.id);if(location.hash===hash){showProblemPage(p);return;}
 const origin={...problemSnapshot(),problemId:p.id};history.replaceState({...history.state,erdeneProblemReturn:origin},'');history.pushState({erdeneProblemOrigin:origin},'',hash);window.dispatchEvent(new HashChangeEvent('hashchange'));
}
function resetHintView(){revealedHintCount=0;hiddenHints.clear();hintPanelOpen=false;}
function leaveProblem(){resetHintView();solverRequest++;selectedProblem=null;hintRenderTurn++;problemEditorialUI?.clear();problemStatementUI?.clear();try{window.MathJax?.typesetClear?.([$ ('hint-list')]);}catch{}$('hint-list').replaceChildren();}
function syncProblemRoute(){
 const previous=previousProblemHash;previousProblemHash=location.hash;
 if(!/^#problem\//.test(location.hash)){
  leaveProblem();const back=history.state?.erdeneProblemReturn;if(/^#problem\//.test(previous)&&back&&back.hash===location.hash){
   if(location.hash==='#library'&&back.filters){for(const id of problemFilterIds){const value=back.filters[id];if(typeof value==='string'&&value.length<=1000)$(id).value=value;}$('show-tags').checked=back.showTags===true;render();problemPage=Number.isInteger(back.page)?Math.max(0,back.page):0;render();}
   requestAnimationFrame(()=>{window.scrollTo({top:Math.max(0,Number(back.scroll)||0),behavior:'instant'});if(location.hash==='#library')document.querySelector('#problems [data-problem-id="'+CSS.escape(back.problemId||'')+'"]')?.focus({preventScroll:true});});
  }return;
 }
 const id=currentProblemId(),p=data?.problems.find(p=>p.id===id)||data?.problems.find(p=>String(p.number)===id);
 if(p){if(id!==p.id){history.replaceState(history.state,'','#problem/'+encodeURIComponent(p.id));}showProblemPage(p);return;}
 leaveProblem();$('problem-share').disabled=true;$('problem-admin-edit').hidden=true;$('detail-title').textContent=catalogLoading?'Бодлого ачаалж байна…':'Бодлого олдсонгүй';$('detail-source').textContent='БОДЛОГЫН САН';$('detail-note').replaceChildren();$('problem-detail-body').hidden=true;$('problem-retry').hidden=catalogLoading;$('problem-route-state').textContent=catalogLoading?'Онлайн санг шалгаж байна…':'Энэ бодлого байхгүй эсвэл жагсаалтаас хасагдсан байж болно. ID-г шалгах эсвэл жагсаалт руу буцна уу.';
}
function showProblemPage(p) {$('problem-share').disabled=false;$('problem-back').textContent=history.state?.erdeneProblemOrigin?.hash&&history.state.erdeneProblemOrigin.hash!=='#library'?'← Буцах':'← Бодлогын жагсаалт';const changed=selectedProblem?.id!==p.id;selectedProblem=p;if(changed){detailTagsShown=false;resetHintView();}$('problem-detail-body').hidden=false;$('problem-route-state').textContent='';$('problem-retry').hidden=true;$('detail-title').textContent=(isHighPriority(p)?'★ ':'')+p.title;$('detail-source').textContent='#'+p.number+' · '+p.source+' · '+p.ref;$('detail-note').textContent=(p.ratingKind==='unrated'?'Үнэлгээгүй':p.ratingKind==='official'?'CF албан rating':'CF difficulty-ийн баримжаа'+(p.ratingConfidence==='rough'?' · Урьдчилсан үнэлгээ':''))+(p.level==='Interactive'?' · Interactive':'')+(p.source==='EGOI'?' · Full task; subtask-аас эхэл':'')+' · '+priorityLabel(p);const detailRating=el('span','rating '+ratingClass(p),ratingLabel(p));$('detail-note').prepend(detailRating,document.createTextNode(' · '));$('problem-link').href=p.url;if(changed)$('notes').value=entry(p.id).notes;$('detail-feedback').textContent='';document.title=p.title+' — Erdene Club';renderDetail();if(changed){void loadSolvers();requestAnimationFrame(()=>$('detail-title').focus({preventScroll:true}));}}
function renderDetail() {
  if(!selectedProblem)return;problemEditorialUI?.render(selectedProblem);problemStatementUI?.render(selectedProblem);const p=selectedProblem,e=entry(p.id),tagsVisible=$('show-tags').checked||detailTagsShown||e.status==='solved',learningLinks=$('detail-learning-links');learningLinks.replaceChildren();if(tagsVisible){for(const t of learningUI?.linksForProblem(p)||[]){const a=el('a','',(t.primary?'Үндсэн · ':'')+t.title);a.href='#tutorial/'+t.id;learningLinks.append(a);}}learningUI?.renderProblemLinks(p,learningLinks);const hintCount=hintTexts(p,'mn').length;$('hint-list').closest('.hints').hidden=priorityLevel(p)==='low'||!hintPanelOpen;$('problem-hints-button').hidden=priorityLevel(p)==='low'||!hintCount;$('problem-hints-button').setAttribute('aria-expanded',String(hintPanelOpen));$('problem-editorial-button').hidden=!p.hasEditorial&&!p.editorial;$('problem-admin-edit').hidden=!problemAdminAllowed;$('hint-language').closest('label').hidden=!hintCount;$('problem-status').value=e.status;$('problem-status').disabled=loading;$('notes').disabled=loading;$('save-note').disabled=loading;const hintTurn=++hintRenderTurn;try{window.MathJax?.typesetClear?.([$ ('hint-list')]);}catch{}const hintBody=el('div','hint-render-body');$('hint-list').replaceChildren(hintBody);
  hintTexts(p,hintLanguage).slice(0,revealedHintCount).forEach((hint,i)=>{const h=el('div','hint');const text=el('span');appendHintText(text,hint);h.append(el('b','','HINT '+(i+1)),text);hintBody.append(h);});
  const hintsVisible=!hiddenHints.has(p.id);
  $('hint-list').hidden=!hintsVisible;
  $('toggle-hints').hidden=!hintCount||revealedHintCount===0;
  $('toggle-hints').textContent=hintsVisible?'Hint-үүдийг нуух':'Нээсэн hint-үүдийг харуулах';
  $('toggle-hints').setAttribute('aria-expanded',String(hintsVisible&&revealedHintCount>0));
  $('next-hint').hidden=revealedHintCount>=hintCount;$('next-hint').textContent='Дараагийн hint нээх';$('reflection').hidden=e.status!=='solved';$('tags').textContent=tagsVisible?'Сэдэв: '+p.tags.join(' · '):'';$('lesson').textContent=e.status==='solved'?p.lesson||'':'';$('lesson').hidden=!p.lesson;
  $('problem-topics-hidden').hidden=tagsVisible;$('tags').hidden=!tagsVisible;$('detail-tags').hidden=!tagsVisible;$('detail-tags').replaceChildren();if(tagsVisible)for(const tag of p.tags)$('detail-tags').append(el('span','tag-chip',tag));
  $('reveal-detail-tags').hidden=$('show-tags').checked||e.status==='solved';$('reveal-detail-tags').textContent=detailTagsShown?'Tags нуух':'Tags харуулах';
  $('editorial-link').hidden=!p.editorialUrl;if(p.editorialUrl)$('editorial-link').href=p.editorialUrl;
  if(hintCount&&revealedHintCount>0&&hintsVisible){const id=p.id,language=hintLanguage,target=hintBody;void typeset([target],undefined,()=>hintTurn===hintRenderTurn&&selectedProblem?.id===id&&hintLanguage===language&&problemPageActive()&&priorityLevel(selectedProblem)!=='low'&&target.isConnected).catch(()=>{if(hintTurn===hintRenderTurn)$('detail-feedback').textContent='Томъёог одоогоор дүрсэлж чадсангүй; эх бичвэр хэвээр байна.';});}

}
async function switchUser(next) {
  if(user?.id===next?.id)return;
  const turn=++epoch;user=next;adminProfileUI?.accountChanged();username=null;myProfile=null;if(avatarPreviewUrl){URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;}for(const id of ['full-name','first-name','last-name','school','avatar-file'])$(id).value='';$('legacy-name-note').textContent='';$('remove-avatar').checked=false;renderOwnAvatar();profileLoading=false;profileSaving=false;$('username').value='';$('profile-feedback').textContent='';loading=!!user;resetHintView();problemStatementUI?.clear();problemEditorialUI?.clear();readLocal();void learningProgressStore?.accountChanged();render();updateAccount();if(selectedProblem){$('notes').value=entry(selectedProblem.id).notes;renderDetail();void loadSolvers();}
  if(user) {
    void loadProfile();
    try {
      const {data:rows,error}=await client.from('progress').select('problem_id,status,notes').eq('user_id',user.id);
      if(error)throw error;if(turn!==epoch)return;
      const remote={};for(const row of rows)if(validProgressId(row.problem_id))remote[row.problem_id]=cleanProgress(row);
      state={...remote,...dirty};persist();notice('Account-ын progress ачаалагдлаа.');
    } catch(error) {if(turn===epoch)notice('Онлайн progress ачаалагдсангүй. Энэ төхөөрөмжийн хуулбарыг ашиглаж байна: '+error.message);}
    finally {if(turn===epoch){loading=false;render();if(selectedProblem){$('notes').value=entry(selectedProblem.id).notes;renderDetail();}void sync();}}
  } else {notice('Зочин горим. Progress энэ browser-т хадгалагдана.');}
}
async function sync() {
  if(!user || !client || loading)return;
  if(syncing){syncAgain=true;return;}if(!Object.keys(dirty).length)return;
  syncing=true;const turn=epoch,uid=user.id, batch={...dirty},activityBatch={...activityPending};notice('Онлайнаар хадгалж байна…');
  try {
    let result=await client.from('progress').upsert(progressRows(uid,batch,activityBatch),{onConflict:'user_id,problem_id',defaultToNull:false});
    if(result.error&&String(result.error.message).includes('record_activity')&&['PGRST204','42703'].includes(result.error.code))result=await client.from('progress').upsert(progressRows(uid,batch).map(({record_activity,...row})=>row),{onConflict:'user_id,problem_id',defaultToNull:false});
    if(result.error)throw result.error;if(turn!==epoch)return;
    for(const id of Object.keys(batch)){if(dirty[id]===batch[id])delete dirty[id];if(activityPending[id]===activityBatch[id])delete activityPending[id];}persist();notice(Object.keys(dirty).length?'Өөрчлөлтийг хадгалж байна…':'Онлайн progress хадгалагдлаа.');
    if(problemPageActive() && batch[selectedProblem?.id])void loadSolvers();learningUI?.profileUpdated();
  } catch(error) {if(turn===epoch)notice('Онлайн хадгалалт амжилтгүй. Browser-т хадгалсан; дахин оролдох боломжтой. '+error.message);}
  finally {syncing=false;updateAccount();if(syncAgain){syncAgain=false;void sync();}}
}
function renderOwnAvatar() {
  const url=avatarPreviewUrl||avatarUrl(client,myProfile);$('own-avatar').hidden=!url;if(url)$('own-avatar').src=url;else $('own-avatar').removeAttribute('src');$('own-avatar-fallback').hidden=!!url;$('own-avatar-fallback').textContent=((myProfile?.full_name||myProfile?.username||'?')[0]||'?').toUpperCase();
}
function updateAccount() {
  social?.accountChanged();adminProfileUI?.accountChanged();adminUI?.accountChanged();tutorialUI?.accountChanged();groupUI?.accountChanged();learningUI?.accountChanged();
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
  if(!selectedProblem || !problemPageActive())return;
  const request=++solverRequest, pid=selectedProblem.id, turn=epoch, offset=append?solverNames.length:0;
  if(!append){solverNames=[];solverTotal=0;$('solver-list').replaceChildren();$('solver-count').textContent='';}
  $('more-solvers').hidden=true;$('refresh-solvers').disabled=true;
  if(!client){$('solvers-message').textContent='Бодсон хүмүүсийг харахад онлайн холболт шаардлагатай.';$('refresh-solvers').disabled=false;return;}
  $('solvers-message').textContent='Бодсон хүмүүсийг ачаалж байна…';
  try {
    const result=await getSolvers(client,pid,offset);
    if(request!==solverRequest||turn!==epoch||selectedProblem?.id!==pid||!problemPageActive())return;
    solverNames=[...new Set([...solverNames,...result.names])];solverTotal=result.total||solverNames.length;
    $('solver-list').replaceChildren();for(const name of solverNames){const li=el('li',name===username?'mine':''),button=el('button','','@'+name+(name===username?' · чи':''));button.onclick=()=>{void social?.byUsername(name);};li.append(button);$('solver-list').append(li);}
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
    if(result.error)throw result.error;$('password').value='';$('auth-feedback').textContent=result.data.session?'Амжилттай нэвтэрлээ.':'Баталгаажуулах email дээрх холбоос дээр дарна уу.';await switchUser(result.data.session?.user || null);
  } catch(error){$('auth-feedback').textContent=error.message;}finally{buttons.forEach(b=>b.disabled=false);}
}
function populateSources(){for(const id of ['source','admin-source']){const chosen=$(id).value;$(id).replaceChildren();if(id==='source'){const option=el('option','','Бүгд');option.value='';$(id).append(option);}for(const source of getSources(data.problems,data.sources||[])){const option=el('option','',source);option.value=source;$(id).append(option);}$(id).value=[...$(id).options].some(o=>o.value===chosen)?chosen:(id==='source'?'':'Codeforces');}adminUI?.sourcesChanged();}
function populateTags(){const chosen=$('tag-filter').value;$('tag-filter').replaceChildren(el('option','','Бүх tags'));$('tag-filter').children[0].value='';for(const tag of getTags(data.problems)){const option=el('option','',tag);option.value=tag;$('tag-filter').append(option);}$('tag-filter').value=getTags(data.problems).includes(chosen)?chosen:'';}
async function refreshCatalog(){if(!client){catalogLoading=false;render();notice('Онлайн бодлогын сангийн холболт шаардлагатай.');return false;}catalogLoading=true;render();
 try{const document=parseCatalog(await rpc(client,'get_catalog'));data.problems=document.problems;data.sources=document.sources||[];for(const id of document.knownIds)catalogIds.add(id);try{localStorage.setItem('think-cp:online-catalog',JSON.stringify(document));}catch{}populateTags();populateSources();
  syncProblemRoute();social?.connected();return true;
 }catch(error){notice('Онлайн бодлогын сан шинэчлэгдсэнгүй. Одоогийн хуулбарыг харуулж байна. '+accountError(error));return false;}
 finally{catalogLoading=false;render();syncProblemRoute();}
}
async function init() {
  const filterPanel=$('catalog-filter-panel'),smallScreen=matchMedia('(max-width:700px)');if(filterPanel){filterPanel.open=!smallScreen.matches;smallScreen.addEventListener('change',event=>{filterPanel.open=!event.matches;});}

  data={problems:[],sources:[]};catalogLoading=configured;
  // Configured clients use the authoritative catalog, without first downloading
  // a seed that cannot be used until that request completes.
  if(!configured){const response=await fetch('./problems.json?v=16',{cache:'no-store'});if(!response.ok)throw new Error('Бодлогын санг ачаалж чадсангүй.');data=await response.json();data.problems=data.problems.map(p=>({...p,url:canonicalProblemUrl(p.url)}));}
  catalogIds=new Set(data.problems.map(p=>p.id));
  try{const cached=parseCatalog(JSON.parse(localStorage.getItem('think-cp:online-catalog')||'null'));data.problems=cached.problems;data.sources=cached.sources||[];for(const id of cached.knownIds)catalogIds.add(id);}catch{}
  learningProgressStore=createLearningStore({client:()=>client,user:()=>user,message:text=>{if($('learning-save-status'))$('learning-save-status').textContent=text;if($('learning-retry-save'))$('learning-retry-save').hidden=!user;}},()=>learningUI?.storeChanged());void learningProgressStore.accountChanged();
  readLocal();render();updateAccount();
  populateTags();populateSources();
  $('hint-language').value=hintLanguage;
  $('hint-language').onchange=()=>{hintLanguage=$('hint-language').value;renderDetail();};
  $('refresh-catalog').onclick=()=>void refreshCatalog();
  try {const prefs=JSON.parse(localStorage.getItem('think-cp:catalog-preferences')||'{}');$('show-tags').checked=prefs.showTags===true;if(['rating-asc','rating-desc','priority','title','number-asc'].includes(prefs.sort))$('sort').value=prefs.sort;}catch{}
  const savePreferences=()=>{try{localStorage.setItem('think-cp:catalog-preferences',JSON.stringify({showTags:$('show-tags').checked,sort:$('sort').value}));}catch{}};
  savePreferences(); // Discard obsolete priority-only preference keys; explicit level filtering stays visible.
  for(const id of ['search','source','status-filter','tag-filter','min-rating','max-rating','priority-filter'])$(id).addEventListener('input',render);
  for(const [id,delta] of [['problem-prev',-1],['problem-next',1]])$(id).onclick=()=>{problemPage+=delta;render();$('library').scrollIntoView({block:'start'});};
  $('sort').addEventListener('change',()=>{savePreferences();render();});
  $('show-tags').addEventListener('change',()=>{detailTagsShown=false;savePreferences();render();if(selectedProblem)renderDetail();});
  $('reveal-detail-tags').onclick=()=>{detailTagsShown=!detailTagsShown;renderDetail();};
  $('reset-filters').onclick=()=>{for(const id of ['search','source','status-filter','tag-filter','min-rating','max-rating','priority-filter'])$(id).value='';$('sort').value='rating-asc';savePreferences();render();};
  render();
  document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>$(b.dataset.close).close());
  $('problem-back').onclick=()=>{if(history.state?.erdeneProblemOrigin&&history.length>1)history.back();else location.hash='#library';};
  $('problem-retry').onclick=()=>location.reload();
  $('problem-hints-button').onclick=()=>{if(!selectedProblem||priorityLevel(selectedProblem)==='low')return;hintPanelOpen=!hintPanelOpen;renderDetail();if(hintPanelOpen){$('problem-hints-panel').scrollIntoView({block:'start'});$('problem-hints-panel').focus({preventScroll:true});}};
  $('problem-solvers-button').onclick=()=>{$('solver-list').closest('section').scrollIntoView({block:'start'});$('refresh-solvers').focus({preventScroll:true});};
  $('problem-editorial-button').onclick=()=>{const details=$('problem-editorial').querySelector('details');if(details){details.open=true;details.scrollIntoView({block:'start'});details.querySelector('summary').focus({preventScroll:true});}};
  $('problem-admin-edit').onclick=()=>{if(selectedProblem)adminUI?.editProblem(selectedProblem.id);};
  window.addEventListener('erdene-admin',e=>{problemAdminAllowed=e.detail===true;$('problem-admin-edit').hidden=!problemAdminAllowed;});
  $('problem-share').onclick=async()=>{if(!selectedProblem)return;const url=location.origin+location.pathname+'#problem/'+encodeURIComponent(selectedProblem.id);try{await navigator.clipboard.writeText(url);$('problem-share-message').textContent='Бодлогын холбоос хуулагдлаа.';}catch{$('problem-share-url').hidden=false;$('problem-share-url').value=url;$('problem-share-url').select();$('problem-share-message').textContent='Холбоосыг сонгон хуулна уу.';}};
  window.addEventListener('hashchange',syncProblemRoute);
  $('account').onclick=()=>{updateAccount();$('auth').showModal();};
  groupUI=setupGroups({client:()=>client,user:()=>user,openAccount:()=>{$('account').onclick();}});
  problemStatementUI=setupProblemStatement($('problem-statement'),{client:()=>client,user:()=>user,active:id=>selectedProblem?.id===id&&problemPageActive()});
  problemEditorialUI=setupProblemEditorial($('problem-editorial'),{client:()=>client,user:()=>user,active:id=>selectedProblem?.id===id&&problemPageActive()});
  social=setupSocial({client:()=>client,user:()=>user,problems:()=>data.problems,openProblem,viewProfile:id=>{if(learningUI)location.hash='#profile/'+id;else void social?.openProfile(id);},openAccount:()=>{$('account').onclick();},notice});
  adminUI=setupAdmin({progress:()=>state,client:()=>client,user:()=>user,refreshCatalog,sources:()=>getSources(data.problems,data.sources||[])});
  adminProfileUI=setupAdminProfiles($('admin-users'),{enabled:cfg.adminProfileEditorEnabled===true,client:()=>client,user:()=>user,navigation:allowed=>{$('admin-users-link').hidden=!allowed;},saved:profile=>{if(profile.user_id===user?.id)void loadProfile();social?.connected();}});
  let studyStarted=false;
  function startStudy(){if(studyStarted)return;studyStarted=true;
  tutorialUI=setupTutorials({requiresOnline:configured,problems:()=>data.problems,progress:()=>state,client:()=>client,user:()=>user,learning:()=>learningUI});
  void setupLearning({learningStore:learningProgressStore,isAdmin:()=>problemAdminAllowed,client:()=>client,user:()=>user,profile:()=>myProfile,problems:()=>data.problems,progress:()=>state,openProblem,refreshCatalog,redraw:render,refreshDetail:renderDetail,refreshTutorialLibrary:()=>tutorialUI?.refreshStatus(),openAccount:()=>{$('account').onclick();},socialProfile:id=>social.openProfile(id)}).then(ui=>{learningUI=ui;learningUI.accountChanged();tutorialUI.refreshLearning();render();if(selectedProblem)renderDetail();}).catch(()=>{for(const id of ['learning-profile-body','study-plan-body','learning-admin-body'])$(id).textContent='Сургалтын хэсэг түр ачаалсангүй. Хуудсаа дахин ачаална уу.';});
  }
  const studyRoute=()=>/^#(?:tutorial|plan|profile|learning-admin)/.test(location.hash)||location.hash==='#admin-tutorials';
  if(!configured||studyRoute())startStudy();window.addEventListener('hashchange',()=>{if(studyRoute())startStudy();});
  try{const density=localStorage.getItem('erdene:problem-density');$('problem-density').value=['comfortable','compact','minimalist'].includes(density)?density:'comfortable';}catch{}$('problem-density').onchange=()=>{try{localStorage.setItem('erdene:problem-density',$('problem-density').value);}catch{}render();};render();
  $('avatar-file').onchange=()=>{if(avatarPreviewUrl)URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;const file=$('avatar-file').files?.[0];if(file){avatarPreviewUrl=URL.createObjectURL(file);$('remove-avatar').checked=false;}renderOwnAvatar();};
  $('remove-avatar').onchange=()=>{if($('remove-avatar').checked){$('avatar-file').value='';if(avatarPreviewUrl)URL.revokeObjectURL(avatarPreviewUrl);avatarPreviewUrl=null;$('own-avatar').hidden=true;$('own-avatar-fallback').hidden=false;}else renderOwnAvatar();};
  $('profile-form').onsubmit=event=>void saveProfile(event);
  $('reload-profile').onclick=()=>void loadProfile();
  $('refresh-solvers').onclick=()=>void loadSolvers();$('more-solvers').onclick=()=>void loadSolvers(true);
  $('problem-status').onchange=()=>{setEntry(selectedProblem.id,{status:$('problem-status').value});renderDetail();};
  $('toggle-hints').onclick=()=>{const id=selectedProblem.id;if(hiddenHints.has(id))hiddenHints.delete(id);else hiddenHints.add(id);renderDetail();};
  $('next-hint').onclick=()=>{if(!selectedProblem||!problemPageActive()||priorityLevel(selectedProblem)==='low'||!selectedProblem.hints?.length)return;hiddenHints.delete(selectedProblem.id);revealedHintCount=Math.min(revealedHintCount+1,selectedProblem.hints.length);renderDetail();};
  $('save-note').onclick=()=>{setEntry(selectedProblem.id,{notes:$('notes').value});$('detail-feedback').textContent='Тэмдэглэлийг progress-д нэмлээ. Хадгалалтын төлөвийг үндсэн хуудаснаас харна уу.';};
  $('export').onclick=()=>{const blob=new Blob([JSON.stringify({version:2,progress:state},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download='erdene-club-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  $('import').onchange=async event=>{
    const file=event.target.files[0],turn=epoch;if(!file)return;
    try {if(loading)throw new Error('Account ачаалагдаж байна. Түр хүлээгээд дахин сонгоно уу.');if(file.size>2_000_000)throw new Error('Файл хэт том байна.');const imported=parseCurrentBackup(JSON.parse(await file.text()),catalogIds);if(turn!==epoch)throw new Error('Account солигдлоо. Файлаа дахин сонгоно уу.');if(!confirm('Файлд байгаа бодлогуудын progress-ийг сэргээх үү? Одоогийн ижил бодлогын төлөв солигдоно.'))return;for(const [id,e] of Object.entries(imported)){state[id]=e;dirty[id]=e;delete activityPending[id];}const saved=persist();render();if(saved)notice('Progress сэргээгдлээ.');void sync();}
    catch(error){notice(error.message);}finally{event.target.value='';}
  };
  $('auth-form').onsubmit=event=>{event.preventDefault();void authAction(false);};$('signup').onclick=()=>void authAction(true);
  $('signout').onclick=async()=>{if(syncing){$('auth-feedback').textContent='Хадгалалт дуусахыг хүлээгээрэй.';return;}const {error}=await client.auth.signOut();if(error){$('auth-feedback').textContent=error.message;return;}await switchUser(null);$('auth-feedback').textContent='Account-аас гарлаа.';};
  $('retry-sync').onclick=()=>void sync();window.addEventListener('online',()=>void sync());
  if(configured) {
    try {
      const {createClient}=await import('https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm');client=createClient(cfg.supabaseUrl,cfg.supabaseKey);
      client.auth.onAuthStateChange((event,session)=>{social.authEvent(event,session);setTimeout(()=>void switchUser(session?.user || null),0);});
      await refreshCatalog();startStudy();
      const {data:sessionData,error}=await client.auth.getSession();if(error)throw error;await switchUser(sessionData.session?.user || null);updateAccount();social.connected();adminUI.connected();tutorialUI.connected();groupUI.connected();
    } catch(error){client=null;catalogLoading=false;render();updateAccount();notice('Account холболт ажилласангүй: '+error.message);}
  }
  startStudy();syncProblemRoute();
}
init().catch(error=>{$('problems').textContent=error.message;$('detail-title').textContent='Бодлого ачаалсангүй';$('problem-route-state').textContent='Холболтоо шалгаад хуудсаа дахин ачаална уу.';$('problem-retry').hidden=false;notice('Хуудсаа дахин ачаалаарай.');});
