"""Read-only Supabase MCP checks; credentials and sessions stay in memory."""
import datetime
import json
import os
import urllib.error
import urllib.parse
import urllib.request


class MCPError(RuntimeError):
    pass


class SupabaseMCP:
    def __init__(self):
        token = os.environ.get("SUPABASE_WRITE_TOKEN")
        project = os.environ.get("SUPABASE_PROJECT_REF")
        if not token or not project:
            raise MCPError("Required Supabase runtime variables are missing")
        self._token = token
        self._session = None
        self._id = 0
        self._url = "https://mcp.supabase.com/mcp?" + urllib.parse.urlencode(
            {"project_ref": project, "features": "database"}
        )
        self._headers = {
            "Authorization": "Bearer " + token,
            "User-Agent": "ErdeneClub-Codex/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }
        result = self._request("initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "ErdeneClub-Codex", "version": "1.0"},
        })
        if not self._session:
            raise MCPError("Initialize response omitted Mcp-Session-Id")
        self._headers["MCP-Protocol-Version"] = result["protocolVersion"]
        self._request("notifications/initialized", {}, notification=True)

    def _safe(self, value):
        text = str(value).replace(self._token, "[REDACTED]")
        if self._session:
            text = text.replace(self._session, "[REDACTED]")
        return text

    def _request(self, method, params, notification=False):
        self._id += 1
        body = {"jsonrpc": "2.0", "method": method, "params": params}
        if not notification:
            body["id"] = self._id
        sent = datetime.datetime.now(datetime.timezone.utc).isoformat()
        request = urllib.request.Request(
            self._url, json.dumps(body).encode(), self._headers, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                session = response.headers.get("Mcp-Session-Id")
                if session:
                    self._session = session
                    self._headers["Mcp-Session-Id"] = session
                raw = response.read().decode()
                print(json.dumps({"method": method, "http_status": response.status,
                                  "request_utc": sent}))
                if notification and not raw:
                    return {}
                if "text/event-stream" in response.headers.get("Content-Type", ""):
                    events = []
                    data = []
                    for line in raw.splitlines() + [""]:
                        if line.startswith("data:"):
                            data.append(line[5:].lstrip())
                        elif not line and data:
                            events.append(json.loads("\n".join(data)))
                            data = []
                    replies = [e for e in events if e.get("id") == body.get("id")]
                    if not replies:
                        raise MCPError("No matching JSON-RPC response")
                    result = replies[-1]
                else:
                    result = json.loads(raw)
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise MCPError(self._safe(json.dumps({
                "http_status": error.code, "cloudflare_ray_id": error.headers.get("cf-ray"),
                "request_utc": sent, "error": detail,
            }))) from None
        except (OSError, ValueError) as error:
            raise MCPError(self._safe(str(error))) from None
        if "error" in result:
            raise MCPError(self._safe(json.dumps(result["error"])))
        return result.get("result", {})

    def read_tool(self, name, arguments=None):
        if name not in {"list_migrations", "execute_sql"}:
            raise MCPError("Tool is outside this read-only check's allowlist")
        if name == "execute_sql" and arguments != {"query": COUNT_QUERY}:
            raise MCPError("Only the fixed COUNT query is allowed")
        result = self._request("tools/call", {"name": name, "arguments": arguments or {}})
        if result.get("isError"):
            raise MCPError(self._safe(json.dumps(result)))
        return result


COUNT_QUERY = (
    "SELECT (SELECT COUNT(*) FROM public.problem_catalog) AS problem_count, "
    "(SELECT COUNT(*) FROM public.tutorial_catalog) AS tutorial_count;"
)


def main():
    client = SupabaseMCP()
    for name, args in [("execute_sql", {"query": COUNT_QUERY}), ("list_migrations", {})]:
        print(client._safe(json.dumps({"tool": name, "result": client.read_tool(name, args)})))


if __name__ == "__main__":
    try:
        main()
    except MCPError as error:
        print(str(error))
        raise SystemExit(1)
