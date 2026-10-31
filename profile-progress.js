// Pure profile metrics; no persistence or access changes.
export function ratingColor(rating){
 if(rating<1200)return'grey';if(rating<1400)return'green';if(rating<1600)return'cyan';if(rating<1900)return'blue';if(rating<2100)return'magenta';if(rating<2400)return'orange';if(rating<3000)return'red';return'black';
}
export function ratingColumns(stats){
 const groups=new Map();let unknown=stats.unrated||0;
 for(const[key,count]of stats.ratings){const[kind,raw]=key.split('|'),rating=Number(raw);if(!Number.isFinite(rating)||rating<0){unknown+=count;continue;}const bucket=rating<800?700:Math.floor(rating/100)*100,row=groups.get(bucket)||{rating:bucket,official:0,estimated:0,total:0};row[kind==='official'?'official':'estimated']+=count;row.total+=count;groups.set(bucket,row);}
 if(!groups.size)return{columns:[],unknown,max:1};const first=groups.has(700)?700:800,last=Math.max(...groups.keys()),columns=[];
 for(let rating=first;rating<=last;rating+=100){const row=groups.get(rating)||{rating,official:0,estimated:0,total:0};columns.push({...row,label:rating===700?'<800':String(rating),range:rating===700?'800-аас доош':rating+'–'+(rating+99),color:ratingColor(rating)});}
 return{columns,unknown,max:Math.max(1,...columns.map(row=>row.total))};
}
export function highestSolvedProblem(week){return week.solved.filter(p=>Number.isFinite(p.rating)&&p.rating>=0&&p.ratingKind!=='unrated').reduce((best,p)=>!best||p.rating>best.rating?p:best,null);}
export function validActivityDay(day){
 if(typeof day!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(day))return false;
 const stamp=Date.parse(day+'T00:00:00Z');return Number.isFinite(stamp)&&new Date(stamp).toISOString().slice(0,10)===day;
}
export function weeklyTutorialActivity(records,start,end,dateKey){
 const viewed=[],completed=[];let unknownRead=0;
 const within=stamp=>typeof stamp==='string'&&Number.isFinite(Date.parse(stamp))&&dateKey(stamp)>=start&&dateKey(stamp)<end;
 for(const[id,value]of Object.entries(records||{})){
  const r=value&&typeof value==='object'?value:{},days=Array.isArray(r.viewedDays)?r.viewedDays.filter(validActivityDay):[];
  if(within(r.viewedAt)||days.some(day=>day>=start&&day<end))viewed.push(id);
  if(within(r.completedAt))completed.push(id);
  if(Array.isArray(r.readSections)&&r.readSections.length&&!Number.isFinite(Date.parse(r.viewedAt))&&!days.length)unknownRead++;
 }
 return{viewed,completed,unknownRead};
}
export function averageSolvedRating(week){
 const rated=week.solved.filter(p=>Number.isFinite(p.rating)&&p.rating>=0&&p.ratingKind!=='unrated');return rated.length?Math.round(rated.reduce((sum,p)=>sum+p.rating,0)/rated.length):null;
}
