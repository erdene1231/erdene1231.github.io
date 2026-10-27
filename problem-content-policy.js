import {priorityLevel} from './priority.js?v=48';
import {validateTutorial} from './tutorial-model.js?v=48';

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
 if(!Array.isArray(problem.hints)||!Array.isArray(problem.hintsEn)||problem.hints.length!==3||problem.hintsEn.length!==3||[...problem.hints,...problem.hintsEn].some(x=>typeof x!=='string'||!x.trim()))throw new Error('High priority requires three staged hints in both languages.');
 if(!problem.editorial)throw new Error('High priority requires a tutorial-format editorial; an external URL alone is insufficient.');
 validateTutorial(problem.editorial);
 if(!problem.editorial.sections.some(s=>s.blocks.some(b=>b.type==='rich'&&b.content?.some(r=>r.text?.trim())||['p','code'].includes(b.type)&&b.text?.trim()||b.type==='math'&&b.tex?.trim())))throw new Error('High editorial requires substantive typed content.');
 return problem;
}
