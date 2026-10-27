import {validatePriority} from './priority.js?v=42';
import {validateExtendedBlock} from './tutorial-blocks.js?v=42';
export const levels=['beginner','intermediate','advanced'];
export const levelNames={mn:['Анхан шат','Дунд шат','Ахисан шат'],en:['Beginner','Intermediate','Advanced']};
export function validateTutorial(t){
 const fail=message=>{throw new Error(message);};
 const str=(s,max,label)=>{if(typeof s!=='string'||!s.trim()||s.length>max)fail(label+' буруу эсвэл хэт урт байна.');};
 const optional=(s,max,label)=>{if(s!==undefined&&(typeof s!=='string'||s.length>max))fail(label+' буруу эсвэл хэт урт байна.');};
 if(!t||typeof t!=='object'||Array.isArray(t))fail('Хичээлийн бүтэц буруу.');
 validatePriority(t);
 if(!/^[a-z0-9-]{1,80}$/.test(t.id))fail('Хичээлийн ID буруу.');
 if(!levels.includes(t.levelKey)||!Number.isInteger(t.order)||t.order<1||t.order>1000)fail('Түвшин эсвэл дараалал буруу.');
 optional(t.category,80,'Бүлэг');optional(t.aliases,2000,'Хайлтын үг');
 if(t.prerequisiteIds!==undefined&&(!Array.isArray(t.prerequisiteIds)||t.prerequisiteIds.length>30||t.prerequisiteIds.some(x=>typeof x!=='string'||!/^[a-z0-9-]{1,80}$/.test(x))))fail('Урьдчилсан хичээлийн ID буруу.');
 if(t.related!==undefined&&(!Array.isArray(t.related)||t.related.length>30||t.related.some(x=>typeof x!=='string'||!/^[a-z0-9-]{1,80}$/.test(x))))fail('Холбоотой сэдвийн ID буруу.');
 for(const lang of ['mn','en']){const v=lang==='mn'?t:t.translations?.en;if(lang==='en'&&v==null)continue;if(!v)fail('Монгол агуулга шаардлагатай.');(lang==='mn'?str:optional)(v.title,200,'Гарчиг');optional(v.summary,4000,'Тайлбар');optional(v.prerequisites,2000,'Урьдчилан мэдэх зүйл');
  if(!Array.isArray(v.sections)||v.sections.length>80)fail('0–80 хэсэг байна.');
  for(const s of v.sections){optional(s.title,200,'Хэсгийн гарчиг');if(!Array.isArray(s.blocks)||s.blocks.length>100)fail('Хэсгийн агуулга буруу.');for(const b of s.blocks){
   if(!b||typeof b!=='object'||Array.isArray(b))fail('Block бүтэц буруу.');
   if(['p','note','code'].includes(b.type)){optional(b.text,40000,'Агуулга');if(b.type==='note'){if(b.collapsible!==undefined&&typeof b.collapsible!=='boolean')fail('Нээж унших тохиргоо буруу.');if(b.label!==undefined)str(b.label,200,'Нээх товчны нэр');}if(b.type==='code'&&b.language!==undefined)str(b.language,80,'Кодын төрөл');}
   else if(b.type==='math')str(b.tex,8000,'Томъёо');
   else if(['list','ordered'].includes(b.type)){if(!Array.isArray(b.items)||!b.items.length||b.items.length>100)fail('Жагсаалт буруу.');for(const x of b.items)str(x,8000,'Жагсаалтын мөр');}
   else if(b.type==='table'){if(!Array.isArray(b.headers)||!b.headers.length||b.headers.length>8||!Array.isArray(b.rows)||!b.rows.length||b.rows.length>100)fail('Хүснэгт буруу.');for(const h of b.headers)str(h,200,'Багана');for(const row of b.rows){if(!Array.isArray(row)||row.length!==b.headers.length)fail('Хүснэгтийн баганын тоо зөрсөн.');for(const c of row)str(c,8000,'Нүд');}}
   else if(b.type==='links'){if(!Array.isArray(b.items)||!b.items.length||b.items.length>30)fail('Холбоосын жагсаалт буруу.');for(const x of b.items){str(x.label,300,'Холбоосын нэр');str(x.url,1000,'Холбоос');let u;try{u=new URL(x.url);}catch{fail('Холбоос буруу.');}if(u.protocol!=='https:'||u.username||u.password)fail('HTTPS холбоос оруулна уу.');}}
   else if(!validateExtendedBlock(b))fail('Дэмжигдээгүй агуулгын төрөл.');
  }}
 }
 if(JSON.stringify(t).length>1000000)fail('Хичээл хэт том байна.');return t;
}
export const view=(t,lang)=>lang==='en'&&t.translations?.en?(t.translations.en.title?t.translations.en:{...t.translations.en,title:t.title}):t;
