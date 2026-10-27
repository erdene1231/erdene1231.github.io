// Canonical priority is independent of rating/difficulty. Legacy values remain readable.
export const PRIORITY_LEVELS=['low','medium','high'];
export function priorityLevel(item){return PRIORITY_LEVELS.includes(item?.priorityLevel)?item.priorityLevel:item?.priority===true?'high':'medium';}
export const priorityRank=item=>PRIORITY_LEVELS.indexOf(priorityLevel(item));
export const isHighPriority=item=>priorityLevel(item)==='high';
export function priorityLabel(item){const level=priorityLevel(item);return level[0].toUpperCase()+level.slice(1)+' priority';}
export function validatePriority(input){
 if(Object.hasOwn(input,'priorityLevel')&&!PRIORITY_LEVELS.includes(input.priorityLevel))throw new Error('Priority нь Low, Medium эсвэл High байна.');
 if(Object.hasOwn(input,'priorityReason')&&(typeof input.priorityReason!=='string'||input.priorityReason.length>1000))throw new Error('Priority үндэслэл 1000 тэмдэгт хүртэл байна.');
 return input;
}
export function ratingClass(problem){
 if(problem?.ratingKind==='unrated'||!Number.isFinite(problem?.rating))return 'rating-unrated';
 const r=problem.rating;
 // Intermediate values retain their data; each band continues up to the next lower bound.
 return 'rating-'+(r<1200?'newbie':r<1400?'pupil':r<1600?'specialist':r<1900?'expert':r<2100?'candidate-master':r<2400?'master':r<3000?'grandmaster':'legendary');
}
