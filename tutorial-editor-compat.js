// Reading may fall back to MN; editing must never redirect an EN write into MN.
export function editableVersion(body,lang){
 if(lang==='mn')return body;
 if(lang==='en'&&body.translations?.en)return body.translations.en;
 throw new Error('Англи хувилбар одоогоор байхгүй. Монгол хувилбарыг сонгоно уу.');
}
export const isLegacyEditableBlock=block=>!!block&&['p','note','code','math','list','ordered','table','links'].includes(block.type);
