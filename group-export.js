// Browser-only .xlsx export. All user text is an inline string, never a formula.
const encoder = new TextEncoder();
const DAYS = ['Ням', 'Даваа', 'Мягмар', 'Лхагва', 'Пүрэв', 'Баасан', 'Бямба'];
export function validDate(value) {
    if (typeof value !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const date = new Date(value + 'T12:00:00Z');
    return !Number.isNaN(date.getTime()) && date.toISOString().slice(0, 10) === value;
}
export function todayInMongolia() {
    const parts = new Intl.DateTimeFormat('en', {timeZone: 'Asia/Ulaanbaatar', year: 'numeric', month: '2-digit', day: '2-digit'}).formatToParts(new Date());
    const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
    return `${values.year}-${values.month}-${values.day}`;
}
export function weekday(date) {
    return validDate(date) ? DAYS[new Date(date + 'T12:00:00Z').getUTCDay()] : '';
}
export function filterWeekdays(dates, allowedDays) {
    const allowed = new Set(allowedDays);
    return [...new Set(dates)].sort().filter(date => validDate(date) && allowed.has(new Date(date + 'T12:00:00Z').getUTCDay()));
}
export function selectReportRows(rows, userIds) {
    const selected = new Set(userIds);
    return rows.filter(row => selected.has(row.user_id));
}
export function shiftDate(date, delta) {
    if (!validDate(date)) throw new Error('Зөв огноо сонгоно уу.');
    const next = new Date(date + 'T12:00:00Z');
    next.setUTCDate(next.getUTCDate() + delta);
    return next.toISOString().slice(0, 10);
}
export function dateRange(start, end, limit = 62) {
    if (!validDate(start) || !validDate(end) || start > end) throw new Error('Эхлэх болон дуусах огноогоо шалгана уу.');
    const dates = [];
    for (let current = start; current <= end; current = shiftDate(current, 1)) {
        if (dates.length === limit) throw new Error('Хугацаа хэт урт байна. Богино хугацаа сонгоно уу.');
        dates.push(current);
    }
    return dates;
}
function xml(value) {
    return String(value ?? '').replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffe\uffff]/g, '')
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}
function col(index) {
    let result = '';
    for (let n = index + 1; n > 0; n = Math.floor((n - 1) / 26)) result = String.fromCharCode(65 + (n - 1) % 26) + result;
    return result;
}
function cell(value, address, style = 0) {
    if (value === null || value === undefined) return `<c r="${address}" s="${style}"/>`;
    if (typeof value === 'number') {
        if (!Number.isFinite(value)) throw new Error('Тайланд буруу тоон утга байна.');
        return `<c r="${address}" s="${style}"><v>${value}</v></c>`;
    }
    return `<c r="${address}" s="${style}" t="inlineStr"><is><t xml:space="preserve">${xml(value)}</t></is></c>`;
}
export const REPORT_HEADERS = ['Овог', 'Нэр', 'Бодсон бодлогууд', 'Нийт бодлогын тоо', 'Бодлогын хүндрэл', 'Судалсан сэдвүүд', 'Нэмэлт тэмдэглэл', 'Багшийн тэмдэглэл', 'Өмнөх овог нэр'];
const HEADERS = REPORT_HEADERS;
const LAST_COLUMN = col(HEADERS.length - 1);
function worksheet(group, date, rows) {
    const count = rows.filter(row => row.has_report).length;
    const totals = rows.filter(row => Number.isInteger(row.problem_count));
    const total = totals.reduce((sum, row) => sum + row.problem_count, 0);
    const title = `${group.name} — ${date}, ${weekday(date)}`;
    const subtitle = `${rows.length} гишүүн · ${count} тэмдэглэл · Нийт ${total} бодлого (${totals.length} гишүүн тоо бөглөсөн). Хоосон тоо нь 0 гэсэн утгагүй.`;
    const lines = [
        `<row r="1" ht="32" customHeight="1">${cell(title, 'A1', 1)}</row>`,
        `<row r="2" ht="36" customHeight="1">${cell(subtitle, 'A2', 4)}</row>`,
        `<row r="3" ht="42" customHeight="1">${HEADERS.map((h, i) => cell(h, col(i) + '3', 2)).join('')}</row>`
    ];
    rows.forEach((row, index) => {
        const values = [row.last_name ?? '', row.first_name ?? '', row.solved_problems ?? '',
            row.problem_count ?? null, row.difficulty ?? '', row.topics ?? '', row.notes ?? '', row.teacher_note ?? '',
            (!row.last_name && !row.first_name) ? row.full_name ?? '' : ''];
        const lineCount = Math.max(...[2, 4, 5, 6, 7].map(i => Math.ceil(String(values[i]).length / 45) + String(values[i]).split('\n').length - 1));
        const height = Math.min(240, Math.max(36, lineCount * 16));
        const number = index + 4;
        lines.push(`<row r="${number}" ht="${height}" customHeight="1">${values.map((v, i) => cell(v, col(i) + number, i === 3 ? 3 : 0)).join('')}</row>`);
    });
    const widths = [23, 23, 58, 16, 30, 36, 48, 48, 30];
    return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<dimension ref="A1:${LAST_COLUMN}${Math.max(3, rows.length + 3)}"/><sheetViews><sheetView workbookViewId="0"><pane ySplit="3" topLeftCell="A4" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>
<sheetFormatPr defaultRowHeight="18"/><cols>${widths.map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w}" customWidth="1"/>`).join('')}</cols>
<sheetData>${lines.join('')}</sheetData><autoFilter ref="A3:${LAST_COLUMN}${Math.max(3, rows.length + 3)}"/><mergeCells count="2"><mergeCell ref="A1:${LAST_COLUMN}1"/><mergeCell ref="A2:${LAST_COLUMN}2"/></mergeCells>
<pageMargins left="0.25" right="0.25" top="0.4" bottom="0.4" header="0.2" footer="0.2"/><pageSetup orientation="landscape" paperSize="9" fitToWidth="1" fitToHeight="0"/>
</worksheet>`;
}
const STYLES = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="4"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="18"/><color rgb="FF214C3A"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font><font><sz val="11"/><color rgb="FF59685A"/><name val="Calibri"/></font></fonts>
<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF214C3A"/><bgColor indexed="64"/></patternFill></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="5"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center"/></xf><xf numFmtId="0" fontId="2" fillId="2" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf><xf numFmtId="1" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1" applyNumberFormat="1"><alignment vertical="top" horizontal="center"/></xf><xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf></cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>`;
const CRC_TABLE = Uint32Array.from({length: 256}, (_, value) => {
    for (let i = 0; i < 8; i++) value = (value & 1) ? 0xedb88320 ^ (value >>> 1) : value >>> 1;
    return value >>> 0;
});
function crc32(bytes) {
    let crc = 0xffffffff;
    for (const byte of bytes) crc = CRC_TABLE[(crc ^ byte) & 255] ^ (crc >>> 8);
    return (crc ^ 0xffffffff) >>> 0;
}
function binary(size, fields) {
    const bytes = new Uint8Array(size), view = new DataView(bytes.buffer);
    for (const [offset, value, width] of fields) width === 4 ? view.setUint32(offset, value, true) : view.setUint16(offset, value, true);
    return bytes;
}
function zip(files) {
    const entries = [], central = [];
    let offset = 0, directorySize = 0;
    for (const [filename, contents] of files) {
        const name = encoder.encode(filename), data = encoder.encode(contents), crc = crc32(data);
        const header = binary(30, [[0, 0x04034b50, 4], [4, 20, 2], [6, 0x800, 2], [10, 0, 2], [12, 33, 2], [14, crc, 4], [18, data.length, 4], [22, data.length, 4], [26, name.length, 2]]);
        const record = binary(46, [[0, 0x02014b50, 4], [4, 20, 2], [6, 20, 2], [8, 0x800, 2], [14, 33, 2], [16, crc, 4], [20, data.length, 4], [24, data.length, 4], [28, name.length, 2], [42, offset, 4]]);
        entries.push(header, name, data); central.push(record, name);
        offset += header.length + name.length + data.length;
        directorySize += record.length + name.length;
        if (offset > 64 * 1024 * 1024) throw new Error('Тайлан хэт том байна. Цөөн өдөр сонгоод дахин export хийнэ үү.');
    }
    const end = binary(22, [[0, 0x06054b50, 4], [8, files.length, 2], [10, files.length, 2], [12, directorySize, 4], [16, offset, 4]]);
    const result = new Uint8Array(offset + directorySize + end.length);
    let position = 0;
    for (const part of [...entries, ...central, end]) {result.set(part, position); position += part.length;}
    return result;
}
export function createReportWorkbook({group, dates, rows}) {
    const selected = [...new Set(dates)].sort();
    if (!selected.length || selected.length > 62 || selected.some(date => !validDate(date))) throw new Error('1–62 зөв огноо сонгоно уу.');
    const files = [];
    const types = selected.map((_, i) => `<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('');
    files.push(['[Content_Types].xml', `<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>${types}</Types>`]);
    files.push(['_rels/.rels', '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>']);
    files.push(['xl/workbook.xml', `<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><bookViews><workbookView/></bookViews><sheets>${selected.map((d, i) => `<sheet name="${d}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`).join('')}</sheets></workbook>`]);
    files.push(['xl/_rels/workbook.xml.rels', `<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">${selected.map((_, i) => `<Relationship Id="rId${i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`).join('')}<Relationship Id="rId${selected.length + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>`]);
    files.push(['xl/styles.xml', STYLES]);
    for (const [i, date] of selected.entries()) files.push([`xl/worksheets/sheet${i + 1}.xml`, worksheet(group, date, rows.filter(row => row.report_date === date))]);
    return zip(files);
}
