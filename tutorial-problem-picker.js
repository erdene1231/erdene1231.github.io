import {canonicalKey} from './learning-model.js?v=39';

// Block references use canonical keys; search also accepts the site's stable IDs
// and visible problem numbers. Keep every catalog entry searchable without a cap.
export function problemPickerRows(problems,query=''){
 const rows=new Map();
 for(const problem of problems){
  if(problem.archived)continue;
  const key=canonicalKey(problem),terms=[problem.title,problem.source,problem.ref,problem.id,problem.sourceId,problem.number,problem.number!==undefined?'#'+problem.number:null,problem.url,key].filter(v=>v!==undefined&&v!==null).join(' ').toLocaleLowerCase();
  const existing=rows.get(key);
  if(existing){existing.searchText+=' '+terms;continue;}
  rows.set(key,{key,problem,searchText:terms});
 }
 const words=query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
 return [...rows.values()].filter(row=>words.every(word=>row.searchText.includes(word)));
}
