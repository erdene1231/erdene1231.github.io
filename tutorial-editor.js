import {priorityLevel} from './priority.js?v=42';
import {mountTutorialReset} from './tutorial-reset.js?v=42';
import {sameEditorBody} from './tutorial-workflow.js?v=42';
import {mountBackupImport} from './tutorial-backup.js?v=42';
import {normalizeProblemReferences} from './learning-model.js?v=42';
import {openProblemSelection} from './problem-selection-dialog.js?v=42';
import {tutorialSlug} from './tutorial-slug.js?v=42';
import {mountTutorialLifecycle} from './tutorial-lifecycle.js?v=42';
import {createBlock} from './tutorial-blocks.js?v=42';
import {uploadTutorialImage,tutorialImageUrl} from './tutorial-media.js?v=42';
import {mountPublication} from './tutorial-publication.js?v=42';
import {mountBlockEditor} from './tutorial-block-editor.js?v=42';
import {mountDraftRecovery} from './tutorial-draft-recovery.js?v=42';
import {createDraftSession} from './tutorial-drafts.js?v=42';
import {editableVersion} from './tutorial-editor-compat.js?v=42';
import {validateRelations} from './learning-model.js?v=42';
import {validateTutorial,view,levelNames,levels} from './tutorial-model.js?v=42';
import {node,drawArticle,typeset} from './tutorials.js?v=42';
const $=id=>document.getElementById(id);
export function setupTutorialEditor(ctx){
 let allowed=false,token=0,draft=null,revision=0,lang='mn',busy=false,accountId,blockEditor,workspace=[],catalogCurrent=null;
 const removedIds=new Set();
 const isPublished=()=>catalogCurrent?.published===true;
 const differsFromPublished=()=>isPublished()&&!sameEditorBody(draft,catalogCurrent.body,availableProblems());
 const availableProblems=()=>ctx.problems?.()||ctx.learning()?.problemsForRelations()||[];
 const currentProgress=()=>ctx.progress?.()||ctx.learning()?.progressForPicker?.()||{};

 $('tutorial-admin-form').hidden=true;
 const relationsBox=node('details',undefined,'tutorial-edit-section'),relationsLabel=node('label','Сургалтын холбоос ба practice — JSON'),relationsInput=node('textarea');
 relationsInput.id='tutorial-admin-relations';relationsInput.rows=16;relationsInput.maxLength=30000;relationsInput.spellcheck=false;
 relationsLabel.append(relationsInput);relationsBox.append(node('summary','Variants, дараагийн хичээл, priority practice засах'),node('p','tutorialId нь нийтлэгдсэн хичээлийн ID; key нь бодлогын дугаар (жишээ 1). Reason тайлбар сонголттой. Stage: Warm-up, Standard, Observation, Application, Challenge, Olympiad extension.'),relationsLabel);$('tutorial-admin-sections').before(relationsBox);
 const selectPractice=node('button','Practice бодлого сонгох…');selectPractice.type='button';relationsBox.before(selectPractice);
 selectPractice.onclick=()=>{if(!draft||busy||!allowed)return;const actor=ctx.user()?.id,turn=token;let rel;try{rel=normalizeProblemReferences({learningRelations:JSON.parse(relationsInput.value)},availableProblems()).learningRelations;}catch{message('Сургалтын холбоосын JSON-ийг эхлээд засна уу.');return;}
 openProblemSelection({problems:availableProblems,progress:currentProgress,valid:()=>allowed&&!busy&&turn===token&&actor===ctx.user()?.id,maxSelected:30,selected:(rel.practice||[]).map(p=>p.key),onSelect:(rows,keys)=>{const old=new Map((rel.practice||[]).map(p=>[p.key,p]));rel.practice=keys.map(key=>old.get(key)||{key,stage:'Warm-up',priority:false});relationsInput.value=JSON.stringify(rel,null,2);changed();}});};
 const message=s=>{$('tutorial-admin-message').textContent=s;if($('tutorial-save-feedback'))$('tutorial-save-feedback').textContent=s;queueMicrotask(updateSave);};
 const session=createDraftSession({client:ctx.client,user:ctx.user,message,stateChanged:()=>queueMicrotask(updateSave),autoSave:()=>!isPublished(),persistUnsaved:()=>!isPublished()});
 const form=$('tutorial-admin-form');form.noValidate=true;
 const priorityLabel=node('label','Priority'),prioritySelect=node('select'),priorityReasonLabel=node('label','Priority үндэслэл'),priorityReason=node('textarea');prioritySelect.id='tutorial-admin-priority';for(const value of ['low','medium','high']){const o=node('option',value[0].toUpperCase()+value.slice(1)+' priority');o.value=value;prioritySelect.append(o);}priorityReason.id='tutorial-admin-priority-reason';priorityReason.maxLength=1000;priorityReason.rows=2;priorityLabel.append(prioritySelect);priorityReasonLabel.append(priorityReason);form.querySelector('.admin-fields').append(priorityLabel,priorityReasonLabel);prioritySelect.onchange=()=>{if(draft&&!busy&&allowed){draft.priorityLevel=prioritySelect.value;changed();}};
 $('tutorial-admin-save').textContent='Ноорог хадгалах';
 const backup=node('button','JSON export');backup.id='tutorial-backup-export';backup.type='button';
 let recovery=null;
 function downloadBody(body){if(!body){message('Backup олдсонгүй.');return;}const url=URL.createObjectURL(new Blob([JSON.stringify(body,null,2)],{type:'application/json'}));const a=node('a');a.href=url;a.download=body.id+'-draft.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 backup.onclick=()=>downloadBody(recovery?.body||session.snapshot()?.body);
 form.prepend(node('p','Ноорог зөвхөн танд харагдана. Нийтлэгдсэн хичээлийг өөрчлөхгүй.'),backup);
 const recoveryNotice=node('section');recoveryNotice.className='recovery-notice';recoveryNotice.hidden=true;
 const resumeRecovery=node('button','Хувилбараа сонгоод засвараа үргэлжлүүлэх');resumeRecovery.type='button';resumeRecovery.dataset.recoveryResume='true';
 const recoveryBackup=node('button','Төхөөрөмжийн засварыг JSON backup татах');recoveryBackup.type='button';recoveryBackup.dataset.recoveryBackup='true';recoveryBackup.onclick=()=>downloadBody(recovery?.body);
 recoveryNotice.append(node('p','Төхөөрөмжийн засвар хадгалагдсан. Үргэлжлүүлэх хувилбараа сонгох эсвэл өөр хичээл нээж болно.'),resumeRecovery,recoveryBackup);form.before(recoveryNotice);
 const comparisonRoot=node('section');comparisonRoot.id='tutorial-draft-comparison';form.before(comparisonRoot);
 const comparison=mountDraftRecovery(comparisonRoot,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,backup:downloadBody,
  capture(){if(draft)session.changed(collect(false));},candidate:()=>recovery||session.snapshot(),
  accept(result,actor,id){draft=structuredClone(result.body);recovery=null;revision=result.base_revision;
   session.open({actor,id,body:draft,baseRevision:result.base_revision,draftRevision:result.revision});session.checkpoint();
   lang='mn';$('tutorial-admin-language').value=lang;$('tutorial-admin-choose').value=id;$('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;paint();}
 });
 resumeRecovery.onclick=()=>void comparison.open();
 const publicationRoot=node('section');publicationRoot.id='tutorial-publication';form.after(publicationRoot);
 const publication=mountPublication(publicationRoot,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,topics:ctx.topics,problems:availableProblems,
  capture(){session.changed(collect(false));},published:row=>{rememberCatalog(row);ctx.saved?.(row);},
  accept(result,actor,id){draft=structuredClone(result.draft?.body||result.body);recovery=null;revision=result.revision;catalogCurrent={...result,published:true};
   session.open({actor,id,body:draft,baseRevision:result.revision,draftRevision:result.draft?.revision||0});session.checkpoint();paint();}
 });
 const publish=node('button','Нийтлэх');publish.type='button';publish.id='tutorial-publish-review';publish.onclick=()=>void publication.open({immediate:isPublished()});backup.after(publish);
 const lifecycleRoot=node('section');lifecycleRoot.id='tutorial-lifecycle';lifecycleRoot.className='tutorial-lifecycle';form.before(lifecycleRoot);
 const lifecycle=mountTutorialLifecycle(lifecycleRoot,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,
  capture(){session.changed(collect(false));},updated:ctx.saved,
  accept(result,actor,id){
   // A visibility change preserves the private body returned by the server.
   // Never interpret a null draft as permission to overwrite a stale local edit.
   if(!result.draft)throw Error('Нооргийн шинэ төлөвийг дахин ачаална уу.');
   draft=structuredClone(result.draft.body);recovery=null;revision=result.draft.base_revision;rememberCatalog(result);
   session.open({actor,id,body:draft,baseRevision:revision,draftRevision:result.draft.revision});session.checkpoint();paint();
  },
  removed(result,actor,id){if(result?.id!==id||result?.deleted!==true)throw Error('Устгалтын хариуг баталгаажуулж чадсангүй. Дахин ачаална уу.');
   session.invalidate({saveLocal:false});
   try{const key='erdene:tutorial-draft:v3:'+actor+':'+id;localStorage.removeItem(key);localStorage.removeItem(key+':before-rebase');}catch{}
   recovery=null;catalogCurrent=null;removedIds.add(id);workspace=workspace.filter(row=>row.id!==id);clearDocument();$('tutorial-admin-choose').value='';ctx.deleted?.(id);queueMicrotask(()=>void refresh());
  }
 });
 const lifecycleActions=node('div');lifecycleActions.className='tutorial-lifecycle-actions';
 const visibility=node('button','Түр устгах'),permanentDelete=node('button','Ноорог устгах');visibility.type=permanentDelete.type='button';
 visibility.id='tutorial-visibility-review';visibility.onclick=()=>void lifecycle.open(catalogCurrent?.published===false?'restore':'hide');
 permanentDelete.id='tutorial-delete-review';permanentDelete.className='tutorial-danger';permanentDelete.onclick=()=>void lifecycle.open('delete');
 const lifecycleState=node('p');lifecycleState.id='tutorial-lifecycle-state';lifecycleActions.append(lifecycleState,visibility,permanentDelete);publish.after(lifecycleActions);
 const toolbar=node('div');toolbar.className='tutorial-editor-toolbar';toolbar.append(backup);form.prepend(toolbar);
 const importInput=node('input');importInput.type='file';importInput.accept='.json,application/json';importInput.hidden=true;importInput.id='tutorial-backup-file';const importButton=node('button','JSON import');importButton.type='button';importButton.id='tutorial-backup-import';importButton.onclick=()=>importInput.click();toolbar.append(importButton,importInput);
 const importRoot=node('section');importRoot.id='tutorial-import-review';form.before(importRoot);
 const importer=mountBackupImport(importRoot,importInput,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,
  accept(body,current){draft=normalizeProblemReferences(body,availableProblems());recovery=null;revision=current.baseRevision;lang='mn';session.open({...current,body:draft,unsynced:true});session.checkpoint();$('tutorial-admin-language').value=lang;$('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;paint();}
 });
 const advanced=node('details');advanced.className='tutorial-editor-settings';advanced.append(node('summary','ID, хайлтын түлхүүр үг ба холбоотой хичээлүүд'));for(const id of ['tutorial-admin-id','tutorial-admin-aliases','tutorial-admin-related'])advanced.append($(id).closest('label'));toolbar.after(advanced);
 $('tutorial-admin-sections').before(node('h3','Хичээлийн агуулга'));$('tutorial-admin-sections').after(lifecycleActions);
 const resetRoot=node('section');resetRoot.id='tutorial-reset-review';form.before(resetRoot);
 const resetter=mountTutorialReset(resetRoot,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,
  accept(result,actor,id){draft=normalizeProblemReferences(result.body,availableProblems());recovery=null;revision=result.revision;catalogCurrent=result;session.open({actor,id,body:draft,baseRevision:revision,draftRevision:0});session.checkpoint();try{localStorage.removeItem('erdene:tutorial-draft:v3:'+actor+':'+id+':before-rebase');}catch{}lang='mn';$('tutorial-admin-language').value=lang;$('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;paint();rememberCatalog(result);ctx.saved?.(result);}
 });
 const reset=node('button','Reset');reset.type='button';reset.id='tutorial-reset';reset.onclick=()=>void resetter.open();
 const savebar=$('tutorial-admin-preview').parentElement;savebar.classList.add('tutorial-editor-savebar');savebar.append(publish,reset,visibility,permanentDelete);const saveFeedback=node('span');saveFeedback.id='tutorial-save-feedback';saveFeedback.setAttribute('role','status');saveFeedback.setAttribute('aria-live','polite');savebar.append(saveFeedback);
 function rememberCatalog(row){catalogCurrent=row;workspace=workspace.filter(t=>t.id!==row.body.id);workspace.push({id:row.body.id,title:row.body.title,revision:row.revision,published:row.published});void refresh();}
 function changed(){if(!draft||busy||!allowed)return;try{const body=collect(false);if(!sameEditorBody(body,session.snapshot()?.body,availableProblems()))session.changed(body);recovery=null;updateSave();}catch(e){message(e.message);}}
 form.addEventListener('input',event=>{if(event.target!==importInput&&!event.target.closest('#tutorial-admin-sections'))changed();});
 window.addEventListener('online',()=>{if(!isPublished())void session.flush();});
 window.addEventListener('beforeunload',e=>{if(session.dirty()){e.preventDefault();e.returnValue='';}});

 async function edit(id){
  const actor=ctx.user()?.id;if(!allowed||!actor)return;
  if(session.dirty()&&isPublished()){if(!window.confirm('Хадгалаагүй засварыг орхих уу? Үргэлжлүүлэхийн өмнө Түр хадгалах боломжтой.')){$('tutorial-admin-choose').value=draft?.id||'';return;}session.invalidate({saveLocal:false});}
  if(session.dirty()){await session.flush();if(session.dirty()){message('Хадгалаагүй ноорог байна. JSON backup татаад хадгалалтыг дахин оролдоно уу.');$('tutorial-admin-choose').value=draft?.id||'';return;}}
  if(!allowed||ctx.user()?.id!==actor)return;
  const row=choices().find(t=>t.id===id)||(!id?choices()[0]:null);if(!row){message('Хичээл сонгоно уу.');return;}
  publication.invalidate();comparison.invalidate();lifecycle.invalidate();importer.invalidate();resetter.invalidate();const turn=++token,uid=ctx.user()?.id;clearDocument();setBusy(true);
  try{const {data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:row.id});if(error)throw error;if(turn!==token||uid!==ctx.user()?.id)return;
   if(data.deleted)throw Error('Энэ хичээл үүрд устгагдсан. Өөр хичээл сонгоно уу.');catalogCurrent=data.current;const server=data.draft,base=server?.base_revision??data.current?.revision??row.revision??0,rev=server?.revision||0;
   const local=session.local(uid,row.id);recovery=local?.unsynced?local:null;
   if((isPublished()&&recovery)||(recovery&&(local.baseRevision!==base||local.draftRevision!==rev))||(server&&data.current&&base!==data.current.revision)){recovery??=local||{actor:uid,id:row.id,body:server.body,baseRevision:base,draftRevision:rev};session.invalidate({saveLocal:false});message('Local ба онлайн ноорог зөрсөн. Хувилбаруудаа харьцуулж засвараа сэргээнэ үү.');queueMicrotask(()=>{if(turn===token&&recovery)void comparison.open();});return;}
   if(!server?.body&&!data.current?.body)throw Error('Хичээлийн онлайн агуулга олдсонгүй. Дахин ачаалж оролдоно уу.');
   draft=structuredClone(recovery?.body||server?.body||data.current?.body);delete draft.searchText;delete draft.revision;revision=base;
   session.open({actor:uid,id:row.id,body:draft,baseRevision:base,draftRevision:rev,unsynced:!!recovery});
   lang='mn';$('tutorial-admin-language').value=lang;$('tutorial-admin-choose').value=row.id;$('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;paint();message(recovery?'Local ноорог сэргээгдлээ.':server?'Онлайн ноорог ачааллаа.':'Нийтлэгдсэн хувилбараас ноорог үүсгэнэ.');
  }catch(e){if(turn===token){clearDocument();message(e.message);}}finally{if(turn===token)setBusy(false);}
 }
 function paint(){if(!draft)return;prioritySelect.value=priorityLevel(draft);priorityReason.value=draft.priorityReason||'';draft=normalizeProblemReferences(draft,availableProblems());$('tutorial-admin-id').value=draft.id;$('tutorial-admin-aliases').value=draft.aliases||'';$('tutorial-admin-related').value=(draft.related||[]).join(', ');const v=editableVersion(draft,lang);$('tutorial-admin-title').value=v.title;$('tutorial-admin-summary').value=v.summary;$('tutorial-admin-prerequisites').value=v.prerequisites;$('tutorial-admin-prerequisite-ids').value=(draft.prerequisiteIds||[]).join(', ');const rel=draft.learningRelations;relationsInput.disabled=busy||!allowed;relationsInput.value=draft._draftRelationsText??JSON.stringify(rel?{variants:rel.variants,next:rel.next,practice:rel.practice}:{variants:[],next:null,practice:[]},null,2);$('tutorial-admin-sections').replaceChildren();
  blockEditor?.destroy();blockEditor=mountBlockEditor($('tutorial-admin-sections'),v.sections,{changed,message,locked:()=>busy||!allowed,
   uploadImage:(file,blockCurrent)=>{const actor=ctx.user()?.id,turn=token,id=draft.id;return uploadTutorialImage(ctx.client(),id,file,actor,()=>turn===token&&actor===ctx.user()?.id&&draft?.id===id&&allowed&&!busy&&blockCurrent());},
   imageUrl:path=>tutorialImageUrl(ctx.client(),path,ctx.user()?.id,true),topics:ctx.topics,problems:availableProblems,progress:currentProgress});
 }
 function collect(validate=true){if(!draft)return;if(draft.priorityLevel!==undefined||prioritySelect.value!==priorityLevel(draft))draft.priorityLevel=prioritySelect.value;if(draft.priorityReason!==undefined||priorityReason.value.trim())draft.priorityReason=priorityReason.value.trim();draft.aliases=$('tutorial-admin-aliases').value.trim();draft.related=$('tutorial-admin-related').value.split(',').map(x=>x.trim()).filter(Boolean);editableVersion(draft,lang);draft.levelKey=$('tutorial-admin-level').value;draft.level=levelNames.mn[levels.indexOf(draft.levelKey)];draft.order=Number($('tutorial-admin-order').value||1);draft.category=$('tutorial-admin-category').value.trim();draft.prerequisiteIds=$('tutorial-admin-prerequisite-ids').value.split(',').map(x=>x.trim()).filter(Boolean);const v=editableVersion(draft,lang);v.title=$('tutorial-admin-title').value.trim();v.summary=$('tutorial-admin-summary').value.trim();v.prerequisites=$('tutorial-admin-prerequisites').value.trim();
  if(!validate){draft._draftRelationsText=relationsInput.value;return draft;}
  const published=ctx.topics(),ids=new Set(published.map(t=>t.id));for(const id of draft.prerequisiteIds)if(!ids.has(id)||id===draft.id)throw new Error('Урьдчилсан хичээлийн ID байхгүй эсвэл өөрийгөө заасан: '+id);
  const graph=new Map(published.map(t=>[t.id,t.id===draft.id?draft.prerequisiteIds:t.prerequisiteIds||[]])),visiting=new Set(),done=new Set();
  function walk(id){if(visiting.has(id))throw new Error('Prerequisite cycle үүсэж байна.');if(done.has(id))return;visiting.add(id);for(const next of graph.get(id)||[])walk(next);visiting.delete(id);done.add(id);}walk(draft.id);
  if(ctx.learning()&&relationsInput.value.trim()){let rel;try{rel=JSON.parse(relationsInput.value);}catch{throw new Error('Сургалтын холбоосын JSON буруу байна.');}if(draft.learningRelations||rel.practice?.length||rel.variants?.length||rel.next)draft.learningRelations=validateRelations(rel,draft.id,published,ctx.learning().problemsForRelations());}
  return validateTutorial(draft);
 }
 function clearDocument(){blockEditor?.destroy();blockEditor=null;draft=null;catalogCurrent=null;
  for(const id of ['id','title','summary','prerequisites','prerequisite-ids','aliases','related','category','order'])$('tutorial-admin-'+id).value='';
 }
 function setBusy(value){busy=value;form.hidden=!allowed||!draft;recoveryNotice.hidden=!allowed||!recovery||!comparisonRoot.hidden||busy;const editable=allowed&&!!draft&&!busy;
  for(const el of form.querySelectorAll('input,textarea,select,button,[contenteditable]')){
   if(el.hasAttribute('contenteditable'))el.contentEditable=String(editable);
   else el.disabled=!editable;
  }
  relationsInput.disabled=!editable;
  backup.disabled=busy||!allowed||!(recovery||session.snapshot());
  publish.disabled=!editable;
  const existing=!!draft&&catalogCurrent?.body?.id===draft.id;
  visibility.hidden=!existing||catalogCurrent?.published!==true;visibility.disabled=!editable;visibility.textContent='Түр устгах';
  permanentDelete.hidden=!draft||catalogCurrent?.published===true;permanentDelete.disabled=!editable;
  lifecycleState.textContent=!existing?'Шинэ хувийн ноорог — хараахан нийтлэгдээгүй.':catalogCurrent.published===false?'Ноорог төлөв. Нийтлэх эсвэл нооргийг бүрмөсөн устгах боломжтой.':'Нийтлэгдсэн хичээл. Үүрд устгахын өмнө түр устгана.';
  updateSave();
  blockEditor?.refreshControls();
  $('tutorial-admin-choose').disabled=busy||!allowed;$('tutorial-admin-reload').disabled=busy||!allowed;$('tutorial-admin-new').disabled=busy||!allowed;for(const el of $('tutorial-new-form').querySelectorAll('input,button'))el.disabled=busy||!allowed;
 }
 function updateSave(){const snapshot=session.snapshot(),saving=session.saving?.(),saved=!!snapshot?.draftRevision&&!session.dirty(),published=isPublished(),button=$('tutorial-admin-save');
  button.textContent=saving?'Хадгалж байна…':published?'Түр хадгалах':saved?'Хадгалагдсан':'Хадгалах';button.disabled=busy||!allowed||!draft||!ctx.ready()||saving||(published?!session.dirty():saved);
  for(const id of ['tutorial-admin-choose','tutorial-admin-reload','tutorial-admin-new'])$(id).disabled=busy||!allowed||saving;reset.hidden=!published;reset.disabled=busy||!allowed||!published||saving||(!differsFromPublished()&&!(snapshot?.draftRevision&&!sameEditorBody(session.savedBody(),catalogCurrent.body,availableProblems())));
  publish.disabled=busy||!allowed||!draft||saving||(published&&!differsFromPublished());
  lifecycleState.textContent=published?(session.dirty()?'Нийтлэл · Хадгалаагүй өөрчлөлттэй':differsFromPublished()?'Нийтлэл · Түр хадгалсан засвар байна — нийтлэлд ороогүй':'Нийтлэл · Хадгалагдсан'):'Ноорог · Зөвхөн танд харагдана';
 }

 function choices(){const rows=new Map(ctx.topics().map(t=>[t.id,t]));for(const t of workspace)rows.set(t.id,{...rows.get(t.id),...t});
  if(draft)rows.set(draft.id,{...rows.get(draft.id),...draft,published:catalogCurrent?.published===true});if(recovery)rows.set(recovery.id,{...rows.get(recovery.id),...recovery.body});return [...rows.values()].filter(t=>!removedIds.has(t.id));
 }
 async function loadWorkspace(){const actor=ctx.user()?.id,turn=token;try{const {data,error}=await ctx.client().rpc('admin_tutorial_workspace');if(error)throw error;
   if(turn!==token||actor!==ctx.user()?.id||!allowed)return;
   workspace=[...(data?.catalog||[]),...(data?.drafts||[]).map(d=>({...d,id:d.tutorial_id,title:(d.title||d.tutorial_id)+' · ноорог'}))];
  }catch{/* Existing public choices remain usable when workspace metadata cannot load. */}
 }
 async function refresh(){const old=draft?.id||recovery?.id||$('tutorial-admin-choose').value;$('tutorial-admin-choose').replaceChildren();
  for(const t of choices()){const o=node('option',(t.title||t.id)+' · '+t.id+(t.published===false?' · ноорог':''));o.value=t.id;$('tutorial-admin-choose').append(o);}
  if(choices().some(t=>t.id===old))$('tutorial-admin-choose').value=old;
  if(allowed&&!draft&&!recovery)await edit(old);else setBusy(busy);
 }
 const idHint=node('p','ID нь хичээлийн нэрээс автоматаар үүснэ.');idHint.className='muted';$('tutorial-new-id').closest('label').after(idHint);$('tutorial-new-id').oninput=()=>{const id=tutorialSlug($('tutorial-new-id').value);idHint.textContent=id?'Хичээлийн ID: '+id:'Нэрэнд үсэг оруулна уу.';};
 $('tutorial-admin-new').onclick=()=>{$('tutorial-new-form').hidden=false;$('tutorial-new-id').focus();};
 $('tutorial-new-cancel').onclick=()=>{$('tutorial-new-form').hidden=true;};
 $('tutorial-new-form').onsubmit=async event=>{event.preventDefault();const actor=ctx.user()?.id,title=$('tutorial-new-id').value.trim(),id=tutorialSlug(title);
  if(!allowed||busy||!actor)return;if(!/^[a-z0-9-]{1,80}$/.test(id)){message('Хичээлийн нэр оруулна уу. Нэрэнд үсэг байх шаардлагатай.');return;}
  if(choices().some(t=>t.id===id)){message('Энэ ID-тай tutorial/ноорог байна. Жагсаалтаас нээгээрэй.');return;}
  if(session.dirty()&&isPublished()){if(!window.confirm('Хадгалаагүй засварыг орхиод шинэ хичээл нээх үү?'))return;session.invalidate({saveLocal:false});}await session.flush();if(!allowed||ctx.user()?.id!==actor)return;if(session.dirty()){message('Одоогийн нооргийг хадгалж эсвэл backup татаж хамгаална уу.');return;}
  const turn=++token;setBusy(true);
  try{const {data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:id});if(error)throw error;if(turn!==token||actor!==ctx.user()?.id)return;
   if(data?.deleted)throw Error('Энэ ID-тай хичээл үүрд устгагдсан. Шинэ ID сонгоно уу.');
   if(data?.current||data?.draft)throw Error('Энэ ID аль хэдийн ашиглагдсан байна. Өөр ID сонгоно уу.');
   publication.invalidate();comparison.invalidate();lifecycle.invalidate();importer.invalidate();resetter.invalidate();
   draft={id,title,summary:'',prerequisites:'',aliases:'',category:'',levelKey:'beginner',level:levelNames.mn[0],order:Math.min(1000,Math.max(0,...ctx.topics().map(t=>t.order))+1),related:[],prerequisiteIds:[],sections:[]};
   recovery=null;removedIds.delete(id);catalogCurrent=null;revision=0;lang='mn';$('tutorial-admin-language').value=lang;session.open({actor,id,body:draft,baseRevision:0,draftRevision:0});
   $('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;
   paint();await refresh();if(turn!==token||actor!==ctx.user()?.id)return;session.changed(collect(false));$('tutorial-new-form').hidden=true;$('tutorial-new-id').value='';message('Шинэ хувийн ноорог үүслээ. Гарчиг, тайлбар, бүлэг болон агуулгаа бөглөөрэй.');
  }catch(e){if(turn===token)message(e.message);}finally{if(turn===token){setBusy(false);$('tutorial-admin-title').focus();}}
 };
 async function accountChanged(force=false){const id=ctx.user()?.id||null;if(!force&&id===accountId)return;blockEditor?.destroy();publication.invalidate();comparison.invalidate();lifecycle.invalidate();importer.invalidate();resetter.invalidate();session.invalidate();recovery=null;recoveryNotice.hidden=true;workspace=[];$('tutorial-new-form').hidden=true;accountId=id;const turn=++token;allowed=false;clearDocument();$('tutorial-admin-choose').replaceChildren();setBusy(false);$('tutorial-admin-form').hidden=true;$('tutorial-admin-save').disabled=true;if($('tutorial-preview').open)$('tutorial-preview').close();$('tutorial-preview-content').replaceChildren();if(!ctx.client()||!ctx.user())return;
  try{const {data,error}=await ctx.client().rpc('is_admin');if(error)throw error;if(turn!==token)return;allowed=data===true;$('tutorial-admin-form').hidden=!allowed;if(allowed){setBusy(false);await loadWorkspace();if(turn!==token)return;await refresh();}}catch{if(turn===token)message('Админ эрхийг шалгаж чадсангүй. Дахин нэвтэрч оролдоорой.');}
 }
 $('tutorial-admin-language').onchange=()=>{if(!draft||busy||!allowed)return;try{collect(false);const nextLang=$('tutorial-admin-language').value;if(nextLang==='en'&&!draft.translations?.en){draft.translations??={};draft.translations.en={title:'',summary:'',prerequisites:'',sections:[]};}lang=nextLang;paint();changed();setBusy(false);message('');}catch(e){$('tutorial-admin-language').value=lang;message(e.message);}};
 $('tutorial-admin-choose').onchange=()=>{edit($('tutorial-admin-choose').value);};
 $('tutorial-admin-reload').onclick=async()=>{if(!allowed||busy)return;await loadWorkspace();await edit($('tutorial-admin-choose').value);};
 $('tutorial-admin-preview').onclick=()=>{try{if(!allowed||busy||!draft)return;collect(false);const snapshot=structuredClone(draft),selectedLang=lang,turn=token,actor=ctx.user()?.id;$('tutorial-preview-content').replaceChildren();$('tutorial-preview').showModal();void typeset([$ ('tutorial-preview-content')],()=>{if(turn!==token||!allowed||actor!==ctx.user()?.id||!$('tutorial-preview').open)return false;const target=$('tutorial-preview-content'),v=view(snapshot,selectedLang);drawArticle(snapshot,target,selectedLang,{client:ctx.client(),viewerId:ctx.user()?.id||'public',adminPreview:true,draftPreview:true,learning:ctx.learning()});target.prepend(node('p','Урьдчилан харах — нийтлэл өөрчлөгдөхгүй.'),node('h2',v.title||'Гарчиггүй хичээл'),node('p',v.summary||''));}).catch(e=>message(e.message));}catch(e){message(e.message);}};
 $('tutorial-admin-form').onsubmit=async event=>{event.preventDefault();if(!allowed||busy||!draft)return;if(!session.dirty()&&!session.snapshot()?.draftRevision)session.changed(collect(false));updateSave();await session.flush();updateSave();};
 refresh();return {refresh,accountChanged};
}
