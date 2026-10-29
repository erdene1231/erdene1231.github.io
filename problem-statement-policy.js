import {validateTutorial} from './tutorial-model.js?v=63';
export const STATEMENT_CHECKS=['task','input','output','constraints','samples','translation','rights'];
export function assertProblemStatementReady(problem){
 const body=problem.statement,provenance=problem.statementProvenance;if(!provenance||JSON.stringify(provenance).length>16384)throw Error('Statement provenance required, at most16KB.');
 if(!body)throw Error('Монгол/English tutorial-format statement шаардлагатай.');
 validateTutorial(body);
 for(const version of[body,body.translations?.en]){
  const substantive=b=>typeof b.text==='string'&&b.text.trim()||b.type==='rich'&&b.content.some(x=>x.text.trim())||b.type==='math'&&b.tex.trim()||['list','ordered','table'].includes(b.type);
  if(!version?.title?.trim()||!Array.isArray(version.sections)||version.sections.length<5||version.sections.slice(0,5).some(s=>!s.blocks.some(substantive)))throw Error('Statement: хоёр хэлний task/input/output/constraints/samples агуулгыг бүрдүүлнэ.');
 }
 const samples=v=>v.sections[4].blocks.filter(b=>b.type==='code').map(b=>b.text);
 const mn=samples(body),en=samples(body.translations.en);if(mn.length<2||mn.length%2!==0||JSON.stringify(mn)!==JSON.stringify(en))throw Error('MN/EN sample input/output literal текст ижил, хос code blocks байна.');
 let source;try{source=new URL(provenance?.sourceUrl);}catch{throw Error('Statement эх сурвалж шаардлагатай.');}
 if(source.href.length>1000||source.protocol!=='https:'||source.username||source.password||!/^([a-f0-9]{64})$/.test(provenance?.sourceSha256||''))throw Error('Statement HTTPS source/hash шаардлагатай.');
 if(!['original-functional-restatement','licensed','public-domain'].includes(provenance.rightsBasis))throw Error('Statement rights basis шаардлагатай.');
 if(['licensed','public-domain'].includes(provenance.rightsBasis)){let license;try{license=new URL(provenance.rightsReference);}catch{throw Error('License/permission reference шаардлагатай.');}if(license.href.length>1000||license.protocol!=='https:'||license.username||license.password)throw Error('License reference HTTPS байна.');}
 if(!/^\d{4}-\d{2}-\d{2}$/.test(provenance.reviewedAt||'')||Number.isNaN(Date.parse(provenance.reviewedAt+'T00:00:00Z'))||new Date(provenance.reviewedAt+'T00:00:00Z').toISOString().slice(0,10)!==provenance.reviewedAt)throw Error('Statement review date буруу.');
 if(STATEMENT_CHECKS.some(key=>provenance.checks?.[key]!==true))throw Error('Statement meaning/translation/samples/rights review дуусаагүй.');
 return problem;
}
