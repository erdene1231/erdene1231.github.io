import {priorityLevel} from './priority.js?v=52';
import {validateTutorial} from './tutorial-model.js?v=62';
import {drawArticle,typeset} from './tutorials.js?v=62';
import {mountBlockEditor} from './tutorial-block-editor.js?v=62';
import {uploadTutorialImage,tutorialImageUrl} from './tutorial-media.js?v=62';
const node=(tag,text,cls)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
const clearMath=root=>{try{window.MathJax?.typesetClear?.([root]);}catch{}};
const missing='Editorial одоогоор бэлтгэгдэж байна.';

// Catalog metadata carries only hasEditorial. Fetch the full tutorial document
// when the reader opens it; detached generations cannot update a new problem.
export function setupProblemEditorial(root,ctx){
 let turn=0,key=null;
 function clear(){turn++;key=null;clearMath(root);root.replaceChildren();root.hidden=true;}
 function render(problem){
  const next=[problem.id,problem.revision,problem.priorityLevel,!!problem.hasEditorial,!!problem.editorial].join('|');if(next===key)return;
  clear();key=next;if(!problem.hasEditorial&&!problem.editorial)return;
  root.hidden=false;const generation=turn,details=node('details'),summary=node('summary','Editorial'),message=node('p','Тайлбарыг нээж унших боломжтой.','muted'),article=node('article',undefined,'tutorial-content'),language=node('select'),label=node('label','Editorial-ийн хэл');
  for(const [value,text]of [['mn','Монгол'],['en','English']]){const o=node('option',text);o.value=value;language.append(o);}label.append(language);label.hidden=true;details.append(summary,label,message,article);root.append(details);
  let doc=null,pending=false;const valid=()=>turn===generation&&details.isConnected&&ctx.active(problem.id);
  async function paint(){if(!valid()||!doc)return;clearMath(article);const target=node('div');article.replaceChildren(target);const lang=language.value;message.textContent=lang==='en'&&!doc.translations?.en?'English translation is not published yet; showing Монгол.':'';article.lang=lang==='en'&&!doc.translations?.en?'mn':lang;
   try{await typeset([target],()=>drawArticle(doc,target,lang,{client:ctx.client(),viewerId:ctx.user?.()?.id||'public'}),()=>valid()&&language.value===lang&&target.isConnected);}catch{if(valid())message.textContent='Томьёог дүрсэлж чадсангүй; эх бичвэрийг харуулж байна.';}
  }
  async function load(){if(pending)return;if(doc){await paint();return;}if(!problem.editorial&&!problem.hasEditorial){message.textContent=missing;return;}pending=true;message.textContent='Editorial ачаалж байна…';
   try{let body=problem.editorial;if(!body){if(!ctx.client())throw Error('Онлайн editorial холболт шаардлагатай.');const result=await ctx.client().rpc('get_problem_editorial',{p_problem_id:problem.id});if(result.error)throw result.error;body=result.data?.body;}
    if(!valid())return;if(!body){message.textContent=missing;return;}validateTutorial(body);doc=structuredClone(body);label.hidden=false;await paint();
   }catch{if(valid())message.textContent='Editorial ачаалсангүй. Дахин нээж оролдоно уу.';}finally{pending=false;}
  }
  details.addEventListener('toggle',()=>{if(details.open)void load();});language.onchange=()=>void paint();
 }
 return{render,clear};
}

// The document and block editor are the tutorial editor's actual schema and
// component, including bilingual blocks, formatting, math, code and safe media.
export function setupProblemEditorialEditor(root,ctx){
 let turn=0,doc=null,editor=null,loading=false,failed=false,lang='mn',target=null,touched=false;
 const details=node('details'),summary=node('summary','Tutorial бүтэцтэй editorial'),message=node('p','', 'muted'),controls=node('div',undefined,'auth-actions'),create=node('button','Editorial үүсгэх'),remove=node('button','Editorial салгах'),language=node('select'),label=node('label','Хэл'),title=node('input'),titleLabel=node('label','Editorial гарчиг'),body=node('div');
 create.type=remove.type='button';for(const [value,text]of[['mn','Монгол'],['en','English']]){const o=node('option',text);o.value=value;language.append(o);}label.append(language);title.maxLength=200;titleLabel.append(title);controls.append(create,remove,label);details.append(summary,message,controls,titleLabel,body);root.append(details);
 const locked=()=>loading||ctx.locked();
 function version(){if(lang==='mn')return doc;doc.translations??={};return doc.translations.en??={title:'',sections:[]};}
 function paint(){editor?.destroy();editor=null;body.replaceChildren();titleLabel.hidden=remove.hidden=label.hidden=!doc;create.hidden=!!doc;create.disabled=locked();remove.disabled=locked();language.disabled=locked();title.disabled=locked();if(!doc)return;const v=version();title.value=v.title||'';const generation=turn,actor=ctx.user()?.id,id=doc.id;
  editor=mountBlockEditor(body,v.sections,{locked,changed:()=>{touched=true;},message:t=>message.textContent=t,problems:ctx.problems,progress:ctx.progress,
   uploadImage:async(file,current)=>{await ctx.requireBackend?.();return uploadTutorialImage(ctx.client(),id,file,actor,()=>generation===turn&&!locked()&&ctx.user()?.id===actor&&doc?.id===id&&current());},
   imageUrl:path=>tutorialImageUrl(ctx.client(),path,ctx.user()?.id,true)});
 }
 async function edit(problem){const generation=++turn;editor?.destroy();doc=null;target=problem;lang='mn';language.value=lang;touched=false;failed=false;loading=!!problem?.hasEditorial&&!problem.editorial;message.textContent=loading?'Editorial ачаалж байна…':'High priority-д шаталсан hint болон бүрэн editorial шаардлагатай.';details.open=false;paint();
  if(problem?.editorial){doc=structuredClone(problem.editorial);paint();return;}
  if(!loading)return;
  const actor=ctx.user()?.id;
  try{const result=await ctx.client().rpc('get_problem_editorial',{p_problem_id:problem.id});if(result.error)throw result.error;if(generation!==turn||actor!==ctx.user()?.id)return;
   if(result.data?.problemRevision!==problem.revision)throw Error('REVISION_CONFLICT');validateTutorial(result.data?.body);doc=structuredClone(result.data.body);message.textContent='Хадгалах үед бодлого болон editorial хамт шинэчлэгдэнэ.';
  }catch{if(generation===turn){failed=true;message.textContent='Editorial ачаалсангүй. Өгөгдөл алдахгүйн тулд бодлого хадгалахыг түр хориглолоо; дахин ачаална уу.';}}
  finally{if(generation===turn){loading=false;paint();}}
 }
 create.onclick=()=>{if(locked()||failed)return;doc={id:'problem-editorial-'+crypto.randomUUID(),title:(target?.title||'Бодлого')+' — Editorial',levelKey:'intermediate',order:1,category:'Problem editorial',sections:[{title:'Тайлбар',blocks:[]}]};touched=true;details.open=true;paint();};
 remove.onclick=()=>{if(locked()||!doc||!confirm('Editorial холбоосыг салгах уу? Хадгалах хүртэл серверийн хувилбар өөрчлөгдөхгүй.'))return;doc=null;touched=true;paint();};
 language.onchange=()=>{if(locked()||!doc)return;lang=language.value;paint();};title.oninput=()=>{if(locked()||!doc)return;version().title=title.value;touched=true;};
 window.addEventListener('beforeunload',e=>{if(touched){e.preventDefault();e.returnValue='';}});
 return{edit,markSaved(){touched=false;},collect(){if(loading||failed)throw Error('Editorial бүрэн ачаалагдаагүй байна. Дахин ачаална уу.');if(doc){validateTutorial(doc);return structuredClone(doc);}return touched?null:undefined;},invalidate(){turn++;editor?.destroy();doc=null;target=null;loading=false;failed=false;touched=false;paint();},dirty:()=>touched,refresh:paint};
}
