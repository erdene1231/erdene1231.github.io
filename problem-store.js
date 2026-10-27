import {validateTutorial} from './tutorial-model.js?v=44';
import {canonicalProblemUrl,problemUrlIdentity} from './problem-url.js?v=44';
import {validatePriority,priorityLevel,isHighPriority} from './priority.js?v=44';
export function validateSource(value) {
 if(typeof value!=='string')throw new Error('Source нэр оруулна уу.');
 const name=value.trim().replace(/\s+/g,' ');
 if(!name||name.length>80||/[\u0000-\u001f\u007f]/.test(value))throw new Error('Source нэр 1–80 тэмдэгт байна.');
 return name;
}
export function getSources(problems, saved=[]) {
 const names=new Map();
 for(const value of ['Codeforces','CSES','EGOI','Other',...saved,...problems.map(p=>p.source)]) {
  const name=validateSource(value),key=name.toLowerCase();if(!names.has(key))names.set(key,name);
 }
 return [...names.values()].sort((a,b)=>a.localeCompare(b));
}
export function validateProblem(input) {
 validatePriority(input);
 const p={title:String(input.title||'').trim(),source:validateSource(input.source),ref:String(input.ref||'').trim(),url:canonicalProblemUrl(input.url),rating:input.ratingKind==='unrated'?null:Number(input.rating),ratingKind:input.ratingKind,level:input.level||'Practice',priority:isHighPriority(input),tags:[...new Set((input.tags||[]).map(t=>String(t).trim().toLowerCase()).filter(Boolean))],hints:input.hints===undefined?[]:input.hints,hintsEn:input.hintsEn===undefined?[]:input.hintsEn,lesson:String(input.lesson||'').trim()};
 if(!p.title||p.title.length>200||!p.ref||p.ref.length>80)throw new Error('Бодлогын нэр болон эх бодлогын ID-гаа шалгана уу.');
 if(p.source.toLowerCase()==='codeforces')p.source='Codeforces';
 const validUrl=s=>{try{const u=new URL(s);return u.protocol==='https:'&&!u.username&&!u.password&&String(s).length<=1000&&!/\s/.test(s);}catch{return false;}};
 if(!validUrl(p.url))throw new Error('HTTPS бодлогын холбоос оруулна уу.');
 if(input.editorialUrl){if(!validUrl(input.editorialUrl))throw new Error('Editorial HTTPS холбоос байх ёстой.');p.editorialUrl=input.editorialUrl;}
 if(p.ratingKind!=='unrated'&&(!Number.isInteger(p.rating)||p.rating<800||p.rating>4000))throw new Error('Rating 800–4000 хүрээнд байна.');
 if(!['official','estimated','unrated'].includes(p.ratingKind)||(p.ratingKind==='official'&&p.source!=='Codeforces'))throw new Error('Rating-ийн төрлийг зөв сонгоно уу.');
 if(!['Practice','Interactive'].includes(p.level))throw new Error('Бодлогын төрөл сонгоно уу.');
 if(p.tags.length<1||p.tags.length>20||p.tags.some(t=>!/^[a-zA-Z0-9 +/&()_-]{1,50}$/.test(t)))throw new Error('1–20 English tag оруулна уу; tag тус бүр 50 тэмдэгт хүртэл.');
 for(const hints of [p.hints,p.hintsEn])if(!Array.isArray(hints)||![0,3].includes(hints.length)||hints.some(h=>typeof h!=='string'||!h.trim()||h.length>3000))throw new Error('Hint-гүй бол хоёуланг нь орхи; hint-тэй бол хэл тус бүрд 3 hint, hint бүр 1–3000 тэмдэгт байна.');
 if(p.hints.length!==p.hintsEn.length)throw new Error('Монгол болон English hint-ийн тоо ижил байна.');
 if(p.lesson.length>2000)throw new Error('Бодсоны дараах тайлбар 2000 тэмдэгт хүртэл байна.');
 for(const key of ['sourceId','sourceCategory','verifiedAt','difficultyCategory','ratingBasis','ratingConfidence','ratingEstimatedAt'])if(typeof input[key]==='string'&&input[key].length<=500)p[key]=input[key];
 for(const key of ['ratingSource','ratingVerifiedAt'])if(Object.hasOwn(input,key)){if(typeof input[key]!=='string'||input[key].length>500||(key==='ratingSource'&&!validUrl(input[key])))throw new Error('Rating provenance талбар буруу байна.');p[key]=input[key];}
 if(Object.hasOwn(input,'sourceTags')){if(!Array.isArray(input.sourceTags)||input.sourceTags.length>20||input.sourceTags.some(t=>typeof t!=='string'||!/^[a-zA-Z0-9 +/&()_*-]{1,50}$/.test(t)))throw new Error('Source tags буруу байна.');p.sourceTags=[...input.sourceTags];}
 if(Object.hasOwn(input,'editorial')){validateTutorial(input.editorial);p.editorial=structuredClone(input.editorial);}
 if(Object.hasOwn(input,'priorityLevel'))p.priorityLevel=priorityLevel(input);if(Object.hasOwn(input,'priorityReason'))p.priorityReason=input.priorityReason;
 return p;
}
export function parseCatalog(document) {
 if(!document||!Array.isArray(document.problems)||!Array.isArray(document.knownIds))throw new Error('Бодлогын сангийн хариу буруу байна.');
 if(document.sources!==undefined&&(!Array.isArray(document.sources)||document.sources.some(s=>{try{validateSource(s);return false;}catch{return true;}})))throw new Error('Source жагсаалт буруу байна.');
 const ids=new Set(),numbers=new Set();
 for(const p of document.problems){validateProblem(p);if(typeof p.id!=='string'||!/^[a-zA-Z0-9_-]{1,100}$/.test(p.id)||ids.has(p.id)||!Number.isSafeInteger(p.number)||p.number<1||numbers.has(p.number))throw new Error('Бодлогын ID давхардсан эсвэл буруу байна.');ids.add(p.id);numbers.add(p.number);}
 if(document.knownIds.some(id=>typeof id!=='string'||!/^[a-zA-Z0-9_-]{1,100}$/.test(id))||[...ids].some(id=>!document.knownIds.includes(id)))throw new Error('Бодлогын ID жагсаалт буруу байна.');
 return {...document,problems:document.problems.map(p=>({...p,url:canonicalProblemUrl(p.url)}))};
}
export function hintTexts(problem,language) {return priorityLevel(problem)==='low'?[]:(language==='en'?problem.hintsEn:problem.hints)||[];}

export function parseProblemImport(document) {
 const list=Array.isArray(document)?document:Array.isArray(document?.problems)?document.problems:[document];
 if(list.length<1||list.length>200)throw new Error('Нэг удаад 1–200 бодлого оруулна уу.');
 const urls=new Set(),refs=new Set();
 return list.map((input,index)=>{
  try {
   if(!input||typeof input!=='object'||Array.isArray(input)||!Array.isArray(input.tags))throw new Error('Бодлогын object болон tags array шаардлагатай.');
   if(!Object.hasOwn(input,'priorityLevel')&&typeof input.priority!=='boolean')throw new Error('Priority нь true эсвэл false байна.');
   const p=validateProblem(input),key=p.source.toLowerCase()+'|'+p.ref.toLowerCase();
   if(urls.has(problemUrlIdentity(p.url))||refs.has(key))throw new Error('Файл дотор бодлого давхардсан байна.');
   urls.add(problemUrlIdentity(p.url));refs.add(key);return p;
  }catch(e){throw new Error('Бодлого '+(index+1)+': '+e.message);}
 });
}
