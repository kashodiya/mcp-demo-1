@echo off
echo Starting BMO MCP Servers...

set BASE_URL=http://localhost:9008

start "BMO Server" uv run python bmo_mcp_server.py
start "SQL Server" uv run python sql_mcp_server.py

echo Both MCP servers started. Press Ctrl+C to stop.
@REM pause >nul
