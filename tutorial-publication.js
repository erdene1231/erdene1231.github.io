import {validateTutorial} from './tutorial-model.js?v=38';
import {validateRelations} from './learning-model.js?v=38';
export function publicationBody(draft,topics,problems){
 const body=structuredClone(draft);
 if(Object.hasOwn(body,'_draftRelationsText')){
  if(typeof body._draftRelationsText!=='string')throw Error('Сургалтын холбоосын JSON буруу.');
  let rel;try{rel=JSON.parse(body._draftRelationsText);}catch{throw Error('Сургалтын холбоосын JSON буруу.');}
  if(!rel||!Array.isArray(rel.practice)||!Array.isArray(rel.variants))throw Error('Сургалтын холбоосын бүтэц буруу.');
  if(body.learningRelations||rel.practice.length||rel.variants.length||rel.next)body.learningRelations=rel;
  delete body._draftRelationsText;
 }
 if(body.learningRelations){validateRelations(body.learningRelations,body.id,topics,problems);if(!body.learningRelations.practice.length||!body.learningRelations.practice.some(p=>p.priority))throw Error('Дор хаяж нэг Priority бодлого сонгоно уу.');}
 validateTutorial(body);return body;
}
const el=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
export function mountPublication(root,ctx){
 let generation=0,active=false;
 const valid=(turn,actor)=>turn===generation&&ctx.allowed()&&ctx.user()?.id===actor;
 function close(){generation++;active=false;root.replaceChildren();root.hidden=true;ctx.session.resume();ctx.lock(false);}
 async function open(){
  if(active||!ctx.allowed()||!ctx.session.snapshot())return;active=true;const turn=++generation,actor=ctx.user()?.id;ctx.lock(true);root.hidden=false;root.replaceChildren(el('p','Нийтлэх агуулгыг шалгаж байна…'));root.scrollIntoView({block:'nearest'});
  try{
   ctx.capture();const body=publicationBody(ctx.session.snapshot().body,ctx.topics(),ctx.problems());
   await ctx.session.flush();if(!valid(turn,actor))return;if(ctx.session.dirty())throw Error('Ноорог онлайн хадгалагдаагүй. Нийтлэхийн өмнө хадгалалтыг засна уу.');
   await ctx.session.pause();if(!valid(turn,actor))return;const snapshot=ctx.session.snapshot();
   root.replaceChildren(el('h3','Хичээлийг нийтлэх'),el('p',body.title+' · '+body.id+' · '+body.sections.length+' хэсэг'),el('p','Баталгаажуулбал энэ агуулга бүх уншигчид харагдана.'));
   const details=el('details');details.append(el('summary','Нийтлэх агуулгыг шалгах'));const pre=el('pre',JSON.stringify(body,null,2));pre.style.cssText='max-height:320px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere';details.append(pre);root.append(details);
   const status=el('p');status.setAttribute('role','status');const confirm=el('button','Баталгаажуулж нийтлэх'),cancel=el('button','Буцах');confirm.type=cancel.type='button';confirm.dataset.publishConfirm='true';cancel.onclick=close;root.append(status,confirm,cancel);root.scrollIntoView({block:'nearest'});cancel.focus({preventScroll:true});
   confirm.onclick=async()=>{if(confirm.disabled||!valid(turn,actor))return;confirm.disabled=cancel.disabled=true;
    try{const {data,error}=await ctx.client().rpc('admin_publish_tutorial_draft',{p_id:snapshot.id,p_body:body,p_base_revision:snapshot.baseRevision,p_draft_revision:snapshot.draftRevision,p_actor:actor});if(error)throw error;if(!valid(turn,actor))return;ctx.accept(data,actor,snapshot.id);close();ctx.message('Хичээл нийтлэгдлээ.');ctx.published?.(data);}
    catch(e){if(valid(turn,actor)){status.textContent=/REVISION_CONFLICT/.test(e.message)?'Хувилбар өөрчлөгджээ. Буцаад дахин ачаалж, засвараа сэргээнэ үү.':e.message;cancel.disabled=false;}}
   };
  }catch(e){if(valid(turn,actor)){root.replaceChildren(el('p',e.message));const cancel=el('button','Буцах');cancel.type='button';cancel.onclick=close;root.append(cancel);}}
 }
 root.hidden=true;return {open,invalidate:close};
}
