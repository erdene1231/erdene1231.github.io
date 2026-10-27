import fs from'node:fs';
import{assertReviewedStatement}from'./statement_review_gate.mjs';
import {assertProblemContentReady,assertNewProblemRatingReady,assertProblemSelectionReady}from'../problem-content-policy.js';
import {assertProblemStatementReady}from'../problem-statement-policy.js';
const records=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(records.map(problem=>{
 let editorial_ready=false,statement_ready=false,selection_ready=false;const reasons=[],optional_content_notes=[];
 try{assertProblemSelectionReady(problem);selection_ready=true;}catch(error){reasons.push(error.message);}
 try{assertNewProblemRatingReady(problem);assertProblemContentReady(problem);editorial_ready=!!problem.editorial;}catch(error){optional_content_notes.push(error.message);}
 try{assertProblemStatementReady(problem);assertReviewedStatement(problem);statement_ready=true;}catch(error){optional_content_notes.push(error.message);}
 return{ready:selection_ready,selection_ready,full_content_ready:editorial_ready&&statement_ready,editorial_ready,statement_ready,optional_content_notes,...(reasons.length?{reason:reasons.join(' ')}:{})};
})));
