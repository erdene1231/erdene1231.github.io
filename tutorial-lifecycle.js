// Admin-only lifecycle controls. Reviewing never changes public visibility.
const el=(tag,text)=>{const node=document.createElement(tag);if(text!==undefined)node.textContent=text;return node;};
const failure=e=>/REVISION_CONFLICT/.test(e.message)?'Хувилбар өөрчлөгджээ. Буцаад дахин ачаалах эсвэл хувилбаруудаа харьцуулна уу.':/still requires this prerequisite/.test(e.message)?'Өөр нийтлэгдсэн хичээл үүнийг урьдчилсан хичээлээр шаардсан байна. Эхлээд тэр холбоосыг засна уу.':/TUTORIAL_REFERENCED/.test(e.message)?'Өөр хичээл эсвэл хувийн ноорог энэ хичээл рүү холбоостой байна. Эхлээд холбоосыг засна уу.':/TUTORIAL_DELETED/.test(e.message)?'Хичээл үүрд устгагдсан байна. Дахин ачаална уу.':e.message;
export function mountTutorialLifecycle(root,ctx){
 let generation=0,active=false;
 const valid=(turn,actor)=>generation===turn&&ctx.allowed()&&ctx.user()?.id===actor;
 function close(){generation++;active=false;root.replaceChildren();root.hidden=true;ctx.session.resume();ctx.lock(false);}
 async function open(mode){
  if(active||!ctx.allowed()||!ctx.session.snapshot()||!['hide','restore','delete'].includes(mode))return;
  active=true;const turn=++generation,actor=ctx.user()?.id,permanent=mode==='delete';
  ctx.lock(true);root.hidden=false;root.replaceChildren(el('p','Хичээлийн төлөвийг шалгаж байна…'));
  try{
   ctx.capture();
   if(!permanent){await ctx.session.flush();if(!valid(turn,actor))return;if(ctx.session.dirty())throw Error('Эхлээд нооргоо онлайн хадгална уу. Хадгалаагүй засвар тань төхөөрөмжид үлдсэн.');}
   await ctx.session.pause();if(!valid(turn,actor))return;
   const snapshot=ctx.session.snapshot(),{data,error}=await ctx.client().rpc('admin_tutorial_document',{p_id:snapshot.id});
   if(error)throw error;if(!valid(turn,actor))return;const current=data?.current;
   if(!current)throw Error('Нийтэлж байсан хичээл олдсонгүй. Энэ нь зөвхөн хувийн ноорог байж болно.');
   if(!Number.isInteger(current.revision)||typeof current.published!=='boolean')throw Error('Хичээлийн төлөвийг баталгаажуулж чадсангүй. Дахин ачаална уу.');
   if((mode==='hide')!==current.published)throw Error('Хичээлийн төлөв өөрчлөгджээ. Буцаад дахин ачаална уу.');
   // 024 advances only a draft based on the current catalog revision. A stale
   // draft must be explicitly rebased, never replaced by the public body.
   if(!permanent&&(snapshot.baseRevision!==current.revision||data.draft?.base_revision!==current.revision||snapshot.draftRevision!==data.draft?.revision))throw Error('REVISION_CONFLICT: draft changed');
   const title=mode==='hide'?'Хичээлийг түр устгах':permanent?'Хичээлийг үүрд устгах':'Хичээлийг сэргээх';
   root.replaceChildren(el('h3',title),el('p',current.body.title+' · '+snapshot.id));
   root.append(el('p',permanent?'Энэ хичээлийн онлайн агуулга, бүх админы ноорог, засварын түүхийг бүрмөсөн устгана. Буцааж сэргээх боломжгүй. Бусад хичээлийн ID болон хэрэглэгчдийн progress өөрчлөгдөхгүй.':mode==='hide'?'Хичээл нийтийн жагсаалтаас хасагдана. Агуулга, ноорог, түүх, ID болон progress хадгалагдана. Дараа нь эндээс сэргээж болно.':'Хамгийн сүүлд нийтэлсэн агуулга ижил ID-тайгаар дахин харагдана. Хувийн ноорог тань нийтлэгдэхгүй.'));
   let input;
   if(permanent){const label=el('label','Баталгаажуулахын тулд хичээлийн ID-г бичнэ үү: '+snapshot.id);input=el('input');input.type='text';input.autocomplete='off';input.spellcheck=false;input.dataset.deleteId='true';label.append(input);root.append(label);}
   const status=el('p');status.setAttribute('role','status');
   const confirm=el('button',permanent?'Баталгаажуулж үүрд устгах':mode==='hide'?'Баталгаажуулж түр устгах':'Баталгаажуулж сэргээх'),cancel=el('button','Буцах');
   confirm.type=cancel.type='button';confirm.dataset.lifecycleConfirm=mode;cancel.dataset.lifecycleCancel='true';cancel.onclick=close;
   if(mode!=='restore')confirm.className='tutorial-danger';if(permanent){confirm.disabled=true;input.oninput=()=>{confirm.disabled=input.value!==snapshot.id;};}
   root.append(status,confirm,cancel);root.scrollIntoView({block:'nearest'});(input||cancel).focus({preventScroll:true});
   confirm.onclick=async()=>{
    if(confirm.disabled||!valid(turn,actor))return;confirm.disabled=cancel.disabled=true;if(input)input.disabled=true;
    try{
     const args={p_id:snapshot.id,p_revision:current.revision,p_actor:actor};
     if(permanent)args.p_confirmation=input.value;else args.p_published=mode==='restore';
     const {data:result,error}=await ctx.client().rpc(permanent?'admin_delete_tutorial':'admin_set_tutorial_publication',args);
     if(error)throw error;if(!valid(turn,actor))return;
     if(permanent){ctx.removed(result,actor,snapshot.id);close();ctx.message('Хичээл үүрд устгагдлаа. Бусад хичээлийн ID өөрчлөгдөөгүй.');}
     else{ctx.accept(result,actor,snapshot.id);close();ctx.message(mode==='hide'?'Хичээл түр устгагдлаа. Админ жагсаалтаас сонгож сэргээж болно.':'Хичээл сэргээгдлээ. Хувийн ноорог хадгалагдсан.');ctx.updated?.(result);}
    }catch(e){if(valid(turn,actor)){status.textContent=failure(e);cancel.disabled=false;}}
   };
  }catch(e){if(valid(turn,actor)){root.replaceChildren(el('p',failure(e)));const cancel=el('button','Буцах');cancel.type='button';cancel.dataset.lifecycleCancel='true';cancel.onclick=close;root.append(cancel);}}
 }
 root.hidden=true;return {open,invalidate:close};
}
