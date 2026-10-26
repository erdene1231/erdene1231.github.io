// Private Storage upload and short-lived signed delivery; never cache account URLs.
import {validMediaPath} from './tutorial-blocks.js?v=33';
let generation=0;
export const clearMediaCache=()=>{generation++;};
export async function tutorialImageUrl(client,path,viewer='public',preview=false){
 if(!client?.storage||!validMediaPath(path))throw new Error('Зургийн онлайн холболт шаардлагатай.');
 const turn=generation;
 const {data,error}=await client.storage.from('tutorial-media').createSignedUrl(path,preview?60:600);
 if(turn!==generation)throw new Error('Account changed.');
 if(error)throw error;
 const url=new URL(data?.signedUrl);
 if(url.protocol!=='https:'||url.username||url.password)throw new Error('Unsafe image delivery URL.');
 return url.href;
}

export async function imageSignature(file){
 if(!file||!['image/png','image/jpeg','image/webp'].includes(file.type)||file.size<12||file.size>5*1024*1024)throw new Error('PNG, JPG/JPEG, WebP · 5 MB хүртэл зураг сонгоно уу. SVG болон HTML дэмжихгүй.');
 const a=new Uint8Array(await file.slice(0,12).arrayBuffer()),png=[137,80,78,71,13,10,26,10].every((x,i)=>a[i]===x),jpg=a[0]===255&&a[1]===216&&a[2]===255,webp=String.fromCharCode(...a.slice(0,4))==='RIFF'&&String.fromCharCode(...a.slice(8,12))==='WEBP';
 if(!(file.type==='image/png'&&png||file.type==='image/jpeg'&&jpg||file.type==='image/webp'&&webp))throw new Error('Зургийн MIME төрөл болон файлын агуулга тохирохгүй байна.');return true;
}
export async function prepareTutorialImage(file){
 await imageSignature(file);const bitmap=await createImageBitmap(file);
 try{if(!bitmap.width||!bitmap.height||bitmap.width*bitmap.height>40000000)throw new Error('Зураг 40 megapixel-ээс бага байна.');const ratio=Math.min(1,2400/Math.max(bitmap.width,bitmap.height)),canvas=document.createElement('canvas');canvas.width=Math.max(1,Math.round(bitmap.width*ratio));canvas.height=Math.max(1,Math.round(bitmap.height*ratio));canvas.getContext('2d').drawImage(bitmap,0,0,canvas.width,canvas.height);const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/webp',.9));if(!blob||blob.type!=='image/webp'||blob.size>5*1024*1024)throw new Error('Зургийг боловсруулах боломжгүй эсвэл хэмжээ хэт том байна.');return {blob,width:canvas.width,height:canvas.height};}finally{bitmap.close();}
}
export async function uploadTutorialImage(client,tutorialId,file,actorId,isCurrent=()=>true){
 if(!client?.storage||!/^[a-z0-9-]{1,80}$/.test(tutorialId)||!/^[0-9a-f-]{36}$/.test(actorId||''))throw new Error('Эхлээд хичээлийн ID-гаа тохируулж нэвтэрнэ үү.');
 const turn=generation,active=()=>turn===generation&&isCurrent();
 if(!active())throw new Error('Upload context changed.');
 const prepared=await prepareTutorialImage(file);
 if(!active())throw new Error('Upload context changed.');
 const path=tutorialId+'/'+actorId+'/'+crypto.randomUUID()+'.webp',result=await client.storage.from('tutorial-media').upload(path,prepared.blob,{contentType:'image/webp',cacheControl:'3600',upsert:false});if(!active())throw new Error('Upload context changed.');if(result.error)throw result.error;return {path,pixelWidth:prepared.width,pixelHeight:prepared.height};
}
