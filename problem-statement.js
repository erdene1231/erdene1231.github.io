import {assertProblemStatementReady,STATEMENT_CHECKS} from './problem-statement-policy.js?v=63';
import {validateTutorial} from './tutorial-model.js?v=63';
import {drawArticle,typeset} from './tutorials.js?v=68';
import {mountBlockEditor} from './tutorial-block-editor.js?v=68';
import {uploadTutorialImage,tutorialImageUrl} from './tutorial-media.js?v=63';
const node=(tag,text,cls)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;};
const clearMath=root=>{try{window.MathJax?.typesetClear?.([root]);}catch{}};

// Catalog metadata carries only hasStatement. Fetch the full tutorial document
// when the reader opens it; detached generations cannot update a new problem.
export function setupProblemStatement(root,ctx){
 let turn=0,key=null;
 function clear(){turn++;key=null;clearMath(root);root.replaceChildren();root.hidden=true;}
 function render(problem){
  const next=[problem.id,problem.revision,problem.priorityLevel,!!problem.hasStatement,!!problem.statement].join('|');if(next===key)return;
  clear();key=next;if(!problem.hasStatement&&!problem.statement)return;
  root.hidden=false;const generation=turn,details=node('details'),summary=node('summary','Бодлогын нөхцөл / Statement'),message=node('p','Бодлогын нөхцөл, оролт/гаралт, хязгаарлалт, жишээ.','muted'),article=node('article',undefined,'tutorial-content'),language=node('select'),label=node('label','Statement-ийн хэл');
  for(const [value,text]of [['mn','Монгол'],['en','English']]){const o=node('option',text);o.value=value;language.append(o);}label.append(language);label.hidden=true;details.append(summary,label,message,article);root.append(details);
  let doc=null,pending=false;const attribution=node('p',undefined,'muted');details.insertBefore(attribution,article);const valid=()=>turn===generation&&details.isConnected&&ctx.active(problem.id);
  async function paint(){if(!valid()||!doc)return;clearMath(article);const target=node('div');article.replaceChildren(target);const lang=language.value;message.textContent='';article.lang=lang;if(lang==='en'&&!doc.translations?.en){message.textContent='English statement одоогоор бэлтгэгдэж байна.';return;}
   try{await typeset([target],()=>drawArticle(doc,target,lang,{client:ctx.client(),viewerId:ctx.user?.()?.id||'public'}),()=>valid()&&language.value===lang&&target.isConnected);}catch{if(valid())message.textContent='Томьёог дүрсэлж чадсангүй; эх бичвэрийг харуулж байна.';}
  }
  async function load(){if(pending)return;if(doc){await paint();return;}if(!problem.statement&&!problem.hasStatement){message.textContent='Монгол/English statement хараахан бүрдээгүй. Эх бодлогын холбоосоор бүрэн нөхцөлийг үзнэ үү.';return;}pending=true;message.textContent='Statement ачаалж байна…';
   try{let body=problem.statement,provenance=problem.statementProvenance;if(!body){if(!ctx.client())throw Error('Онлайн statement холболт шаардлагатай.');const result=await ctx.client().rpc('get_problem_statement',{p_problem_id:problem.id});if(result.error)throw result.error;body=result.data?.body;provenance=result.data?.provenance;}
    if(!valid())return;if(!body){message.textContent='Монгол/English statement хараахан бүрдээгүй. Эх бодлогын холбоосоор бүрэн нөхцөлийг үзнэ үү.';return;}assertProblemStatementReady({statement:body,statementProvenance:provenance});const source=node('a','Эх сурвалж / Source');source.href=provenance.sourceUrl;source.target='_blank';source.rel='noopener noreferrer';attribution.replaceChildren(source,document.createTextNode(provenance.rightsBasis==='original-functional-restatement'?' · Original functional restatement':' · '+provenance.rightsBasis));doc=structuredClone(body);label.hidden=false;await paint();
   }catch{if(valid())message.textContent='Statement ачаалсангүй. Дахин нээж оролдоно уу.';}finally{pending=false;}
  }
  details.addEventListener('toggle',()=>{if(details.open)void load();});language.onchange=()=>void paint();details.open=true;
 }
 return{render,clear};
}

// The document and block editor are the tutorial editor's actual schema and
// component, including bilingual blocks, formatting, math, code and safe media.
export function setupProblemStatementEditor(root,ctx){
 let turn=0,doc=null,editor=null,loading=false,failed=false,lang='mn',target=null,touched=false;
 const details=node('details'),summary=node('summary','Tutorial бүтэцтэй statement'),message=node('p','', 'muted'),controls=node('div',undefined,'auth-actions'),create=node('button','Statement үүсгэх'),remove=node('button','Statement салгах'),language=node('select'),label=node('label','Хэл'),title=node('input'),titleLabel=node('label','Statement гарчиг'),body=node('div');
 create.type=remove.type='button';for(const [value,text]of[['mn','Монгол'],['en','English']]){const o=node('option',text);o.value=value;language.append(o);}label.append(language);title.maxLength=200;titleLabel.append(title);controls.append(create,remove,label);details.append(summary,message,controls,titleLabel,body);root.append(details);
 const metadata=node('fieldset'),metaLegend=node('legend','Statement эх сурвалж ба review'),sourceInput=node('input'),hashInput=node('input'),rights=node('select'),rightsReference=node('input'),reviewDate=node('input'),reviewed=node('input');metadata.append(metaLegend);
 for(const[value,text]of[['original-functional-restatement','Өөрийн functional restatement'],['licensed','License / permission'],['public-domain','Public domain']]){const option=node('option',text);option.value=value;rights.append(option);}
 sourceInput.type=rightsReference.type='url';sourceInput.maxLength=rightsReference.maxLength=1000;hashInput.maxLength=64;reviewDate.type='date';reviewed.type='checkbox';
 for(const[text,input]of[['Authoritative source URL',sourceInput],['Source SHA-256',hashInput],['Rights basis',rights],['License/permission reference',rightsReference],['Reviewed date',reviewDate],['Task, input/output, exact constraints/samples, MN/EN meaning ба rights-ийг шалгасан',reviewed]]){const label=node('label',text);label.append(input);metadata.append(label);input.addEventListener('input',()=>{touched=true;if(input!==reviewed)reviewed.checked=false;});}details.insertBefore(metadata,body);
 function setProvenance(value){sourceInput.value=value?.sourceUrl||target?.url||'';hashInput.value=value?.sourceSha256||'';rights.value=value?.rightsBasis||'original-functional-restatement';rightsReference.value=value?.rightsReference||'';reviewDate.value=value?.reviewedAt||new Date().toISOString().slice(0,10);reviewed.checked=STATEMENT_CHECKS.every(key=>value?.checks?.[key]===true);}
 function collectProvenance(){return{sourceUrl:sourceInput.value.trim(),sourceSha256:hashInput.value.trim(),rightsBasis:rights.value,...(rightsReference.value.trim()?{rightsReference:rightsReference.value.trim()}:{}),reviewedAt:reviewDate.value,checks:Object.fromEntries(STATEMENT_CHECKS.map(key=>[key,reviewed.checked]))};}
 const locked=()=>loading||ctx.locked();
 function version(){if(lang==='mn')return doc;doc.translations??={};return doc.translations.en??={title:'',sections:['Task','Input','Output','Constraints','Samples'].map(title=>({title,blocks:[]}))};}
 function paint(){metadata.hidden=!doc;for(const input of metadata.querySelectorAll('input,select'))input.disabled=locked();editor?.destroy();editor=null;body.replaceChildren();titleLabel.hidden=remove.hidden=label.hidden=!doc;create.hidden=!!doc;create.disabled=locked();remove.disabled=locked();language.disabled=locked();title.disabled=locked();if(!doc)return;const v=version();title.value=v.title||'';const generation=turn,actor=ctx.user()?.id,id=doc.id;
  editor=mountBlockEditor(body,v.sections,{locked,changed:()=>{touched=true;reviewed.checked=false;},message:t=>message.textContent=t,problems:ctx.problems,progress:ctx.progress,
   uploadImage:async(file,current)=>{await ctx.requireBackend?.();return uploadTutorialImage(ctx.client(),id,file,actor,()=>generation===turn&&!locked()&&ctx.user()?.id===actor&&doc?.id===id&&current());},
   imageUrl:path=>tutorialImageUrl(ctx.client(),path,ctx.user()?.id,true)});
 }
 async function edit(problem){const generation=++turn;editor?.destroy();doc=null;target=problem;setProvenance(problem?.statementProvenance);lang='mn';language.value=lang;touched=false;failed=false;loading=!!problem?.hasStatement&&!problem.statement;message.textContent=loading?'Statement ачаалж байна…':'Priority-гаас үл хамааран statement нь Монгол/English task, I/O, constraints, samples-тай байна.';details.open=false;paint();
  if(problem?.statement){doc=structuredClone(problem.statement);paint();return;}
  if(!loading)return;
  const actor=ctx.user()?.id;
  try{const result=await ctx.client().rpc('get_problem_statement',{p_problem_id:problem.id});if(result.error)throw result.error;if(generation!==turn||actor!==ctx.user()?.id)return;
   if(result.data?.problemRevision!==problem.revision)throw Error('REVISION_CONFLICT');validateTutorial(result.data?.body);doc=structuredClone(result.data.body);setProvenance(result.data.provenance);message.textContent='Хадгалах үед бодлого болон statement хамт шинэчлэгдэнэ.';
  }catch{if(generation===turn){failed=true;message.textContent='Statement ачаалсангүй. Өгөгдөл алдахгүйн тулд бодлого хадгалахыг түр хориглолоо; дахин ачаална уу.';}}
  finally{if(generation===turn){loading=false;paint();}}
 }
 create.onclick=()=>{if(locked()||failed)return;doc={id:'problem-statement-'+crypto.randomUUID(),title:(target?.title||'Бодлого')+' — Statement',levelKey:'intermediate',order:1,category:'Problem statement',sections:['Бодлогын нөхцөл','Оролт','Гаралт','Хязгаарлалт','Жишээ'].map(title=>({title,blocks:[]}))};touched=true;details.open=true;paint();};
 remove.onclick=()=>{if(locked()||!doc||!confirm('Statement холбоосыг салгах уу? Хадгалах хүртэл серверийн хувилбар өөрчлөгдөхгүй.'))return;doc=null;touched=true;paint();};
 language.onchange=()=>{if(locked()||!doc)return;lang=language.value;paint();};title.oninput=()=>{if(locked()||!doc)return;version().title=title.value;touched=true;reviewed.checked=false;};
 window.addEventListener('beforeunload',e=>{if(touched){e.preventDefault();e.returnValue='';}});
 return{edit,markSaved(){touched=false;},collect(){if(loading||failed)throw Error('Statement бүрэн ачаалагдаагүй байна. Дахин ачаална уу.');if(doc){assertProblemStatementReady({statement:doc,statementProvenance:collectProvenance()});return structuredClone(doc);}return touched?null:undefined;},invalidate(){turn++;editor?.destroy();doc=null;target=null;loading=false;failed=false;touched=false;paint();},provenance:collectProvenance,dirty:()=>touched,refresh:paint};
}
