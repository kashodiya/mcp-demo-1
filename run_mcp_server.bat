@REM set BASE_URL=http://localhost:9008

@REM uv run python bmo_mcp_server.py


@echo off
echo Starting BMO MCP Servers...

set BASE_URL=http://localhost:9008

start /B uv run python bmo_mcp_server.py
start /B uv run python sql_mcp_server.py

echo Both MCP servers started. Press Ctrl+C to stop both servers.
pause >nul
