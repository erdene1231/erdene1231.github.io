import fs from'node:fs';
import {assertProblemContentReady,assertNewProblemRatingReady}from'../problem-content-policy.js';
const records=JSON.parse(fs.readFileSync(0,'utf8'));
process.stdout.write(JSON.stringify(records.map(problem=>{try{assertNewProblemRatingReady(problem);assertProblemContentReady(problem);return{ready:true};}catch(error){return{ready:false,reason:error.message};}})));
