@echo off

:: Determinate script path
set "SCRIPT_PATH=%~dp0"

:: Start process
call %SCRIPT_PATH%\.venv\Scripts\python.exe %SCRIPT_PATH%\hv.py

pause
