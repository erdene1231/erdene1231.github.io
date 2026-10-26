"""Capture app schema metadata only; no user rows, credentials or sessions."""
import argparse
import json
import re
from pathlib import Path
from supabase_mcp import MCPError, SupabaseMCP


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='New metadata JSON path (will not overwrite)')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; preserve previous audit snapshots')
    root = Path(__file__).resolve().parent.parent
    client = SupabaseMCP()
    query = (root / 'supabase/audit/catalog.sql').read_text()
    result = client._request('tools/call', {'name': 'execute_sql', 'arguments': {'query': query}})
    if result.get('isError'):
        raise MCPError(client._safe(json.dumps(result)))
    text = json.loads(result['content'][0]['text'])['result']
    match = re.search(r'\n<untrusted-data-[^>]+>\s*(.*?)\s*</untrusted-data-', text, re.S)
    if not match:
        raise MCPError('Unexpected SQL result format; no snapshot written')
    catalog = json.loads(match.group(1))[0]['catalog']
    with args.output.open('x') as output:
        output.write(client._safe(json.dumps(catalog, indent=2, ensure_ascii=False)) + '\n')
    print(json.dumps({key: len(value or []) for key, value in catalog.items()}))


if __name__ == '__main__':
    try:
        main()
    except MCPError as error:
        print(str(error))
        raise SystemExit(1)
