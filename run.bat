@echo off

rem Run the uvicorn command
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000