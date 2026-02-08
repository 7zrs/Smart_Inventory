@echo off
echo ========================================
echo Smart Inventory - Starting Application
echo ========================================
echo.

echo [1/5] Checking for Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo [2/5] Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✓ Virtual environment activated
) else (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to set up the project.
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
pip install -q -r requirements.txt
echo ✓ Dependencies up to date
echo.

echo [5/5] Starting Django server...
echo.

REM Start Django server in a new window
start "Smart Inventory - Django Server" cmd /k "venv\Scripts\activate.bat && python manage.py runserver"

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
