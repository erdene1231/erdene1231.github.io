"""Lightweight educational selection quota and identity/dedup verification. Optional statements/editorials/proofs/code are not selection requirements."""
import json
import sys
import subprocess
from collections import Counter
from pathlib import Path
from audit_part04_catalog import url_key

QUOTAS = {'IOI': 30, 'EGOI': 30, 'APIO': 15, 'JOI': 20, 'Codeforces': 100, 'AtCoder': 50}


def verify(records, baseline, content_readiness=None):
    old_urls = {url_key(row['body']['url']) for row in baseline['problems']}
    old_keys = {(row['body']['source'].casefold(), row['body']['ref'].replace('/', '').casefold()) for row in baseline['problems']}
    seen_urls, seen_keys = set(), set()
    counts, source_counts, rejected = Counter(), Counter(), []
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
        # Latest scope: concise educational curation, not proof/content authorship.
        if not str(record.get('learningObjective') or record.get('curationReason') or '').strip(): reason.append('missing educational usefulness rationale')
        if record.get('priorityLevel') not in ['low','medium','high'] or not str(record.get('priorityReason','')).strip(): reason.append('missing individual priority/rationale')
        if not reason: source_counts[source] += 1
        ready = content_readiness[index] if content_readiness is not None else {'ready':False,'reason':'Selection metadata check not run'}
        if not ready.get('ready'): reason.append(ready.get('reason','selection metadata invalid'))
        if reason: rejected.append({'index': index, 'ref': record.get('ref'), 'reasons': reason})
        else: counts[source] += 1
    quotas = {source: {'required': target, 'verified': counts[source], 'remaining': max(0, target-counts[source])} for source, target in QUOTAS.items()}
    return {'complete': not rejected and all(counts[s] >= n for s, n in QUOTAS.items()), 'quotas': quotas, 'source_curated_unique': dict(source_counts), 'rejected': rejected,
            'limitations': 'Lightweight educational selection and metadata/identity/dedup check only;no original proof,solution audit,code,statement or editorial required. No production import authorized.'}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    records = json.loads(Path(sys.argv[1]).read_text())
    checked = subprocess.run(['node',str(root/'tools/check_problem_content.mjs')], input=json.dumps(records), text=True, capture_output=True, check=True)
    report = verify(records, json.loads((root/'audit/PART04-BASELINE.json').read_text()), json.loads(checked.stdout))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report['complete'] else 1)
