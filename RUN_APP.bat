@echo off
REM Change to the directory where your script and venv are located
cd /d "%~dp0"

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run your PyQt app
python main.py

REM Optional: pause so the terminal stays open after running
pause
