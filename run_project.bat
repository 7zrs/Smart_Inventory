@echo off
echo ========================================
echo Smart Inventory - Starting Application
echo ========================================
echo.

REM Determine which Python to use
set PYTHON_CMD=
set PIP_CMD=

echo [1/5] Checking for Python...
if exist python\python.exe (
    set PYTHON_CMD=python\python.exe
    set PIP_CMD=python\Scripts\pip.exe
    echo ✓ Using local embedded Python
) else if exist venv\Scripts\activate.bat (
    set PYTHON_CMD=python
    set PIP_CMD=pip
    echo ✓ Using system Python
) else (
    echo ERROR: No Python environment found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)
echo.

REM Activate venv if it exists
echo [2/5] Activating environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else if exist python\python.exe (
    echo ✓ Embedded Python ready
) else (
    echo ERROR: No environment found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)
echo.

echo [3/5] Checking environment configuration...
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please run setup.bat first to set up the project.
    echo.
    pause
    exit /b 1
)
echo ✓ .env file found
echo.

echo [4/5] Checking dependencies...
%PIP_CMD% install -q --only-binary :all: -r requirements.txt >nul 2>&1
echo ✓ Dependencies up to date
echo.

echo [5/5] Starting Django server...
echo.

REM Start Django server in a new window
if exist venv\Scripts\activate.bat (
    start "Smart Inventory - Django Server" cmd /k "venv\Scripts\activate.bat && python manage.py runserver"
) else (
    start "Smart Inventory - Django Server" cmd /k "python\python.exe manage.py runserver"
)

REM Wait for Django to start
echo Waiting for server to start...
timeout /t 5 /nobreak >nul

REM Open browser
start http://127.0.0.1:8000

echo.
echo ========================================
echo ✓ Application Started Successfully!
echo ========================================
echo.
echo Django server is running at:
echo   http://127.0.0.1:8000
echo.
echo To stop the server:
echo   Close the Django Server window
echo.
echo Press any key to close this window...
pause >nul
