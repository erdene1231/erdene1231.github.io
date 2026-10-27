"""Read-only baseline audit. Never assigns IDs, priorities, or production writes."""
import collections
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]


def url_key(url):
    p = urlsplit(url)
    query = urlencode(sorted((k, v) for k, v in parse_qsl(p.query, keep_blank_values=True)
                             if not k.lower().startswith('utm_')))
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip('/'), query, ''))


def main():
    path = ROOT / 'audit/PART04-BASELINE.json'
    baseline = json.loads(path.read_text())
    problems = baseline['problems']
    groups = {key: collections.defaultdict(list) for key in ['id', 'number', 'source_ref', 'url']}
    findings, review = [], []
    for row in problems:
        body = row['body']; pid = row['id']
        for key, value in [('id', pid), ('number', row['number']),
                           ('source_ref', (body.get('source', '').casefold(), re.sub(r'[/\s]', '', body.get('ref', '')).casefold())),
                           ('url', url_key(body.get('url', '')))]:
            groups[key][value].append(pid)
        issues = []
        if body.get('id') != pid or body.get('number') != row['number']: issues.append('identity mismatch')
        for language in ['hints', 'hintsEn']:
            hints = body.get(language, [])
            if not isinstance(hints, list) or len(hints) not in [0, 3] or any(not isinstance(h, str) or not h.strip() for h in hints): issues.append(language + ' invalid shape')
        if len(body.get('hints', [])) != len(body.get('hintsEn', [])): issues.append('hint language count mismatch')
        if body.get('ratingKind') == 'official' and body.get('source') != 'Codeforces': issues.append('non-CF official rating')
        if body.get('ratingKind') == 'estimated' and not body.get('ratingBasis'): issues.append('estimated rating lacks rationale')
        if issues: findings.append({'id': pid, 'issues': issues})
        review.append({'entity': 'problem', 'id': pid, 'number': row['number'], 'revision': row.get('revision'),
                       'body_sha256': hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest(),
                       'source_url': body.get('url'), 'editorial_url': body.get('editorialUrl'),
                       'legacy_priority': body.get('priority'), 'proposed_priority': None,
                       'priority_review': 'not run', 'hint_semantic_review': 'not run',
                       'rationale': None, 'no_hint_policy': 'Preserve empty hints; inspect original batch constraint before adding any.'})
    for row in baseline['tutorials']:
        review.append({'entity': 'tutorial', 'id': row['id'], 'title': row['body'].get('title'),
                       'proposed_priority': None, 'priority_review': 'not run', 'rationale': None,
                       'constraint': 'Li Chao Tree must be Low; full lesson practice review belongs to packages 2/3.'})
    out = {'baseline_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
           'counts': {'problems': len(problems), 'tutorials': len(baseline['tutorials'])},
           'duplicates': {k: [v for v in g.values() if len(v) > 1] for k, g in groups.items()},
           'shape_findings': findings, 'semantic_review': 'not run', 'writes': False}
    (ROOT / 'audit/PART04-STRUCTURAL-AUDIT.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    target = ROOT / 'audit/PART04-REVIEW-LEDGER.json'
    if not target.exists(): target.write_text(json.dumps({'reviewed': False, 'entries': review}, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'counts': out['counts'], 'duplicate_groups': {k: len(v) for k, v in out['duplicates'].items()}, 'shape_findings': len(findings)}))


if __name__ == '__main__': main()
