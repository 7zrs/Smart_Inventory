@echo off
cls
echo ========================================
echo Smart Inventory - Automated Setup
echo ========================================
echo.

REM ---- Determine Python to use ----
set PYTHON_CMD=
set PIP_CMD=
set USE_VENV=1

echo [1/3] Checking Python installation...

REM Check system Python
python --version >nul 2>&1
if errorlevel 1 goto :no_system_python

for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)

set SYSTEM_OK=1
if %PY_MAJOR% NEQ 3 set SYSTEM_OK=0
if %PY_MINOR% LSS 9 set SYSTEM_OK=0
if %PY_MINOR% GEQ 14 set SYSTEM_OK=0

if %SYSTEM_OK%==0 goto :system_python_bad
set PYTHON_CMD=python
set PIP_CMD=pip
echo   Python %PYTHON_VERSION% found - compatible
echo.
goto :python_ready

:system_python_bad
echo   Found Python %PYTHON_VERSION% - not compatible, need 3.9-3.13
goto :need_embedded

:no_system_python
echo   Python not found on this system.

:need_embedded
set USE_VENV=0

REM Check if embedded Python already exists
if not exist python\python.exe goto :download_python
set PYTHON_CMD=python\python.exe
set PIP_CMD=python\Scripts\pip.exe
REM Ensure project root is in path file for re-runs
findstr /C:".." python\python313._pth >nul 2>&1
if errorlevel 1 echo ..>> python\python313._pth
echo   Using local embedded Python
echo.
goto :python_ready

:download_python
echo.
echo   Downloading portable Python 3.13.1...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.13.1/python-3.13.1-embed-amd64.zip' -OutFile '%TEMP%\python-embed.zip'"
if errorlevel 1 goto :download_failed

echo   Extracting...
powershell -Command "Expand-Archive -Path '%TEMP%\python-embed.zip' -DestinationPath 'python' -Force"
if errorlevel 1 goto :extract_failed
del "%TEMP%\python-embed.zip" >nul 2>&1

REM Enable pip support and add project root to Python path
powershell -Command "(Get-Content 'python\python313._pth') -replace '#import site','import site' | Set-Content 'python\python313._pth'"
echo ..>> python\python313._pth

REM Install pip
echo   Installing pip...
powershell -Command "Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile '%TEMP%\get-pip.py'"
python\python.exe "%TEMP%\get-pip.py" --no-warn-script-location >nul 2>&1
del "%TEMP%\get-pip.py" >nul 2>&1

if not exist python\Scripts\pip.exe goto :pip_failed

set PYTHON_CMD=python\python.exe
set PIP_CMD=python\Scripts\pip.exe
echo   Portable Python 3.13.1 ready
echo.
goto :python_ready

:download_failed
echo   ERROR: Failed to download Python.
echo   Please check your internet connection and try again.
pause
exit /b 1

:extract_failed
echo   ERROR: Failed to extract Python.
pause
exit /b 1

:pip_failed
echo   ERROR: pip installation failed.
pause
exit /b 1

:python_ready

REM ---- Virtual environment ----
echo [2/3] Setting up environment...
if %USE_VENV%==0 goto :skip_venv

if not exist venv (
    %PYTHON_CMD% -m venv venv
    echo   Created virtual environment
) else (
    echo   Virtual environment exists
)
call venv\Scripts\activate.bat
goto :venv_done

:skip_venv
echo   Using embedded Python - venv not needed
:venv_done
echo.

REM ---- Install dependencies ----
echo [3/3] Installing dependencies...
%PIP_CMD% install -q --no-warn-script-location --only-binary :all: -r requirements.txt
if errorlevel 1 (
    echo.
    echo   Retrying without binary-only constraint...
    %PIP_CMD% install -q --no-warn-script-location -r requirements.txt
)
echo   Dependencies installed
echo.

REM ---- Hand off to Python for the rest ----
echo ----------------------------------------
echo   Python handling remaining setup...
echo ----------------------------------------
echo.
%PYTHON_CMD% setup_helper.py %PYTHON_CMD%
if errorlevel 1 (
    echo.
    echo   Setup helper encountered an error.
    pause
    exit /b 1
)

pause
