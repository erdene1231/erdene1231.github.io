import fs from 'node:fs';
import crypto from 'node:crypto';
import {validatePriority} from '../priority.js';
import {validateRelations} from '../learning-model.js';

const stable = value => Array.isArray(value)
    ? '[' + value.map(stable).join(',') + ']'
    : value && typeof value === 'object'
        ? '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + stable(value[key])).join(',') + '}'
        : JSON.stringify(value);
export const bodyHash = value => crypto.createHash('sha256').update(stable(value)).digest('hex');

// Frozen public metadata and actual import receipts, not a replacement for a fresh live guard.
export function proposalProblems() {
    const baseline = JSON.parse(fs.readFileSync('audit/PART04-BASELINE.json')).problems.map(row => row.body);
    const receipts = JSON.parse(fs.readFileSync('audit/PART04-PRODUCTION-IMPORT-RECEIPTS.json')).actual_server_receipts;
    const additions = [1, 2, 3].flatMap(batch => JSON.parse(fs.readFileSync('audit/PART04-IMPORT-METADATA-0' + batch + '.json')));
    return baseline.concat(additions.map(body => {
        const receipt = receipts.find(row => row.source === body.source && row.ref === body.ref);
        if (!receipt) throw Error('Missing actual problem receipt: ' + body.ref);
        return {...body, id: receipt.id, number: receipt.number};
    }));
}

export function proposedTutorialRows(rows) {
    const out = structuredClone(rows);
    const paths = [
        'audit/PACKAGE02-TUTORIAL-PROPOSALS.json',
        'audit/PACKAGE02-SEMANTIC-PATCH01.json',
        'audit/PACKAGE02-PRIORITY-PATCH01.json',
        'audit/PACKAGE02-FOUNDATION-LESSONS-PATCH01.json'
    ];
    for (const path of paths) {
        if (!fs.existsSync(path)) continue;
        const proposal = JSON.parse(fs.readFileSync(path));
        if (proposal.applied !== false) throw Error('Proposal state is not local-only');
        for (const patch of proposal.patches) {
            if (patch.id === 'mongolia') throw Error('Preserve Mongolia test lesson unchanged');
            const row = out.find(item => item.body.id === patch.id);
            if (!row || row.revision !== patch.expected_revision || bodyHash(row.body) !== patch.expected_body_sha256) {
                throw Error('Stale tutorial proposal: ' + patch.id);
            }
            for (const operation of patch.operations) {
                const doc = operation.language === 'mn' ? row.body : row.body.translations.en;
                if (operation.append_sections) {
                    if (doc.sections.length !== operation.expected_length) throw Error('Sections changed: ' + patch.id);
                    doc.sections.push(...structuredClone(operation.append_sections));
                    continue;
                }
                const blocks = doc.sections[operation.section].blocks;
                if (operation.append_blocks) {
                    if (blocks.length !== operation.expected_length) throw Error('Section changed: ' + patch.id);
                    blocks.push(...structuredClone(operation.append_blocks));
                } else {
                    if (stable(blocks[operation.block]) !== stable(operation.expected)) throw Error('Block changed: ' + patch.id);
                    blocks[operation.block] = structuredClone(operation.value);
                }
            }
            if (patch.field_updates) {
                if (Object.keys(patch.field_updates).some(key => !['priorityLevel', 'priorityReason'].includes(key))) {
                    throw Error('Only reviewed tutorial priority fields allowed');
                }
                validatePriority(patch.field_updates);
                Object.assign(row.body, structuredClone(patch.field_updates));
            }
            if (patch.relationships_update) {
                if (stable(row.body.learningRelations ?? null) !== stable(patch.relationships_update.expected)) {
                    throw Error('Relationships changed: ' + patch.id);
                }
                row.body.learningRelations = validateRelations(
                    patch.relationships_update.value, patch.id, out.map(item => item.body), proposalProblems()
                );
            }
        }
    }
    return out;
}
