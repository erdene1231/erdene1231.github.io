import {uploadTutorialImage,tutorialImageUrl} from './tutorial-media.js?v=30';
import {mountPublication} from './tutorial-publication.js?v=30';
import {mountBlockEditor} from './tutorial-block-editor.js?v=30';
import {mountDraftRecovery} from './tutorial-draft-recovery.js?v=30';
import {createDraftSession} from './tutorial-drafts.js?v=30';
import {editableVersion,isLegacyEditableBlock} from './tutorial-editor-compat.js?v=30';
import {validateRelations} from './learning-model.js?v=23';
import {validateTutorial,view,levelNames,levels} from './tutorial-model.js?v=30';
import {node,drawArticle,typeset} from './tutorials.js?v=30';
const $=id=>document.getElementById(id);
export function setupTutorialEditor(ctx){
 let allowed=false,token=0,draft=null,revision=0,lang='mn',busy=false,accountId,blockEditor;
 $('tutorial-admin-form').hidden=true;
 const relationsBox=node('details',undefined,'tutorial-edit-section'),relationsLabel=node('label','Сургалтын холбоос ба practice — JSON'),relationsInput=node('textarea');
 relationsInput.id='tutorial-admin-relations';relationsInput.rows=16;relationsInput.maxLength=30000;relationsInput.spellcheck=false;
 relationsLabel.append(relationsInput);relationsBox.append(node('summary','Variants, дараагийн хичээл, priority practice засах'),node('p','tutorialId нь нийтлэгдсэн хичээлийн ID; key нь source|ref (жишээ cses|1620, codeforces|1201/c). Priority бүрд сурагчдад харагдахгүй reason бичнэ. Stage: Warm-up, Standard, Observation, Application, Challenge, Olympiad extension.'),relationsLabel);$('tutorial-admin-sections').before(relationsBox);
 const message=s=>$('tutorial-admin-message').textContent=s;
 const session=createDraftSession({client:ctx.client,user:ctx.user,message});
 const form=$('tutorial-admin-form');form.noValidate=true;
 $('tutorial-admin-save').textContent='Ноорог хадгалах';
 const backup=node('button','JSON backup татах');backup.type='button';
 let recovery=null;
 function downloadBody(body){if(!body){message('Backup олдсонгүй.');return;}const url=URL.createObjectURL(new Blob([JSON.stringify(body,null,2)],{type:'application/json'}));const a=node('a');a.href=url;a.download=body.id+'-draft.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 backup.onclick=()=>downloadBody(recovery?.body||session.snapshot()?.body);
 const previousBackup=node('button','Харьцуулахаас өмнөх backup татах');previousBackup.type='button';previousBackup.onclick=()=>downloadBody(session.local(ctx.user()?.id,($('tutorial-admin-choose').value)+':before-rebase')?.body);
 form.prepend(node('p','Ноорог зөвхөн танд харагдана. Нийтлэгдсэн хичээлийг өөрчлөхгүй.'),backup,previousBackup);
 const comparisonRoot=node('section');comparisonRoot.id='tutorial-draft-comparison';form.after(comparisonRoot);
 const comparison=mountDraftRecovery(comparisonRoot,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,
  capture(){if(draft)session.changed(collect(false));},candidate:()=>recovery||session.snapshot(),
  accept(result,actor,id){draft=structuredClone(result.body);recovery=null;revision=result.base_revision;
   session.open({actor,id,body:draft,baseRevision:result.base_revision,draftRevision:result.revision});session.checkpoint();
   lang='mn';$('tutorial-admin-language').value=lang;$('tutorial-admin-choose').value=id;$('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;paint();}
 });
 const compare=node('button','Хувилбаруудыг харьцуулах');compare.type='button';compare.id='tutorial-compare-drafts';compare.onclick=()=>void comparison.open();backup.after(compare);
 const publicationRoot=node('section');publicationRoot.id='tutorial-publication';form.after(publicationRoot);
 const publication=mountPublication(publicationRoot,{client:ctx.client,user:ctx.user,allowed:()=>allowed,session,lock:setBusy,message,topics:ctx.topics,problems:()=>ctx.learning()?.problemsForRelations()||[],
  capture(){session.changed(collect(false));},published:ctx.saved,
  accept(result,actor,id){draft=structuredClone(result.draft?.body||result.body);recovery=null;revision=result.revision;
   session.open({actor,id,body:draft,baseRevision:result.revision,draftRevision:result.draft?.revision||0});session.checkpoint();paint();}
 });
 const publish=node('button','Нийтлэхээр шалгах');publish.type='button';publish.id='tutorial-publish-review';publish.onclick=()=>void publication.open();compare.after(publish);
 function changed(){if(!draft||busy||!allowed)return;try{session.changed(collect(false));recovery=null;}catch(e){message(e.message);}}
 form.addEventListener('input',event=>{if(!event.target.closest('#tutorial-admin-sections'))changed();});
 window.addEventListener('online',()=>void session.flush());
 window.addEventListener('beforeunload',e=>{if(session.dirty()){e.preventDefault();e.returnValue='';}});

 async function edit(id){
  if(session.dirty()){await session.flush();if(session.dirty()){message('Хадгалаагүй ноорог байна. JSON backup татаад хадгалалтыг дахин оролдоно уу.');$('tutorial-admin-choose').value=draft?.id||'';return;}}
  const row=ctx.topics().find(t=>t.id===id)||ctx.topics()[0];if(!row)return;
  publication.invalidate();comparison.invalidate();const turn=++token,uid=ctx.user()?.id;setBusy(true);
  try{const {data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:row.id});if(error)throw error;if(turn!==token||uid!==ctx.user()?.id)return;
   const server=data.draft,base=server?.base_revision??data.current?.revision??row.revision??0,rev=server?.revision||0;
   const local=session.local(uid,row.id);recovery=local?.unsynced?local:null;
   if(recovery&&(local.baseRevision!==base||local.draftRevision!==rev)){draft=null;session.invalidate();message('Local ба онлайн ноорог зөрсөн. JSON backup татаж хадгалаарай. Автоматаар дарж хадгалахгүй.');return;}
   draft=structuredClone(recovery?.body||server?.body||data.current?.body||row);delete draft.searchText;delete draft.revision;revision=base;
   session.open({actor:uid,id:row.id,body:draft,baseRevision:base,draftRevision:rev,unsynced:!!recovery});
   lang='mn';$('tutorial-admin-language').value=lang;$('tutorial-admin-choose').value=row.id;$('tutorial-admin-level').value=draft.levelKey;$('tutorial-admin-order').value=draft.order;$('tutorial-admin-category').value=draft.category;paint();message(recovery?'Local ноорог сэргээгдлээ.':server?'Онлайн ноорог ачааллаа.':'Нийтлэгдсэн хувилбараас ноорог үүсгэнэ.');
  }catch(e){if(turn===token){draft=null;message(e.message);}}finally{if(turn===token)setBusy(false);}
 }
 function paint(){if(!draft)return;const v=editableVersion(draft,lang);$('tutorial-admin-title').value=v.title;$('tutorial-admin-summary').value=v.summary;$('tutorial-admin-prerequisites').value=v.prerequisites;$('tutorial-admin-prerequisite-ids').value=(draft.prerequisiteIds||[]).join(', ');const rel=draft.learningRelations||ctx.learning()?.relationsFor(draft.id);relationsInput.disabled=!ctx.learning();relationsInput.value=draft._draftRelationsText??JSON.stringify(rel?{variants:rel.variants,next:rel.next,practice:rel.practice}:{variants:[],next:null,practice:[]},null,2);$('tutorial-admin-sections').replaceChildren();
  blockEditor?.destroy();blockEditor=mountBlockEditor($('tutorial-admin-sections'),v.sections,{changed,message,locked:()=>busy||!allowed,
   uploadImage:(file,blockCurrent)=>{const actor=ctx.user()?.id,turn=token,id=draft.id;return uploadTutorialImage(ctx.client(),id,file,actor,()=>turn===token&&actor===ctx.user()?.id&&draft?.id===id&&allowed&&!busy&&blockCurrent());},
   imageUrl:path=>tutorialImageUrl(ctx.client(),path,ctx.user()?.id,true),topics:ctx.topics,problems:()=>ctx.learning()?.problemsForRelations()||[]});
 }
 function collect(validate=true){if(!draft)return;editableVersion(draft,lang);draft.levelKey=$('tutorial-admin-level').value;draft.level=levelNames.mn[levels.indexOf(draft.levelKey)];draft.order=Number($('tutorial-admin-order').value);draft.category=$('tutorial-admin-category').value.trim();draft.prerequisiteIds=$('tutorial-admin-prerequisite-ids').value.split(',').map(x=>x.trim()).filter(Boolean);const v=editableVersion(draft,lang);v.title=$('tutorial-admin-title').value.trim();v.summary=$('tutorial-admin-summary').value.trim();v.prerequisites=$('tutorial-admin-prerequisites').value.trim();
  if(!validate){draft._draftRelationsText=relationsInput.value;return draft;}
  const published=ctx.topics(),ids=new Set(published.map(t=>t.id));for(const id of draft.prerequisiteIds)if(!ids.has(id)||id===draft.id)throw new Error('Урьдчилсан хичээлийн ID байхгүй эсвэл өөрийгөө заасан: '+id);
  const graph=new Map(published.map(t=>[t.id,t.id===draft.id?draft.prerequisiteIds:t.prerequisiteIds||[]])),visiting=new Set(),done=new Set();
  function walk(id){if(visiting.has(id))throw new Error('Prerequisite cycle үүсэж байна.');if(done.has(id))return;visiting.add(id);for(const next of graph.get(id)||[])walk(next);visiting.delete(id);done.add(id);}walk(draft.id);
  if(ctx.learning()){let rel;try{rel=JSON.parse(relationsInput.value);}catch{throw new Error('Сургалтын холбоосын JSON буруу байна.');}draft.learningRelations=validateRelations(rel,draft.id,published,ctx.learning().problemsForRelations());}
  return validateTutorial(draft);
 }
 function setBusy(value){busy=value;for(const el of $('tutorial-admin-form').querySelectorAll('input,textarea,select,button,[contenteditable]')){if(el.hasAttribute('contenteditable'))el.contentEditable=String(!value);else el.disabled=value;}$('tutorial-admin-choose').disabled=value;$('tutorial-admin-reload').disabled=value;}
 async function refresh(){const old=$('tutorial-admin-choose').value;$('tutorial-admin-choose').replaceChildren();for(const t of ctx.topics()){const o=node('option',t.title+' · '+levelNames.mn[levels.indexOf(t.levelKey)]);o.value=t.id;$('tutorial-admin-choose').append(o);}if(allowed)await edit(old);$('tutorial-admin-save').disabled=!allowed||!ctx.ready();if(allowed&&!ctx.ready())message('Онлайн засварлахын тулд Supabase дээр 008-tutorials.sql шинэчлэлтийг ажиллуулна уу.');}
 async function accountChanged(force=false){const id=ctx.user()?.id||null;if(!force&&id===accountId)return;blockEditor?.destroy();publication.invalidate();comparison.invalidate();session.invalidate();recovery=null;accountId=id;const turn=++token;allowed=false;draft=null;$('tutorial-admin-form').hidden=true;$('tutorial-admin-save').disabled=true;if($('tutorial-preview').open)$('tutorial-preview').close();if(!ctx.client()||!ctx.user())return;
  try{const {data,error}=await ctx.client().rpc('is_admin');if(error)throw error;if(turn!==token)return;allowed=data===true;$('tutorial-admin-form').hidden=!allowed;if(allowed){setBusy(false);await refresh();}}catch{if(turn===token)message('Админ эрхийг шалгаж чадсангүй. Дахин нэвтэрч оролдоорой.');}
 }
 $('tutorial-admin-language').onchange=()=>{try{changed();collect(false);const nextLang=$('tutorial-admin-language').value;editableVersion(draft,nextLang);lang=nextLang;paint();message('');}catch(e){$('tutorial-admin-language').value=lang;message(e.message);}};
 $('tutorial-admin-choose').onchange=()=>{edit($('tutorial-admin-choose').value);message(ctx.ready()?'':'008-tutorials.sql шинэчлэлт шаардлагатай.');};
 $('tutorial-admin-reload').onclick=()=>void edit($('tutorial-admin-choose').value);
 $('tutorial-admin-preview').onclick=()=>{try{collect();const snapshot=structuredClone(draft),selectedLang=lang;$('tutorial-preview').showModal();void typeset([$ ('tutorial-preview-content')],()=>{const target=$('tutorial-preview-content'),v=view(snapshot,selectedLang);drawArticle(snapshot,target,selectedLang,{client:ctx.client(),viewerId:ctx.user()?.id||'public',adminPreview:true,learning:ctx.learning()});target.prepend(node('h2',v.title),node('p',v.summary));}).catch(e=>message(e.message));}catch(e){message(e.message);}};
 $('tutorial-admin-form').onsubmit=async event=>{event.preventDefault();if(!allowed||busy||!draft)return;changed();await session.flush();};
 refresh();return {refresh,accountChanged};
}
