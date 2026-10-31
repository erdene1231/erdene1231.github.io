import {dateKey} from './learning-model.js?v=87';
import {validActivityDay} from './profile-progress.js?v=1';
const datedToday=(stamp,today)=>typeof stamp==='string'&&Number.isFinite(Date.parse(stamp))&&dateKey(stamp)===today;
export function todayProblemItems(rows,problems,today,base){
 const catalog=new Map(problems.map(p=>[String(p.id),p])),seen=new Set(),items=[];
 for(const row of rows){const id=String(row.problem_id);if(seen.has(id)||row.status!=='solved'||!datedToday(row.first_solved_at,today))continue;seen.add(id);const p=catalog.get(id),url=base+'#problem/'+encodeURIComponent(id);items.push({id,url,aliases:p?.url?[p.url]:[],line:(p?.title||'Бодлого '+id)+' — '+url});}return items;
}
export function todayTutorialItems(records,tutorials,today,base){
 const titles=new Map(tutorials.map(row=>{const t=row.body||row;return[String(t.id),t.title];})),items=[],seen=new Set();
 for(const row of records){if(row.kind!=='tutorial'||seen.has(String(row.key)))continue;const r=row.value||{},days=Array.isArray(r.viewedDays)?r.viewedDays:[];if(!datedToday(r.viewedAt,today)&&!datedToday(r.completedAt,today)&&!days.some(day=>validActivityDay(day)&&day===today))continue;const id=String(row.key);seen.add(id);const url=base+'#tutorial/'+encodeURIComponent(id);items.push({id,url,aliases:[],line:(titles.get(id)||'Хичээл '+id)+' — '+url});}return items;
}
export function appendActivity(text,items,maxLength){
 const urls=new Set(text.match(/https?:\/\/[^\s<>]+|#(?:problem|tutorial)\/[^\s<>]+/g)||[]),add=[];for(const url of [...urls]){const fragment=url.slice(url.indexOf('#'));if(/^#(?:problem|tutorial)\//.test(fragment))urls.add(fragment);}
 for(const item of items){const fragment=item.url.slice(item.url.indexOf('#'));if(urls.has(item.url)||urls.has(fragment)||item.aliases.some(url=>urls.has(url)))continue;add.push(item.line);urls.add(item.url);urls.add(fragment);}
 const value=add.length?text+(text&&!text.endsWith('\n')?'\n':'')+add.join('\n'):text;if(value.length>maxLength)throw new Error('Талбарын урт хэтрэх тул юу ч нэмээгүй. Жагсаалтаа богиносгоод дахин оролдоорой.');return{value,added:add.length};
}

export async function loadOwnerActivity(client,table,fields,actor){
 const rows=[];
 for(let start=0;start<10000;start+=500){let query=client.from(table).select(fields).eq('user_id',actor);if(table==='learning_records')query=query.eq('kind','tutorial');const result=await query.order(table==='progress'?'problem_id':'key').range(start,start+499);if(result.error)throw result.error;if(!Array.isArray(result.data))throw new Error('Өдрийн үйлдлийн жагсаалт бүрэн бус байна.');rows.push(...result.data);if(result.data.length<500)return rows;}
 throw new Error('Өдрийн үйлдлийн жагсаалт хэт урт байна. Юу ч нэмээгүй.');
}
