@echo off
echo Starting BMO Data Validation Application...
echo.
echo Make sure you have installed the requirements:
echo pip install -r requirements.txt
echo.
echo Starting server on http://localhost:8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000