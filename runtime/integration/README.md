# ChatGPT MCP bridge

This is a thin adapter over the existing Runtime HTTP API. It exposes only:

- `start_project`
- `continue_project`
- `project_status`

It does not import the Orchestrator, access SQLite, or implement lifecycle
decisions. Set `RUNTIME_API_URL` when the verified Runtime API is not on its
default `http://127.0.0.1:8765`.

Local development:

```text
python3 -m runtime_api
python3 -m integration.mcp_server
```

The MCP endpoint is `http://127.0.0.1:8787/mcp`. For ChatGPT developer mode,
make this endpoint reachable through Secure MCP Tunnel (or another HTTPS
development endpoint) and connect the resulting `/mcp` URL. Do not expose the
local HTTP endpoint directly to the public internet.

Local Chat MVP:

```text
python3 -m integration.local_chat
```

Open `http://127.0.0.1:8790` in a browser. The browser talks only to the local
chat server; the server calls MCP, and MCP calls the Runtime API.

The chat accepts natural Hebrew. Once a project is active, ordinary messages
are routed as continuation input; users do not need to know tool names or
project IDs. The browser receives a Hebrew presentation response only. Set
`LOCAL_CHAT_DEBUG=1` only for development to include tool, project ID, and raw
Runtime response in the API response.

## One-click macOS launcher

From Finder, double-click **Start AI Project OS.command** in the project root.
It starts the Runtime API, MCP Server, and Local Chat, waits for all three
services to answer, and opens `http://127.0.0.1:8790`. Starting twice is safe:
the launcher detects its managed PIDs and does not create duplicates.

To stop the system, double-click **Stop AI Project OS.command**. It terminates
only the PIDs recorded by the launcher; it does not kill unrelated processes.
