import {validateGraphStyle} from './tutorial-graph.js?v=55';
// Typed content, never arbitrary HTML. Old block shapes stay valid.
export const BLOCK_TYPES=['p','rich','heading','code','math','list','ordered','checklist','table','links','quote','callout','note','divider','image','diagram','problem','tutorial'];
export const MARKS=['bold','italic','underline','strike','code'];
export const TONES=['note','important','warning','example','proof','observation','complexity','mistake'];
export const MEDIA_BUCKET='tutorial-media';
export const validMediaPath=value=>typeof value==='string'&&/^[a-z0-9-]{1,80}\/[0-9a-f-]{36}\/[0-9a-f-]{36}\.webp$/.test(value);
export function safeLink(value){
 if(typeof value!=='string'||value.length>1000||/[\s\\]/.test(value))return null;
 if(/^#(?:tutorial\/[a-z0-9-]{1,80}(?:\/part\/\d+)?|tutorials|library|plan(?:\/\d+)?|profile(?:\/[a-zA-Z0-9_-]+)?)$/.test(value))return value;
 if(!value.startsWith('https://'))return null;
 try{const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password?u.href:null;}catch{return null;}
}
export function validateInline(content){
 if(!Array.isArray(content)||content.length>1000)throw new Error('Inline content 1–1000 хэсэгтэй байна.');
 let size=0;for(const item of content){if(!item||typeof item.text!=='string'||item.text.length>40000)throw new Error('Inline text буруу.');size+=item.text.length;if(item.marks!==undefined&&(!Array.isArray(item.marks)||item.marks.length>20||item.marks.some(m=>!MARKS.includes(m))))throw new Error('Дэмжигдээгүй formatting.');if(item.href!==undefined&&!safeLink(item.href))throw new Error('Аюулгүй HTTPS эсвэл дотоод холбоос оруулна уу.');}
 if(size>40000)throw new Error('Formatting хийсэн текст хоосон эсвэл хэт урт байна.');return content;
}
export function plainInline(content){return (content||[]).map(x=>x.text).join('');}
export function validateExtendedBlock(b){
 if(!b||typeof b!=='object'||Array.isArray(b))throw new Error('Block бүтэц буруу.');
 if(b.caption!==undefined&&(typeof b.caption!=='string'||b.caption.length>2000))throw new Error('Caption буруу.');
 const text=(value,max=40000)=>{if(typeof value!=='string'||!value.trim()||value.length>max)throw new Error('Агуулга хоосон эсвэл хэт урт байна.');};
 if(b.type==='rich'){validateInline(b.content);return true;}
 if(b.type==='heading'){if(!Number.isInteger(b.level)||b.level<1||b.level>4)throw new Error('H1–H4 гарчиг сонгоно уу.');text(b.text,200);return true;}
 if(b.type==='divider')return true;
 if(b.type==='quote'||b.type==='callout'){if('content' in b)validateInline(b.content);else text(b.text);if(b.title!==undefined&&(typeof b.title!=='string'||b.title.length>200))throw new Error('Callout гарчиг хэт урт.');if(b.type==='callout'&&!TONES.includes(b.tone))throw new Error('Callout төрөл буруу.');return true;}
 if(b.type==='checklist'){if(!Array.isArray(b.items)||!b.items.length||b.items.length>100)throw new Error('Checklist 1–100 мөртэй байна.');for(const item of b.items){text(item.text,8000);if(typeof item.checked!=='boolean')throw new Error('Checklist төлөв буруу.');}return true;}
 if(b.type==='image'){if(!validMediaPath(b.path))throw new Error('Tutorial Storage зураг сонгоно уу.');text(b.alt,500);if(b.caption!==undefined&&String(b.caption).length>2000)throw new Error('Caption хэт урт.');if(!['left','center','right'].includes(b.align)||!Number.isInteger(b.width)||b.width<20||b.width>100)throw new Error('Зургийн байрлал/өргөн буруу.');return true;}
 if(b.type==='problem'){text(b.problemKey,200);if(!/^(?:[1-9][0-9]{0,15}|[a-z0-9 ._-]+\|[a-z0-9_\/-]+)$/i.test(b.problemKey))throw new Error('Problem key буруу.');return true;}
 if(b.type==='tutorial'){if(!/^[a-z0-9-]{1,80}$/.test(b.tutorialId))throw new Error('Tutorial ID буруу.');if(b.label!==undefined)text(b.label,300);return true;}
 if(b.type==='diagram'){
  if(!['array','graph','tree','dp'].includes(b.kind))throw new Error('Diagram төрөл буруу.');if(b.caption!==undefined&&String(b.caption).length>2000)throw new Error('Diagram тайлбар хэт урт.');
  if(['array','dp'].includes(b.kind)){if(!Array.isArray(b.rows)||!b.rows.length||b.rows.length>20)throw new Error('Diagram 1–20 мөртэй байна.');for(const row of b.rows){if(!Array.isArray(row)||!row.length||row.length>30)throw new Error('Diagram мөр 1–30 нүдтэй байна.');for(const value of row)text(value,500);}}
  else {if(!Array.isArray(b.nodes)||!b.nodes.length||b.nodes.length>30||!Array.isArray(b.edges)||b.edges.length>100)throw new Error('Graph 1–30 орой, 0–100 ирмэгтэй байна.');const ids=new Set();for(const n of b.nodes){text(n.id,50);text(n.label,500);if(ids.has(n.id))throw new Error('Diagram оройн ID давхардсан.');ids.add(n.id);if(n.x!==undefined&&(!Number.isFinite(n.x)||n.x<5||n.x>95))throw new Error('Оройн x нь 5–95 байна.');if(n.y!==undefined&&(!Number.isFinite(n.y)||n.y<5||n.y>95))throw new Error('Оройн y нь 5–95 байна.');}for(const edge of b.edges)if(!Array.isArray(edge)||edge.length!==2||edge.some(id=>!ids.has(id)))throw new Error('Diagram ирмэгийн ID байхгүй.');validateGraphStyle(b);}
  if(b.highlights!==undefined&&(!Array.isArray(b.highlights)||b.highlights.length>100||b.highlights.some(v=>typeof v!=='string'||!v.trim()||v.length>50)))throw new Error('Diagram highlight буруу.');return true;
 }
 return false;
}
export function createBlock(type){
 const key=crypto.randomUUID();const common={key,type};
 if(type==='rich')return {...common,content:[{text:'',marks:[]}]};
 if(type==='heading')return {...common,level:3,text:'Шинэ гарчиг'};
 if(type==='math')return {...common,tex:'a_{i+1}=a_i+1'};
 if(type==='code')return {...common,language:'C++17',text:'// C++17\n'};
 if(['list','ordered'].includes(type))return {...common,items:['Шинэ мөр']};
 if(type==='checklist')return {...common,items:[{text:'Ойлгосноо тайлбарлаж чадна.',checked:false}]};
 if(type==='table')return {...common,headers:['Алхам','Төлөв'],rows:[['$1$','Анхны төлөв']]};
 if(type==='links')return {...common,items:[{label:'Эх сурвалж',url:'https://cses.fi/problemset/'}]};
 if(type==='callout')return {...common,tone:'observation',title:'Гол ажиглалт',text:'Өөрчлөгдөхгүй үлдэх шинжийг ажиглаарай.'};
 if(type==='quote')return {...common,text:'Тайлбар эсвэл эшлэл.'};
 if(type==='image')return {...common,path:'',alt:'',caption:'',align:'center',width:100};
 if(type==='diagram')return {...common,kind:'array',rows:[['$2$','$4$','$7$']],highlights:['0:1'],caption:'Array-ийн төлөв'};
 if(type==='problem')return {...common,problemKey:''};
 if(type==='tutorial')return {...common,tutorialId:'binary-search',label:'Binary search'};
 if(type==='divider')return common;
 return {...common,text:'Шинэ тайлбар'};
}
