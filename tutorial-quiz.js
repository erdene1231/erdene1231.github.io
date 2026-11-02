// Practice only: client-delivered answers are inspectable, not secure exam grading.
const idPattern = /^[a-zA-Z0-9_-]{1,80}$/;
export function validateQuiz(b) {
    const text = (s, max) => typeof s === 'string' && !!s.trim() && s.length <= max;
    if (typeof b.quizId !== 'string' || !idPattern.test(b.quizId) || !text(b.question, 4000) || !text(b.explanation, 8000)) throw Error('Quiz ID, асуулт, тайлбараа шалгана уу.');
    if (!Array.isArray(b.options) || b.options.length < 2 || b.options.length > 6) throw Error('Quiz 2–6 сонголттой байна.');
    const ids = new Set();
    for (const o of b.options) {
        if (!o || typeof o.id !== 'string' || !idPattern.test(o.id) || ids.has(o.id) || !text(o.text, 2000)) throw Error('Сонголтын ID/текст буруу эсвэл давхардсан.');
        ids.add(o.id);
    }
    if (!ids.has(b.answerId)) throw Error('Нэг зөв хариулт сонгоно уу.');
    return true;
}
export function createQuiz(key) {
    return {key, type: 'quiz', quizId: 'q-' + key, question: 'Аль хариулт зөв бэ?', options: [{id: 'a', text: 'Эхний сонголт'}, {id: 'b', text: 'Хоёр дахь сонголт'}], answerId: 'a', explanation: 'Яагаад зөв болохыг тайлбарлана.'};
}
export function renderQuiz(b, parent, lang, typeset) {
    validateQuiz(b);
    const en = lang === 'en';
    const node = (tag, text, cls) => { const e = document.createElement(tag); if (text !== undefined) e.textContent = text; if (cls) e.className = cls; return e; };
    const box = node('fieldset', undefined, 'tutorial-quiz'), legend = node('legend', b.question), choices = node('div'), feedback = node('div', undefined, 'quiz-feedback');
    const status = node('p'); status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    const check = node('button', en ? 'Check answer' : 'Хариулт шалгах'), retry = node('button', en ? 'Try again' : 'Дахин оролдох');
    check.type = retry.type = 'button'; check.disabled = true; retry.hidden = feedback.hidden = true;
    const name = 'quiz-' + crypto.randomUUID(); let selected = null;
    const radios = b.options.map(o => {
        const label = node('label'), radio = node('input'); radio.type = 'radio'; radio.name = name; radio.value = o.id;
        radio.onchange = () => { selected = o.id; check.disabled = false; };
        label.append(radio, node('span', o.text)); choices.append(label); return radio;
    });
    check.onclick = () => {
        if (!selected || check.disabled) return;
        const correct = selected === b.answerId;
        status.textContent = correct ? (en ? 'Correct.' : 'Зөв хариуллаа.') : (en ? 'Not quite. Review the explanation.' : 'Хариулт зөрлөө. Тайлбарыг уншаад дахин оролдоорой.');
        box.dataset.result = correct ? 'correct' : 'incorrect';
        feedback.replaceChildren(node('p', b.explanation)); feedback.hidden = false; retry.hidden = false; check.disabled = true;
        radios.forEach(r => r.disabled = true);
        void typeset?.([feedback], undefined, () => feedback.isConnected).catch(() => {});
    };
    retry.onclick = () => { selected = null; radios.forEach(r => { r.checked = false; r.disabled = false; }); feedback.hidden = retry.hidden = true; feedback.replaceChildren(); status.textContent = ''; delete box.dataset.result; check.disabled = true; radios[0].focus(); };
    box.append(legend, choices, check, retry, status, feedback); parent.append(box);
}
