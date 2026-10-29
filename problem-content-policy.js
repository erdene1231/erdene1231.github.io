import {priorityLevel} from './priority.js?v=52';
import {validateTutorial} from './tutorial-model.js?v=62';

export function assertNewProblemRatingReady(problem) {
 if(!Number.isInteger(problem.rating)||problem.rating<800||problem.rating>4000||!['official','estimated'].includes(problem.ratingKind))throw new Error('Every new problem needs a numeric official or estimated rating.');
 if(typeof problem.ratingBasis!=='string'||!problem.ratingBasis.trim())throw new Error('New rating requires a documented basis/calibration rationale.');
 let source;try{source=new URL(problem.ratingSource);}catch{throw new Error('Rating source is required.');}
 if(source.protocol!=='https:'||source.username||source.password)throw new Error('Rating source must be a safe HTTPS URL.');
 const date=problem.ratingKind==='estimated'?problem.ratingEstimatedAt:problem.ratingVerifiedAt;
 if(typeof date!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(date)||!Number.isFinite(Date.parse(date))||new Date(date).toISOString().slice(0,10)!==date)throw new Error('Rating verification/estimation date is required.');
 if(problem.ratingKind==='official'&&(problem.source!=='Codeforces'||source.hostname!=='codeforces.com'))throw new Error('Only source-verified Codeforces ratings are official.');
 if(problem.ratingKind==='estimated'&&(problem.rating%100!==0||typeof problem.ratingConfidence!=='string'||!problem.ratingConfidence.trim()))throw new Error('CF-scale estimates use100-point steps and explicit confidence.');
 return problem;
}

// Completeness gate for newly prepared content. Reading historical catalog rows
// remains non-destructive; this never changes stored hints or learner progress.
export function assertProblemContentReady(problem) {
 const level=priorityLevel(problem);
 if(level==='low') {
  if((problem.hints?.length||0)||(problem.hintsEn?.length||0))throw new Error('New Low content must not offer hints; preserve historical arrays separately.');
  return problem;
 }
 if(level!=='high')return problem;
 if(!problem.editorial)return problem;
 validateTutorial(problem.editorial);
 if(!problem.editorial.sections.some(s=>s.blocks.some(b=>b.type==='rich'&&b.content?.some(r=>r.text?.trim())||['p','code'].includes(b.type)&&b.text?.trim()||b.type==='math'&&b.tex?.trim())))throw new Error('High editorial requires substantive typed content.');
 return problem;
}

// Package4 selection gate: optional authored documents never stand in for review.
export function assertProblemSelectionReady(problem){
 assertNewProblemRatingReady(problem);
 if(!Array.isArray(problem.tags)||!problem.tags.length||problem.tags.some(t=>typeof t!=='string'||!t.trim()))throw Error('Reviewed tags required.');
 if(!['low','medium','high'].includes(problem.priorityLevel)||!problem.priorityReason?.trim())throw Error('Individual priority and rationale required.');
 if(!String(problem.learningObjective||problem.curationReason||'').trim())throw Error('Concise educational usefulness rationale required.');
 if(!problem.title?.trim()||!problem.ref?.trim())throw Error('Problem identity required.');
 let link;try{link=new URL(problem.url);}catch{throw Error('Problem link required.');}
 if(link.protocol!=='https:'||link.username||link.password)throw Error('Safe problem link required.');
 assertProblemContentReady(problem);return problem;
}
