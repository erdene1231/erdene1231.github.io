import {normalizeProblemReferences,stableStringify} from './learning-model.js?v=69';
export function comparableBody(value,problems=[]){
 if(!value)return null;const body=normalizeProblemReferences(value,problems);delete body.searchText;delete body.revision;
 if(typeof body._draftRelationsText==='string')try{body.learningRelations=JSON.parse(body._draftRelationsText);delete body._draftRelationsText;}catch{}
 const rel=body.learningRelations;if(rel&&!rel.practice?.length&&!rel.variants?.length&&!rel.next)delete body.learningRelations;
 for(const field of ['summary','prerequisites','category','aliases'])body[field]??='';body.related??=[];body.prerequisiteIds??=[];
 if(body.translations?.en){const en=body.translations.en;if(!en.title?.trim()&&!en.summary?.trim()&&!en.prerequisites?.trim()&&!en.sections?.length)delete body.translations.en;}
 if(body.translations&&!Object.keys(body.translations).length)delete body.translations;
 return body;
}
export const sameEditorBody=(a,b,problems=[])=>stableStringify(comparableBody(a,problems))===stableStringify(comparableBody(b,problems));
