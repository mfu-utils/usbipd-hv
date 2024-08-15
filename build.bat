@echo off

echo Start build usbipd-hv

set "VENV=.venv"
set "BUILD_DIR=build"
set "BUILD_ASSETS=build-assets"
set "SCRIPTS=%VENV%\Scripts"
set "PY=%SCRIPTS%\python.exe"
set "PYI=%SCRIPTS%\pyinstaller.exe"
set "WORKDIR=.build_logs"
set "SPEC_FILE=build.spec"

:: Create build folder if not exists
IF not exist %BUILD_DIR% (mkdir %BUILD_DIR%)

:: Copy files for building
robocopy src %BUILD_DIR%\src /E

copy requirements.txt %BUILD_DIR%
copy install.bat %BUILD_DIR%
copy config.ini.example %BUILD_DIR%\config.ini
copy filters.yaml.example %BUILD_DIR%\filters.yaml
copy hv.py %BUILD_DIR%
copy config.py %BUILD_DIR%
copy LICENSE %BUILD_DIR%

copy %BUILD_ASSETS%\build-requirements.txt %BUILD_DIR%
copy %BUILD_ASSETS%\build.spec %BUILD_DIR%
copy %BUILD_ASSETS%\ffi.txt %BUILD_DIR%
copy %BUILD_ASSETS%\icon.ico %BUILD_DIR%

:: Set working dir
cd /d %BUILD_DIR%

:: Create working dir folder if not exists
IF not exist %WORKDIR% (mkdir %WORKDIR%)

:: Install requirements into build
echo Install requirements (%WORKDIR%\install_log.txt).
call install.bat > "%WORKDIR%\install_log.txt"
call %PY% -m pip install -r build-requirements.txt >> "%WORKDIR%\install_log.txt"

:: Create .EXE file
echo Generate .EXE file (%WORKDIR%\build_log.txt).
call %PYI% %SPEC_FILE% --workpath %WORKDIR% --distpath . > "%WORKDIR%\build_log.txt" 2>&1

:: Create archive
echo Create archive.
tar -cf usbipd-hv.tar filters.yaml config.ini LICENSE usbipd-hv.exe