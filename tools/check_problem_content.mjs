import fs from'node:fs';
import {assertProblemContentReady,assertNewProblemRatingReady}from'../problem-content-policy.js';
import {assertProblemStatementReady}from'../problem-statement-policy.js';
const records=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(records.map(problem=>{
 let editorial_ready=false,statement_ready=false;const reasons=[];
 try{assertNewProblemRatingReady(problem);assertProblemContentReady(problem);editorial_ready=true;}catch(error){reasons.push(error.message);}
 try{assertProblemStatementReady(problem);statement_ready=true;}catch(error){reasons.push(error.message);}
 return{ready:editorial_ready&&statement_ready,editorial_ready,statement_ready,...(reasons.length?{reason:reasons.join(' ')}:{})};
})));
