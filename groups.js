import {createReportLatex, createReportPdf} from './group-document.js?v=18';
import {rpc} from './accounts.js?v=17';
import {createReportWorkbook, todayInMongolia, validDate, weekday, shiftDate, dateRange, filterWeekdays} from './group-export.js?v=18';

const MARKUP = `
<div class="section-head"><div><p class="eyebrow">ХАМТДАА СУРЪЯ</p><h2>Групп ба өдрийн тэмдэглэл</h2></div><button id="group-create" class="primary" type="button" hidden>+ Групп үүсгэх</button></div>
<p id="group-message" class="muted" role="status" aria-live="polite"></p>
<button id="group-login" type="button" hidden>Account-аар нэвтрэх</button>
<div id="group-list-view" hidden><div class="group-toolbar"><label>Харуулах<select id="group-filter"><option value="all">Хандах боломжтой бүх групп</option><option value="mine">Миний группүүд</option></select></label><button id="group-reload" type="button">Шинэчлэх</button></div><div id="group-list" class="group-grid"></div></div>
<div id="group-detail-view" hidden>
 <a href="#groups">← Группүүд</a>
 <div class="section-head"><div><span id="group-privacy" class="badge"></span><h3 id="group-title"></h3></div><div class="group-actions"><button id="group-members-open" type="button">Гишүүд</button><button id="group-settings" type="button" hidden>Групп засах</button><button id="group-export-open" type="button">Тайлан export</button></div></div>
 <p id="group-description" class="group-text"></p><p id="group-access-note" class="muted"></p>
 <div class="group-day-bar"><button id="group-prev-day" type="button" aria-label="Өмнөх өдөр">←</button><label>Тэмдэглэлийн огноо<input id="group-day" type="date" required></label><button id="group-next-day" type="button" aria-label="Дараах өдөр">→</button><span id="group-weekday"></span><button id="group-today" type="button">Өнөөдөр</button><button id="group-own-report" class="primary" type="button" hidden>Миний тэмдэглэл</button></div>
 <div class="group-toolbar"><p id="group-day-summary" class="muted" role="status" aria-live="polite"></p><label>Сурагчийн тэмдэглэл<select id="group-report-filter"><option value="all">Бүгд</option><option value="filled">Бөглөсөн</option><option value="missing">Бөглөөгүй</option></select></label></div>
 <div id="group-reports" class="group-reports"></div>
</div>
<dialog id="group-editor" aria-labelledby="group-editor-title"><div class="dialog-head"><h2 id="group-editor-title">Групп үүсгэх</h2><button data-group-close="group-editor" type="button" aria-label="Хаах">✕</button></div><form id="group-editor-form"><label>Группын нэр<input id="group-name" maxlength="100" required></label><label>Тайлбар<textarea id="group-description-input" maxlength="2000" rows="3"></textarea></label><label>Харагдах хүрээ<select id="group-visibility"><option value="private">Private — гишүүд болон сайтын админ</option><option value="public">Public — нэвтэрсэн хүн бүр уншина</option></select></label><p class="muted">Гишүүд бусдыг username-аар нэмж чадна. Public сонговол тэмдэглэлүүд нэвтэрсэн бүх хэрэглэгчид харагдана.</p><button id="group-editor-save" class="primary" type="submit">Хадгалах</button><p id="group-editor-message" role="status" aria-live="polite"></p></form></dialog>
<dialog id="group-members-dialog" aria-labelledby="group-members-title"><div class="dialog-head"><h2 id="group-members-title">Группын гишүүд</h2><button data-group-close="group-members-dialog" type="button" aria-label="Хаах">✕</button></div><form id="group-add-form"><label>Нэмэх хэрэглэгчийн username<input id="group-add-username" minlength="3" maxlength="24" pattern="[a-zA-Z0-9_]{3,24}" placeholder="username" required></label><button id="group-add-submit" class="primary" type="submit">Гишүүн нэмэх</button></form><p id="group-members-message" class="muted" role="status" aria-live="polite"></p><ul id="group-members-list" class="group-member-list"></ul></dialog>
<dialog id="group-report-editor" aria-labelledby="group-report-title"><div class="dialog-head"><h2 id="group-report-title">Өдрийн тэмдэглэл</h2><button data-group-close="group-report-editor" type="button" aria-label="Хаах">✕</button></div><p id="group-report-person"></p><p id="group-report-date" class="muted"></p><p class="muted">Бүх талбар сонголттой. Бодлогын нэр, ID эсвэл холбоосыг мөр бүрт нэгээр бичээрэй. Энэ тэмдэглэл бодлогын сан дахь progress-ийг автоматаар өөрчлөхгүй.</p><form id="group-report-form"><label>Бодсон бодлогууд<textarea id="group-report-problems" maxlength="12000" rows="5" placeholder="CSES — Counting Rooms\nCF 1661B — Getting Zero"></textarea></label><div class="group-count-field"><label>Нийт бодлогын тоо<input id="group-report-count" type="number" min="0" max="100000" step="1" placeholder="Бөглөөгүй"></label><button id="group-count-lines" type="button">Жагсаалтын мөрөөр тоолох</button></div><label>Хэр хэцүү бодлогууд бодсон бэ?<textarea id="group-report-difficulty" maxlength="1200" rows="2" placeholder="Жишээ: CF 1400–1700; хоёр нь бие даан, нэг нь hint-тэй"></textarea></label><label>Судалсан сэдвүүд<textarea id="group-report-topics" maxlength="2000" rows="2" placeholder="BFS, grid, path сэргээх"></textarea></label><label>Нэмэлт тэмдэглэл<textarea id="group-report-notes" maxlength="8000" rows="3" placeholder="Хаана гацсан, юу ойлгосон, дараа юу үргэлжлүүлэх вэ?"></textarea></label><button id="group-report-save" class="primary" type="submit">Тэмдэглэл хадгалах</button><p id="group-report-message" role="status" aria-live="polite"></p></form></dialog>
<dialog id="group-teacher-editor" aria-labelledby="group-teacher-title"><div class="dialog-head"><h2 id="group-teacher-title">Багшийн тэмдэглэл</h2><button data-group-close="group-teacher-editor" type="button" aria-label="Хаах">✕</button></div><p id="group-teacher-person"></p><p id="group-teacher-date" class="muted"></p><p class="muted">Группын болон сайтын админ засна. Группийг харах эрхтэй хүмүүс уншина. Сурагчийн өөрийн тэмдэглэл тусдаа хадгалагдана.</p><form id="group-teacher-form"><label>Багшийн тэмдэглэл<textarea id="group-teacher-note" maxlength="8000" rows="7" placeholder="Сурагчийн ахиц, зөвлөгөө, дараагийн ажил…"></textarea></label><button id="group-teacher-save" class="primary" type="submit">Багшийн тэмдэглэл хадгалах</button><p id="group-teacher-message" role="status" aria-live="polite"></p></form></dialog>
<dialog id="group-export-dialog" aria-labelledby="group-export-title"><div class="dialog-head"><h2 id="group-export-title">Тайлан export хийх</h2><button data-group-close="group-export-dialog" type="button" aria-label="Хаах">✕</button></div><p>Excel-д өдөр бүр тусдаа sheet, A4 LaTeX/PDF-д өдөр бүр шинэ хуудаснаас эхэлнэ. Бүх гишүүн, тэмдэглэл бөглөөгүй сурагчид мөн орно. Өмнөх гишүүний тухайн өдрийн хадгалсан тэмдэглэл ч орно.</p><div class="group-export-range"><label>Эхлэх өдөр<input id="group-export-start" type="date"></label><label>Дуусах өдөр<input id="group-export-end" type="date"></label><button id="group-export-range-add" type="button">Эдгээр өдрийг нэмэх</button></div><div class="group-toolbar"><label>Тусдаа өдөр нэмэх<input id="group-export-date" type="date"></label><button id="group-export-date-add" type="button">Өдөр нэмэх</button><button id="group-export-clear" type="button">Сонголт цэвэрлэх</button></div><fieldset class="group-export-weekdays"><legend>Export хийх гаргууд</legend><label><input type="checkbox" data-export-weekday value="1" checked>Даваа</label><label><input type="checkbox" data-export-weekday value="2" checked>Мягмар</label><label><input type="checkbox" data-export-weekday value="3" checked>Лхагва</label><label><input type="checkbox" data-export-weekday value="4" checked>Пүрэв</label><label><input type="checkbox" data-export-weekday value="5" checked>Баасан</label><label><input type="checkbox" data-export-weekday value="6" checked>Бямба</label><label><input type="checkbox" data-export-weekday value="0" checked>Ням</label></fieldset><label>Файлын төрөл<select id="group-export-format"><option value="xlsx">Excel (.xlsx)</option><option value="latex">A4 LaTeX (.tex)</option><option value="pdf">A4 PDF (.pdf)</option></select></label><div id="group-export-dates" class="group-date-chips"></div><p id="group-export-count" class="muted"></p><p class="muted">Нэг export-д гаргийн шүүлтүүрт таарсан 1–62 өдөр. Овог, нэр, бодлогууд, тоо, хүндрэл, сэдэв, сурагчийн болон багшийн тэмдэглэл багтана. Овог, нэрээ Account хэсэгт тусад нь бөглөнө. Хуучин нэрийг тааж салгахгүй; тусдаа баганад хадгална.</p><button id="group-export-download" class="primary" type="button">Excel (.xlsx) татах</button><p id="group-export-message" role="status" aria-live="polite"></p></dialog>`;

function node(tag, className = '', text) {
    const element = document.createElement(tag);
    element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
}
const personName = person => [person.last_name, person.first_name].filter(Boolean).join(' ') || person.full_name || person.username || 'Нэрээ тохируулаагүй';
function errorText(error) {
    if (['42P01', 'PGRST202', 'PGRST205', '42703'].includes(error?.code)) return 'Группын шинэчлэл идэвхжээгүй байна. Сайтын админд мэдэгдээрэй.';
    return error?.message || 'Холболт амжилтгүй. Дахин оролдоорой.';
}
export function setupGroups(ctx) {
    const root = document.getElementById('groups');
    root.innerHTML = MARKUP; // Static template only. User content always uses textContent.
    const $ = id => root.querySelector('#' + id);
    let accountId, version = 0, detailToken = 0, dayToken = 0, listToken = 0;
    let currentId = null, detail = null, rows = [], groups = [], editing = null, teacherEditing = null, editingGroup = false;
    let mutating = false, exporting = false, loadedDay = null, downloadUrl = null;
    const selectedDates = new Set();
    const downloadLink = node('a', 'primary', 'Бэлэн файлыг татах');
    downloadLink.hidden = true; downloadLink.style.marginTop = '12px';
    $('group-export-message').after(downloadLink);
    function clearDownload() {
        if (downloadUrl) URL.revokeObjectURL(downloadUrl);
        downloadUrl = null; downloadLink.hidden = true; downloadLink.removeAttribute('href');
    }
    $('group-day').value = todayInMongolia();
    const current = token => token === version;
    const online = () => Boolean(ctx.client() && ctx.user());
    const activeGroup = () => /^#groups\/[0-9a-f-]{36}$/i.test(location.hash) ? location.hash.slice(8) : null;
    function closeDialogs() {root.querySelectorAll('dialog[open]').forEach(dialog => dialog.close());}
    function renderList() {
        $('group-list').replaceChildren();
        const visible = groups.filter(group => $('group-filter').value !== 'mine' || group.my_role);
        for (const group of visible) {
            const card = node('a', 'group-card'); card.href = '#groups/' + group.id;
            card.append(node('span', 'muted', group.visibility === 'private' ? 'PRIVATE' : 'PUBLIC'), node('h3', '', group.name),
                node('p', 'muted', `${group.member_count} гишүүн${group.my_role === 'admin' ? ' · Админ' : group.my_role ? ' · Гишүүн' : ''}`));
            if (group.description) card.append(node('p', 'group-text', group.description));
            $('group-list').append(card);
        }
        if (!visible.length) $('group-list').append(node('p', 'muted', 'Одоогоор групп байхгүй. Шинэ групп үүсгэх эсвэл багшаараа username-аараа нэмүүлээрэй.'));
    }
    async function loadList() {
        if (!online()) return;
        const token = version, request = ++listToken;
        try {
            const result = await rpc(ctx.client(), 'study_list_groups');
            if (!current(token) || request !== listToken) return;
            groups = result.groups || []; renderList();
            if (!currentId) $('group-message').textContent = 'Өдрийн ажлаа тэмдэглэж, хамтдаа ахиц гаргая.';
        } catch (error) {if (current(token) && request === listToken) $('group-message').textContent = errorText(error);}
    }
    function renderMembers() {
        $('group-members-list').replaceChildren();
        $('group-add-form').hidden = !detail.is_member && !detail.can_manage;
        for (const member of detail.members) {
            const item = node('li'), info = node('div');
            info.append(node('strong', '', personName(member)), node('p', 'muted', `${member.username ? '@' + member.username : 'Username тохируулаагүй'} · ${member.role === 'admin' ? 'Админ' : 'Гишүүн'}`));
            item.append(info);
            if (detail.can_manage) {
                const controls = node('div', 'group-actions');
                for (const [role, label] of [[member.role === 'admin' ? 'member' : 'admin', member.role === 'admin' ? 'Гишүүн болгох' : 'Админ болгох'], ['remove', 'Хасах']]) {
                    const button = node('button', role === 'remove' ? 'danger' : '', label); button.type = 'button';
                    button.onclick = () => void memberRole(member, role); controls.append(button);
                }
                item.append(controls);
            }
            $('group-members-list').append(item);
        }
    }
    async function openGroup(id, keepDialogs = false) {
        if (!online()) return;
        const token = version, request = ++detailToken;
        currentId = id; detail = null; rows = []; loadedDay = null; dayToken++;
        $('group-list-view').hidden = true; $('group-detail-view').hidden = true; $('group-reports').replaceChildren();
        $('group-message').textContent = 'Групп ачаалж байна…';
        if (!keepDialogs) closeDialogs();
        try {
            const result = await rpc(ctx.client(), 'study_group_detail', {p_group_id: id});
            if (!current(token) || request !== detailToken || currentId !== id) return;
            detail = result;
            $('group-title').textContent = detail.group.name;
            $('group-description').textContent = detail.group.description;
            $('group-privacy').textContent = detail.group.visibility === 'private' ? 'Private group' : 'Public group';
            $('group-access-note').textContent = detail.group.visibility === 'private' ? 'Тэмдэглэлүүд зөвхөн группын гишүүд болон сайтын админд харагдана.' : 'Энэ группын тэмдэглэлийг нэвтэрсэн хүн бүр уншиж болно.';
            $('group-settings').hidden = !detail.can_manage;
            $('group-own-report').hidden = !detail.is_member; $('group-own-report').disabled = true;
            $('group-detail-view').hidden = false; $('group-message').textContent = '';
            renderMembers(); await loadDay();
        } catch (error) {
            if (current(token) && request === detailToken) {$('group-message').textContent = errorText(error); closeDialogs();}
        }
    }
    function renderReports() {
        if (!loadedDay) return;
        $('group-reports').replaceChildren();
        const filled = rows.filter(row => row.has_report).length;
        const withCount = rows.filter(row => Number.isInteger(row.problem_count));
        const total = withCount.reduce((sum, row) => sum + row.problem_count, 0);
        $('group-day-summary').textContent = `${filled}/${rows.length} тэмдэглэл · ${total} бодлого (${withCount.length} гишүүн тоо бөглөсөн)`;
        const filter = $('group-report-filter').value;
        const visible = rows.filter(row => filter === 'all' || (filter === 'filled' ? row.has_report : !row.has_report));
        for (const row of visible) {
            const card = node('article', 'group-report-card'), head = node('div', 'group-report-head'), info = node('div');
            info.append(node('h4', '', personName(row)), node('span', 'muted', (row.username ? '@' + row.username : 'Username тохируулаагүй') + (!row.is_member ? ' · Өмнөх гишүүн' : '')));
            head.append(info, node('span', 'badge', row.has_report ? 'Бөглөсөн' : 'Бөглөөгүй'));
            if (row.can_edit) {const button = node('button', '', row.has_report ? 'Засах' : 'Бөглөх'); button.type = 'button'; button.onclick = () => editReport(row); head.append(button);}
            card.append(head);
            if (row.has_report) {
                const fields = [['Бодсон бодлогууд', row.solved_problems], ['Нийт бодлогын тоо', row.problem_count], ['Бодлогын хүндрэл', row.difficulty], ['Судалсан сэдвүүд', row.topics], ['Нэмэлт тэмдэглэл', row.notes]];
                for (const [label, value] of fields) {
                    if (value === null || value === undefined || value === '') continue;
                    const block = node('div', 'group-report-field'); block.append(node('strong', '', label), node('p', 'group-text', String(value))); card.append(block);
                }
                if (fields.every(([, value]) => value === '' || value === null)) card.append(node('p', 'muted', 'Энэ өдрийн тэмдэглэл үүсгэсэн; талбаруудыг хараахан бөглөөгүй.'));
                if (row.updated_at) card.append(node('p', 'muted', 'Шинэчилсэн: ' + new Intl.DateTimeFormat('mn-MN', {timeZone: 'Asia/Ulaanbaatar', dateStyle: 'short', timeStyle: 'short'}).format(new Date(row.updated_at))));
            }
            const teacherBlock = node('div', 'group-teacher-block');
            const teacherHead = node('div', 'group-report-head');
            teacherHead.append(node('strong', '', 'Багшийн тэмдэглэл'));
            if (row.can_edit_teacher) {
                const button = node('button', '', row.teacher_note ? 'Багшийн тэмдэглэл засах' : 'Багшийн тэмдэглэл нэмэх');
                button.type = 'button'; button.onclick = () => editTeacher(row); teacherHead.append(button);
            }
            teacherBlock.append(teacherHead, node('p', 'group-text', row.teacher_note || 'Багшийн тэмдэглэл оруулаагүй.'));
            card.append(teacherBlock);
            $('group-reports').append(card);
        }
        if (!visible.length) $('group-reports').append(node('p', 'muted', 'Энэ шүүлтүүрт тохирох тэмдэглэл байхгүй.'));
    }
    async function loadDay() {
        if (!detail || !online()) return;
        const date = $('group-day').value;
        const token = version, request = ++dayToken, id = currentId;
        loadedDay = null; rows = []; $('group-own-report').disabled = true;
        $('group-reports').replaceChildren(); $('group-weekday').textContent = '';
        if (!validDate(date)) {$('group-day-summary').textContent = 'Огноогоо бүтнээр сонгоно уу.'; return;}
        $('group-weekday').textContent = weekday(date); $('group-reports').replaceChildren(); $('group-day-summary').textContent = 'Тэмдэглэлүүд ачаалж байна…';
        try {
            const result = await rpc(ctx.client(), 'study_report_data', {p_group_id: id, p_dates: [date]});
            if (!current(token) || request !== dayToken || currentId !== id) return;
            rows = result; loadedDay = date; $('group-own-report').disabled = !detail.is_member; renderReports();
        } catch (error) {if (current(token) && request === dayToken) $('group-day-summary').textContent = errorText(error);}
    }
    function editReport(row) {
        if (mutating || !row.can_edit || loadedDay !== $('group-day').value) return;
        editing = {...row, group_id: currentId};
        $('group-report-person').textContent = personName(row) + (row.username ? ' · @' + row.username : '');
        $('group-report-date').textContent = row.report_date + ' · ' + weekday(row.report_date);
        $('group-report-problems').value = row.solved_problems;
        $('group-report-count').value = row.problem_count ?? '';
        $('group-report-difficulty').value = row.difficulty;
        $('group-report-topics').value = row.topics; $('group-report-notes').value = row.notes;
        $('group-report-message').textContent = ''; $('group-report-editor').showModal();
    }
    function editTeacher(row) {
        if (mutating || !row.can_edit_teacher || loadedDay !== $('group-day').value) return;
        teacherEditing = {...row, group_id: currentId};
        $('group-teacher-person').textContent = personName(row);
        $('group-teacher-date').textContent = row.report_date + ' · ' + weekday(row.report_date);
        $('group-teacher-note').value = row.teacher_note || '';
        $('group-teacher-message').textContent = '';
        $('group-teacher-editor').showModal();
    }
    async function memberRole(member, role) {
        if (mutating || !detail?.can_manage) return;
        if (!confirm(`${personName(member)}: ${role === 'remove' ? 'группээс хасах уу? Өмнөх тэмдэглэл хадгалагдана.' : role === 'admin' ? 'группын админ болгох уу?' : 'гишүүн болгох уу?'}`)) return;
        const token = version, id = currentId; mutating = true;
        try {
            await rpc(ctx.client(), 'study_member_role', {p_group_id: id, p_user_id: member.user_id, p_role: role});
            if (!current(token) || currentId !== id) return;
            $('group-members-message').textContent = 'Хадгалагдлаа.'; await openGroup(id, true); void loadList();
        } catch (error) {if (current(token) && currentId === id) $('group-members-message').textContent = errorText(error);}
        finally {mutating = false;}
    }
    function showGroupEditor(update) {
        if (mutating || !online() || (update && !detail?.can_manage)) return;
        editingGroup = update;
        $('group-editor-title').textContent = update ? 'Групп засах' : 'Групп үүсгэх';
        $('group-name').value = update ? detail.group.name : '';
        $('group-description-input').value = update ? detail.group.description : '';
        $('group-visibility').value = update ? detail.group.visibility : 'private';
        $('group-editor-message').textContent = ''; $('group-editor').showModal();
    }
    const effectiveDates = () => filterWeekdays([...selectedDates], [...root.querySelectorAll('[data-export-weekday]:checked')].map(input => Number(input.value)));
    function renderDates() {
        const dates = effectiveDates();
        $('group-export-dates').replaceChildren();
        for (const date of dates) {
            const button = node('button', '', `${date} · ${weekday(date)} ×`); button.type = 'button';
            button.setAttribute('aria-label', date + ' өдрийг хасах');
            button.onclick = () => {if (!exporting) {selectedDates.delete(date); clearDownload(); $('group-export-message').textContent = ''; renderDates();}};
            $('group-export-dates').append(button);
        }
        $('group-export-count').textContent = `${selectedDates.size} өдөр нэмсэн · Гаргийн шүүлтүүрээр ${dates.length} өдөр export хийнэ.` + (dates.length > 62 ? ' Нэг удаад 62 хүртэл өдөр: гаргаа шүүх эсвэл өдрүүдээ хасна уу.' : '');
        $('group-export-download').disabled = exporting || !dates.length || dates.length > 62;
        $('group-export-format').disabled = exporting;
        for (const input of root.querySelectorAll('[data-export-weekday]')) input.disabled = exporting;
        const titles = {xlsx: 'Excel (.xlsx) татах', latex: 'A4 LaTeX (.tex) татах', pdf: 'A4 PDF (.pdf) татах'};
        $('group-export-download').textContent = titles[$('group-export-format').value];
    }
    function addDates(dates) {
        if (exporting) return;
        const next = new Set([...selectedDates, ...dates]);
        if (next.size > 3660) throw new Error('Хугацаа хэт урт байна. Богино хугацаа сонгоно уу.');
        dates.forEach(date => selectedDates.add(date)); clearDownload(); renderDates(); $('group-export-message').textContent = '';
    }
    function dateAction(action) {try {action();} catch (error) {$('group-export-message').textContent = errorText(error);}}
    function route() {
        if (!location.hash.startsWith('#groups')) {closeDialogs(); return;}
        if (!online()) return;
        const id = activeGroup();
        if (id) {void openGroup(id); return;}
        currentId = null; detail = null; rows = []; loadedDay = null; detailToken++; dayToken++;
        closeDialogs(); $('group-list-view').hidden = false; $('group-detail-view').hidden = true; void loadList();
    }
    // Async mutation handlers are below; all writes go through authorized server RPCs.
    $('group-teacher-form').onsubmit = async event => {
        event.preventDefault();
        if (mutating || !teacherEditing || !$('group-teacher-form').reportValidity()) return;
        const target = teacherEditing, token = version;
        mutating = true; $('group-teacher-save').disabled = true; $('group-teacher-message').textContent = 'Хадгалж байна…';
        try {
            await rpc(ctx.client(), 'study_save_teacher_note', {p_group_id: target.group_id, p_user_id: target.user_id,
                p_date: target.report_date, p_note: $('group-teacher-note').value, p_expected_revision: target.teacher_revision ?? null});
            if (!current(token) || currentId !== target.group_id) return;
            $('group-teacher-editor').close(); await loadDay();
        } catch (error) {if (current(token)) $('group-teacher-message').textContent = errorText(error);}
        finally {mutating = false; $('group-teacher-save').disabled = false;}
    };
    $('group-report-form').onsubmit = async event => {
        event.preventDefault(); if (mutating || !editing || !$('group-report-form').reportValidity()) return;
        const target = editing, token = version; mutating = true; $('group-report-save').disabled = true;
        $('group-report-message').textContent = 'Хадгалж байна…';
        const count = $('group-report-count').value;
        try {
            await rpc(ctx.client(), 'study_save_report', {p_group_id: target.group_id, p_user_id: target.user_id, p_date: target.report_date,
                p_expected_revision: target.revision ?? null, p_fields: {solved_problems: $('group-report-problems').value,
                    problem_count: count === '' ? null : Number(count), difficulty: $('group-report-difficulty').value,
                    topics: $('group-report-topics').value, notes: $('group-report-notes').value}});
            if (!current(token) || currentId !== target.group_id) return;
            $('group-report-editor').close(); await loadDay();
        } catch (error) {if (current(token)) $('group-report-message').textContent = errorText(error);}
        finally {mutating = false; $('group-report-save').disabled = false;}
    };
    $('group-add-form').onsubmit = async event => {
        event.preventDefault(); if (mutating || !$('group-add-form').reportValidity()) return;
        const token = version, id = currentId; mutating = true; $('group-add-submit').disabled = true;
        try {
            await rpc(ctx.client(), 'study_add_member', {p_group_id: id, p_username: $('group-add-username').value.trim()});
            if (!current(token) || currentId !== id) return;
            $('group-add-username').value = ''; $('group-members-message').textContent = 'Гишүүн нэмэгдлээ.';
            await openGroup(id, true); void loadList();
        } catch (error) {if (current(token) && currentId === id) $('group-members-message').textContent = errorText(error);}
        finally {mutating = false; $('group-add-submit').disabled = false;}
    };
    $('group-editor-form').onsubmit = async event => {
        event.preventDefault(); if (mutating || !$('group-editor-form').reportValidity()) return;
        const token = version, update = editingGroup, id = currentId;
        mutating = true; $('group-editor-save').disabled = true;
        try {
            const args = {p_name: $('group-name').value.trim(), p_description: $('group-description-input').value, p_visibility: $('group-visibility').value};
            if (!args.p_name) throw new Error('Группын нэрээ бичнэ үү.');
            const result = await rpc(ctx.client(), update ? 'study_update_group' : 'study_create_group', update ? {...args, p_group_id: id} : args);
            if (!current(token)) return;
            $('group-editor').close(); void loadList();
            if (update) await openGroup(id); else location.hash = '#groups/' + result;
        } catch (error) {if (current(token)) $('group-editor-message').textContent = errorText(error);}
        finally {mutating = false; $('group-editor-save').disabled = false;}
    };
    $('group-export-download').onclick = async () => {
        const dates = effectiveDates();
        if (exporting || !dates.length || dates.length > 62 || !detail) return;
        const group = {...detail.group}, token = version, format = $('group-export-format').value;
        exporting = true; renderDates(); $('group-export-message').textContent = 'Тайлан бэлтгэж байна…';
        try {
            const result = await rpc(ctx.client(), 'study_report_data', {p_group_id: group.id, p_dates: dates});
            if (!current(token) || currentId !== group.id) return;
            const data = {group, dates, rows: result};
            let bytes, extension, mime;
            if (format === 'pdf') {bytes = await createReportPdf(data); extension = 'pdf'; mime = 'application/pdf';}
            else if (format === 'latex') {bytes = createReportLatex(data); extension = 'tex'; mime = 'application/x-tex;charset=utf-8';}
            else {bytes = createReportWorkbook(data); extension = 'xlsx'; mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';}
            if (!current(token) || currentId !== group.id) return;
            const blob = new Blob([bytes], {type: mime});
            clearDownload(); downloadUrl = URL.createObjectURL(blob);
            downloadLink.href = downloadUrl; downloadLink.download = `${group.name.replace(/[<>:"/\\|?*\u0000-\u001f]/g, '_').slice(0, 60)}_${dates[0]}_${dates.at(-1)}.${extension}`;
            downloadLink.hidden = false; downloadLink.click();
            $('group-export-message').textContent = `${dates.length} өдрийн ${format === 'xlsx' ? 'Excel' : format === 'pdf' ? 'A4 PDF' : 'A4 LaTeX'} файл бэлэн боллоо. Таталт эхлээгүй бол доорх холбоосыг дарна уу.`;
        } catch (error) {if (current(token) && currentId === group.id) $('group-export-message').textContent = errorText(error);}
        finally {exporting = false; renderDates();}
    };
    for (const button of root.querySelectorAll('[data-group-close]')) button.onclick = () => {if (!mutating && !exporting) $(button.dataset.groupClose).close();};
    for (const dialog of root.querySelectorAll('dialog')) dialog.addEventListener('cancel', event => {if (mutating || exporting) event.preventDefault();});
    $('group-login').onclick = () => ctx.openAccount();
    $('group-create').onclick = () => showGroupEditor(false); $('group-settings').onclick = () => showGroupEditor(true);
    $('group-filter').onchange = renderList; $('group-reload').onclick = () => void loadList();
    $('group-day').onchange = () => void loadDay(); $('group-report-filter').onchange = renderReports;
    $('group-today').onclick = () => {$('group-day').value = todayInMongolia(); void loadDay();};
    for (const [id, delta] of [['group-prev-day', -1], ['group-next-day', 1]]) $(id).onclick = () => {if (validDate($('group-day').value)) {$('group-day').value = shiftDate($('group-day').value, delta); void loadDay();}};
    $('group-own-report').onclick = () => {const row = rows.find(row => row.user_id === ctx.user()?.id); if (row) editReport(row);};
    $('group-count-lines').onclick = () => {$('group-report-count').value = $('group-report-problems').value.split(/\r?\n/).filter(line => line.trim()).length;};
    $('group-members-open').onclick = () => {if (detail) {$('group-members-message').textContent = ''; $('group-members-dialog').showModal();}};
    $('group-export-open').onclick = () => {
        clearDownload();
        for (const input of root.querySelectorAll('[data-export-weekday]')) input.checked = true;
        selectedDates.clear(); const date = $('group-day').value || todayInMongolia(); selectedDates.add(date);
        for (const id of ['group-export-start', 'group-export-end', 'group-export-date']) $(id).value = date;
        $('group-export-message').textContent = ''; renderDates(); $('group-export-dialog').showModal();
    };
    $('group-export-range-add').onclick = () => dateAction(() => addDates(dateRange($('group-export-start').value, $('group-export-end').value, 3660)));
    for (const input of root.querySelectorAll('[data-export-weekday]')) input.onchange = () => {clearDownload(); $('group-export-message').textContent = ''; renderDates();};
    $('group-export-format').onchange = () => {clearDownload(); $('group-export-message').textContent = ''; renderDates();};
    $('group-export-date-add').onclick = () => dateAction(() => {const date = $('group-export-date').value; if (!validDate(date)) throw new Error('Өдөр сонгоно уу.'); addDates([date]);});
    $('group-export-clear').onclick = () => {if (!exporting) {selectedDates.clear(); clearDownload(); $('group-export-message').textContent = ''; renderDates();}};
    window.addEventListener('hashchange', route);
    const api = {
        accountChanged() {
            const id = ctx.user()?.id || null;
            $('group-create').hidden = !online(); $('group-login').hidden = online();
            if (id === accountId) return;
            accountId = id; version++; detailToken++; dayToken++; listToken++;
            closeDialogs(); clearDownload(); detail = null; rows = []; groups = []; currentId = null; editing = null; teacherEditing = null; loadedDay = null; selectedDates.clear();
            for (const form of root.querySelectorAll('form')) form.reset();
            for (const id of ['group-title','group-description','group-access-note','group-report-person','group-report-date','group-day-summary','group-privacy','group-teacher-person','group-teacher-date']) $(id).textContent = '';
            $('group-list').replaceChildren(); $('group-members-list').replaceChildren(); $('group-reports').replaceChildren();
            $('group-list-view').hidden = true; $('group-detail-view').hidden = true;
            $('group-message').textContent = online() ? 'Группүүд ачаалж байна…' : 'Групп болон өдрийн тэмдэглэлээ харахын тулд нэвтэрнэ үү.';
            if (online()) {void loadList(); route();}
        },
        connected() {api.accountChanged(); if (online()) {void loadList(); route();}}
    };
    api.accountChanged();
    return api;
}
