import fs from'node:fs';import crypto from'node:crypto';
const stable=value=>Array.isArray(value)?'['+value.map(stable).join(',')+']':value&&typeof value==='object'?'{'+Object.keys(value).sort().map(k=>JSON.stringify(k)+':'+stable(value[k])).join(',')+'}':JSON.stringify(value);
export const bodyHash=value=>crypto.createHash('sha256').update(stable(value)).digest('hex');
export function proposedTutorialRows(rows){
 const path='audit/PACKAGE02-TUTORIAL-PROPOSALS.json';if(!fs.existsSync(path))return structuredClone(rows);
 const proposal=JSON.parse(fs.readFileSync(path));if(proposal.applied!==false)throw Error('Proposal state is not local-only');const out=structuredClone(rows);
 for(const patch of proposal.patches){const row=out.find(r=>r.body.id===patch.id);if(!row||row.revision!==patch.expected_revision||bodyHash(row.body)!==patch.expected_body_sha256)throw Error('Stale tutorial proposal: '+patch.id);
  for(const op of patch.operations){const d=op.language==='mn'?row.body:row.body.translations.en,blocks=d.sections[op.section].blocks;
   if(op.append_blocks){if(blocks.length!==op.expected_length)throw Error('Section changed: '+patch.id);blocks.push(...structuredClone(op.append_blocks));}
   else{if(stable(blocks[op.block])!==stable(op.expected))throw Error('Block changed: '+patch.id);blocks[op.block]=structuredClone(op.value);}
  }
 }
 return out;
}
