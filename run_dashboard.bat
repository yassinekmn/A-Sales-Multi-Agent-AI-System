@echo off
REM Windows startup script for AI Data Team Dashboard

echo.
echo ========================================
echo  AI Data Team - Streamlit Dashboard
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv\" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

REM Run Streamlit
echo.
echo Starting dashboard...
echo.
echo Dashboard URL: http://localhost:8501
echo Close this window to stop the server.
echo.

streamlit run streamlit_app.py
pause
