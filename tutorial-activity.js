import {dateKey} from './learning-model.js?v=87';
// Explicit reading events are independent of mastery checks and practice solves.
export function readState(record={},count=0){
 const sections=new Set((record.readSections||[]).filter(i=>Number.isInteger(i)&&i>=0&&i<count));
 return{viewed:sections.size>0,complete:count>0&&sections.size===count,read:sections.size};
}
export function tutorialActivity(record,type,count,options={}){
 if(!['viewed','completed'].includes(type))throw Error('Unknown reading activity');
 const previous=structuredClone(record||{}),now=options.now||new Date().toISOString();
 const pending=previous._activityEvent;
 const event=!options.newEvent&&pending?.type===type&&dateKey(now)===dateKey(pending.requestedAt)&&Math.abs(Date.parse(now)-Date.parse(pending.requestedAt))<600000?structuredClone(pending):{id:options.id||crypto.randomUUID(),type,requestedAt:now};
 if(Number.isInteger(count)&&count>0&&count<=1000)event.sectionCount=count;
 event.preserve=pending?.preserve||Object.keys(previous).filter(k=>!['readSections','_activityEvent','viewedAt','viewedDays','completedAt','viewEventId','completionEventId'].includes(k));
 if(type==='completed'){
  if(!Number.isInteger(count)||count<1||count>1000)throw Error('Invalid section count');
  if(readState(previous,count).complete&&!previous._activityEvent)return previous;
  previous.readSections=[...new Set([...(previous.readSections||[]),...Array.from({length:count},(_,i)=>i)])];event.sectionCount=count;
 }
 if(options.guest){
  previous.viewedAt=now;previous.viewedDays=[...new Set([...(previous.viewedDays||[]),dateKey(now)])];
  if(type==='completed'&&!previous.completedAt)previous.completedAt=now;
 }else previous._activityEvent=event;
 return previous;
}
export function tutorialWeek(records,start,end,dateKey){
 const within=s=>typeof s==='string'&&!Number.isNaN(Date.parse(s))&&dateKey(s)>=start&&dateKey(s)<end;
 return{viewed:Object.entries(records).filter(([,r])=>within(r.viewedAt)||(r.viewedDays||[]).some(day=>typeof day==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(day)&&day>=start&&day<end)).map(([id])=>id),completed:Object.entries(records).filter(([,r])=>within(r.completedAt)).map(([id])=>id)};
}
export function sectionActivity(record,index,count,options={}){
 if(!Number.isInteger(index)||index<0||index>=count)throw Error('Invalid tutorial section');
 if((record.readSections||[]).includes(index))return structuredClone(record);
 const next={...record,readSections:[...new Set([...(record.readSections||[]),index])]};
 return readState(next,count).complete?tutorialActivity(record,'completed',count,{...options,newEvent:true}):tutorialActivity(next,'viewed',count,{...options,newEvent:true});
}
