import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {validateTutorial} from '../tutorial-model.js';
import {affectedIds, formatMath} from '../tools/joi_input_format.mjs';
const changes = JSON.parse(fs.readFileSync('audit/joi-input-format/proposals.json'));
const originals = JSON.parse(fs.readFileSync('audit/joi-statements/statement-plans.json'));
test('Only six bilingual input templates become native math; exact sample data and all other content remain', () => {
    assert.deepEqual(changes.map(c => c.id), affectedIds);
    for (const c of changes) {
        const original = originals.find(p => p.id === c.id).statement;
        validateTutorial(c.statement);
        const restored = structuredClone(c.statement);
        assert.equal(c.blocks.length, 2);
        for (const b of c.blocks) {
            const doc = b.lang === 'mn' ? restored : restored.translations.en;
            assert.deepEqual(doc.sections[b.sectionIndex].blocks[b.blockIndex], b.after);
            assert.deepEqual(b.after, {type: 'math', tex: formatMath(b.before.text)});
            assert.equal(b.after.tex.slice('\\begin{array}{l}'.length, -'\\end{array}'.length).split('\\\\\n').map(s => s.split('\\quad ').join(' ')).join('\n') + '\n', b.before.text);
            doc.sections[b.sectionIndex].blocks[b.blockIndex] = b.before;
        }
        assert.deepEqual(restored, original);
        assert.deepEqual(c.statement.sections[4], original.sections[4]);
        assert.deepEqual(c.statement.translations.en.sections[4], original.translations.en.sections[4]);
    }
});
