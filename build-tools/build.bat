@echo off

echo Start build usbipd-hv

set "BUILD_DIR=build"
set "BUILT_TOOLS=build-tools"
set "SCRIPTS=%VENV%\Scripts"
set "PY=%SCRIPTS%\python.exe"
set "PYI=%SCRIPTS%\pyinstaller.exe"
set "WORKDIR=.build_logs"
set "SPEC_FILE=build.spec"

:: Create build folder if not exists
IF not exist %BUILD_DIR% (mkdir %BUILD_DIR%)

:: Copy files for building
robocopy src %BUILD_DIR%/src

copy requirements.txt %BUILD_DIR%
copy install.bat %BUILD_DIR%
copy config.ini.example %BUILD_DIR%\config.ini
copy filters.yaml.example %BUILD_DIR%\filters.yaml
copy hv.py %BUILD_DIR%

copy %BUILT_TOOLS%\build-requirements.txt %BUILD_DIR%
copy %BUILT_TOOLS%\build.spec %BUILD_DIR%
copy %BUILT_TOOLS%\ffi.txt %BUILD_DIR%

:: Set working dir
cd /d %BUILD_DIR%

:: Create working dir folder if not exists
IF not exist %WORKDIR% (mkdir %WORKDIR%)

:: Install requirements into build
call install.bat
call %PY% -m pip install -r build-requirements.txt

:: Create .EXE file
call %PYI% %SPEC_FILE% --workpath %WORKDIR% --distpath . > "%WORKDIR%\build_log.txt" 2>&1

:: Create archive
tar -cf usbipd-hv.zip filters.yaml config.ini usbipd-hv.exe