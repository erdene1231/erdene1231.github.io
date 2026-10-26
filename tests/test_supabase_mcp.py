"""Offline transport checks: never use real environment credentials."""
import contextlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
from supabase_mcp import MCPError, SupabaseMCP

class Response:
    status = 200
    def __init__(self, headers=None, body=None):
        self.headers = headers or {}
        self.body = body
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self): return json.dumps(self.body).encode() if self.body is not None else b''

class SessionTests(unittest.TestCase):
    @patch.dict('os.environ', {'SUPABASE_WRITE_TOKEN': 'test-placeholder', 'SUPABASE_PROJECT_REF': 'test-project'})
    def test_new_clients_initialize_and_all_followups_carry_session(self):
        requests = []
        def send(request, timeout):
            requests.append(request)
            body = json.loads(request.data)
            if body['method'] == 'initialize':
                return Response({'Mcp-Session-Id': 'test-session'}, {'result': {'protocolVersion': '2025-03-26'}})
            if body['method'] == 'notifications/initialized':
                self.assertNotIn('id', body)
                return Response()
            return Response(body={'result': {'content': []}})
        output = io.StringIO()
        with patch('urllib.request.urlopen', side_effect=send), contextlib.redirect_stdout(output):
            for _ in range(2):
                client = SupabaseMCP()
                client.read_tool('list_migrations')
                with self.assertRaises(MCPError): client.read_tool('apply_migration')
                with self.assertRaises(MCPError): client.read_tool('execute_sql', {'query': 'DELETE FROM x'})
        self.assertEqual(len(requests), 6)
        for request in requests:
            headers = {k.lower(): v for k,v in request.header_items()}
            self.assertEqual(headers['user-agent'], 'ErdeneClub-Codex/1.0')
            if json.loads(request.data)['method'] == 'initialize':
                self.assertNotIn('mcp-session-id', headers)
            else:
                self.assertEqual(headers['mcp-session-id'], 'test-session')
                self.assertEqual(headers['mcp-protocol-version'], '2025-03-26')
        self.assertNotIn('test-placeholder', output.getvalue())
        self.assertNotIn('test-session', output.getvalue())

if __name__ == '__main__': unittest.main()
