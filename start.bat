@echo off
cd /d "%~dp0professor_ai_web_demo"
.venv\Scripts\uvicorn main:app
start http://127.0.0.1:8000
pause