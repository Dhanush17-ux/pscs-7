@echo off
cd /d D:\data\raw
call ..\venv\Scripts\activate

start cmd /k "uvicorn main:app --reload --port 8000"
timeout /t 3 >nul

start cmd /k "streamlit run chat_ui.py"
