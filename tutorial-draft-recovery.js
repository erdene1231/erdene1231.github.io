// Explicit comparison/rebase; uses the existing 023 RPC and never publishes.
const el=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
export function mountDraftRecovery(root,ctx){
 let generation=0,active=false;
 const valid=(turn,actor)=>turn===generation&&ctx.allowed()&&ctx.user()?.id===actor;
 function close(){generation++;active=false;root.replaceChildren();root.hidden=true;ctx.session.resume();ctx.lock(false);}
 async function open(){
  if(active||!ctx.allowed())return;
  const actor=ctx.user()?.id,turn=++generation;active=true;ctx.lock(true);
  root.hidden=false;root.replaceChildren(el('p','Хувилбаруудыг ачаалж байна…'));
  try{
   ctx.capture();await ctx.session.pause();if(!valid(turn,actor))return;
   const local=ctx.candidate();if(!local||local.actor!==actor)throw Error('Харьцуулах ноорог сонгоно уу.');
   const id=local.id,{data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:id});
   if(error)throw error;if(!valid(turn,actor))return;
   root.replaceChildren(el('h3','Нооргийн хувилбаруудыг харьцуулах'),el('p','Агуулгаа шалгаж, үргэлжлүүлэх хувилбараа сонгоно уу. Энэ үйлдэл нийтлэгдсэн хичээлийг өөрчлөхгүй.'));
   const versions=[['local','Төхөөрөмжийн засвар',local.body,local.draftRevision],['draft','Онлайн ноорог',data.draft?.body,data.draft?.revision],['published','Нийтлэгдсэн хувилбар',data.current?.body,data.current?.revision]];
   let selected=null;
   const choices=el('div');root.append(choices);
   const status=el('p');status.setAttribute('role','status');
   const save=el('button','Сонгосон хувилбарыг ноорог болгон хадгалах');save.type='button';save.disabled=true;save.dataset.rebaseSave='true';
   for(const [key,label,body,rev] of versions){
    const detail=el('details'),summary=el('summary',label+' · revision '+(rev??0));detail.dataset.version=key;detail.append(summary);
    if(body){const pre=el('pre',JSON.stringify(body,null,2));pre.style.cssText='max-height:320px;overflow:auto;white-space:pre-wrap;overflow-wrap:anywhere';detail.append(pre);
     const choose=el('button',label+' сонгох');choose.type='button';choose.dataset.rebaseChoice=key;
     choose.onclick=()=>{selected=body;status.textContent=label+' сонгогдлоо.';save.disabled=false;};detail.append(choose);
    }else detail.append(el('p','Энэ хувилбар байхгүй.'));choices.append(detail);
   }
   const cancel=el('button','Буцах');cancel.type='button';cancel.onclick=close;
   save.onclick=async()=>{
    if(!selected||!valid(turn,actor)||save.disabled)return;
    for(const b of root.querySelectorAll('button'))b.disabled=true;
    try{
     // Retain the user's local edits even when they deliberately select another version.
     ctx.session.preserve(local);
     const {data:result,error}=await ctx.client().rpc('admin_rebase_tutorial_draft',{p_id:id,p_body:structuredClone(selected),p_current_revision:data.current?.revision??0,p_draft_revision:data.draft?.revision??0,p_actor:actor});
     if(error)throw error;if(!valid(turn,actor))return;
     ctx.accept(result,actor,id);close();ctx.message('Харьцуулсан хувилбар хувийн ноорогт хадгалагдлаа.');
    }catch(e){if(!valid(turn,actor))return;
     status.textContent=/REVISION_CONFLICT/.test(e.message)?'Харьцуулснаас хойш хувилбар өөрчлөгджээ. Буцаад дахин харьцуулна уу. Local засвар хэвээр.':e.message;
     // A stale comparison cannot retry against newer revisions without another review.
     cancel.disabled=false;
    }
   };
   root.append(status,save,cancel);
  }catch(e){if(valid(turn,actor)){root.replaceChildren(el('p',e.message));const cancel=el('button','Буцах');cancel.type='button';cancel.onclick=close;root.append(cancel);}}
 }
 root.hidden=true;return {open,invalidate:close};
}
