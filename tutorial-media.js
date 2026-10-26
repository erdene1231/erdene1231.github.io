// Reader-only signed delivery. Upload/policies remain gated on migration 025.
import {validMediaPath} from './tutorial-blocks.js?v=27';
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
