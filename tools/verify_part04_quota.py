"""Verify reviewed new-task quota evidence without assigning production IDs.

Metadata candidates do not qualify. Each accepted record needs statement and
solution review evidence, a learning objective, a reasoned priority, and a
canonical source identity. Run with an explicit reviewed-ledger JSON path.
"""
import json
import sys
from collections import Counter
from pathlib import Path
from audit_part04_catalog import url_key

QUOTAS = {'IOI': 30, 'EGOI': 30, 'APIO': 15, 'JOI': 20, 'Codeforces': 100, 'AtCoder': 50}


def verify(records, baseline):
    old_urls = {url_key(row['body']['url']) for row in baseline['problems']}
    old_keys = {(row['body']['source'].casefold(), row['body']['ref'].replace('/', '').casefold()) for row in baseline['problems']}
    seen_urls, seen_keys = set(), set()
    counts, rejected = Counter(), []
    for index, record in enumerate(records):
        reason = []
        source = record.get('source', '')
        url = record.get('url', '')
        key = (source.casefold(), record.get('ref', '').replace('/', '').casefold())
        normalized = url_key(url)
        if source not in QUOTAS: reason.append('unsupported quota source')
        if not key[1] or not url.startswith('https://'): reason.append('missing canonical identity')
        if normalized in old_urls or key in old_keys: reason.append('existing baseline task')
        if normalized in seen_urls or key in seen_keys: reason.append('duplicate submitted task')
        seen_urls.add(normalized); seen_keys.add(key)
        for field in ['statementEvidence', 'solutionEvidence']:
            evidence = record.get(field, {})
            if not isinstance(evidence, dict) or not str(evidence.get('url', '')).startswith('https://') or not evidence.get('sha256') or len(evidence.get('sha256', '')) != 64 or not evidence.get('reviewNote'):
                reason.append(field + ' requires source URL, content hash and substantive review note')
        for field in ['learningObjective', 'priorityReason', 'primaryTopic']:
            if not isinstance(record.get(field), str) or not record[field].strip(): reason.append('missing ' + field)
        if record.get('priorityLevel') not in ['low', 'medium', 'high']: reason.append('unreviewed priority')
        if record.get('reviewStatus') != 'reviewed': reason.append('not reviewed')
        if reason: rejected.append({'index': index, 'ref': record.get('ref'), 'reasons': reason})
        else: counts[source] += 1
    quotas = {source: {'required': target, 'verified': counts[source], 'remaining': max(0, target-counts[source])} for source, target in QUOTAS.items()}
    return {'complete': not rejected and all(counts[s] >= n for s, n in QUOTAS.items()), 'quotas': quotas, 'rejected': rejected,
            'limitations': 'Evidence fields are an accountability gate; human semantic review and cross-source aliases still require verification. No production import is authorized by this report.'}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    records = json.loads(Path(sys.argv[1]).read_text())
    report = verify(records, json.loads((root/'audit/PART04-BASELINE.json').read_text()))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report['complete'] else 1)
