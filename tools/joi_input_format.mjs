// Local-only presentation proposals. No network, SQL or production mutation.
import {bodyHash} from './part04_tutorial_proposals.mjs';
export const affectedIds = ['task-721', 'task-723', 'task-896', 'task-897', 'task-898', 'task-899'];
export const hash = bodyHash;
export function formatMath(text) {
    const lines = text.replace(/\n$/, '').split('\n');
    return '\\begin{array}{l}' + lines.map(line => line.split(' ').join('\\quad ')).join('\\\\\n') + '\\end{array}';
}
export function prepareInputFormats(rows) {
    if (rows.length !== 24 || new Set(rows.map(r => r.problem_id)).size !== 24) throw Error('Expected all24 current JOI rows');
    const changes = [];
    for (const row of rows) {
        const before = row.body.statement, after = structuredClone(before), blocks = [];
        for (const [lang, doc] of [['mn', after], ['en', after.translations.en]]) {
            for (const [sectionIndex, section] of doc.sections.entries()) {
                if (!['Оролт', 'Гаралт', 'Input', 'Output'].includes(section.title)) continue;
                section.blocks = section.blocks.map((block, blockIndex) => {
                    if (block.type !== 'code' || !['Input', 'Output'].includes(block.language)) return block;
                    if (!affectedIds.includes(row.problem_id) || sectionIndex !== 1 || block.language !== 'Input') throw Error('Unreviewed format target');
                    const replacement = {type: 'math', tex: formatMath(block.text)};
                    blocks.push({lang, sectionIndex, blockIndex, before: block, after: replacement});
                    return replacement;
                });
            }
        }
        if (blocks.length) changes.push({id: row.problem_id, number: row.number, expected_revision: row.revision, expected_body_sha256: hash(row.body), before_statement_sha256: hash(before), statement: after, blocks});
    }
    if (JSON.stringify(changes.map(c => c.id)) !== JSON.stringify(affectedIds) || changes.some(c => c.blocks.length !== 2)) throw Error('Exact6 bilingual formats expected');
    return changes;
}
