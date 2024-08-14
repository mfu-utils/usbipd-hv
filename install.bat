@echo off

set "VENV=.venv"

:: Create virtual environment
echo Create virtual environment at (%VENV%)
call python -m venv %VENV%

:: Create venv python path
set "PY=%VENV%\Scripts\python.exe"

:: Update pip into venv
echo Upgrade pip into virtual environment
call %PY% -m pip install --upgrade pip

:: Install requirements
echo Install requirements into virtual environment
call %PY% -m pip install -r requirements.txt
