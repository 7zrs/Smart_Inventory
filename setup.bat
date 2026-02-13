@echo off
cls
echo ========================================
echo Smart Inventory - Automated Setup
echo ========================================
echo.

REM Check Python
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Install Python 3.9 - 3.13 from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Validate Python version (requires 3.9 - 3.13)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYTHON_VERSION=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)

if %PY_MAJOR% NEQ 3 (
    echo ERROR: Python 3 is required. Found Python %PYTHON_VERSION%
    echo Install Python 3.9 - 3.13 from https://www.python.org/downloads/
    pause
    exit /b 1
)

if %PY_MINOR% LSS 9 (
    echo ERROR: Python 3.9 or higher is required. Found Python %PYTHON_VERSION%
    echo Install Python 3.9 - 3.13 from https://www.python.org/downloads/
    pause
    exit /b 1
)

if %PY_MINOR% GEQ 14 (
    echo ERROR: Python 3.14+ is not supported due to dependency constraints.
    echo Found Python %PYTHON_VERSION%
    echo Install Python 3.9 - 3.13 from https://www.python.org/downloads/release/python-3131/
    pause
    exit /b 1
)

echo ✓ Python %PYTHON_VERSION% found (compatible)
echo.

REM Create venv
echo [2/7] Setting up virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Created virtual environment
) else (
    echo ✓ Virtual environment exists
)
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [3/7] Installing dependencies...
pip install -q -r requirements.txt
echo ✓ Dependencies installed
echo.

REM Setup .env
echo [4/7] Setting up environment file...
if exist .env (
    echo ✓ .env already exists (keeping existing)
    goto skip_env_setup
)

REM Create .env from template
if not exist .env.example (
    echo ERROR: .env.example not found
    pause
    exit /b 1
)

copy .env.example .env
echo ✓ Created .env from template
echo.

REM Generate SECRET_KEY
echo Generating Django SECRET_KEY...
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > temp_key.txt
set /p SECRET_KEY=<temp_key.txt
del temp_key.txt
powershell -Command "(Get-Content .env) -replace 'SECRET_KEY=your-secret-key-here', 'SECRET_KEY=%SECRET_KEY%' | Set-Content .env"
echo ✓ SECRET_KEY generated
echo.

REM Prompt for API key
echo ========================================
echo Google Gemini API Key Required
echo ========================================
echo.
echo Get your FREE API key from:
echo https://makersuite.google.com/app/apikey
echo.
echo You can:
echo   1. Enter it now
echo   2. Press Enter to skip (add later to .env)
echo.
set /p GEMINI_KEY=Paste your API key or press Enter to skip:

if "%GEMINI_KEY%"=="" (
    echo.
    echo ⚠ Skipped API key - edit .env later
) else (
    powershell -Command "(Get-Content .env) -replace 'GOOGLE_API_KEY=YOUR_NEW_GEMINI_API_KEY_HERE', 'GOOGLE_API_KEY=%GEMINI_KEY%' | Set-Content .env"
    powershell -Command "(Get-Content .env) -replace 'GOOGLE_API_KEY=your-gemini-api-key-here', 'GOOGLE_API_KEY=%GEMINI_KEY%' | Set-Content .env"
    echo ✓ API key saved to .env
)
echo.

:skip_env_setup

REM Validate API key
echo [5/7] Validating Google Gemini API key...
for /f "tokens=2 delims==" %%a in ('findstr "GOOGLE_API_KEY" .env') do set CURRENT_KEY=%%a

REM Check if key is missing or placeholder
if "%CURRENT_KEY%"=="" goto prompt_api_key
if "%CURRENT_KEY%"=="YOUR_NEW_GEMINI_API_KEY_HERE" goto prompt_api_key
if "%CURRENT_KEY%"=="your-gemini-api-key-here" goto prompt_api_key
echo ✓ API key configured
goto api_key_done

:prompt_api_key
echo.
echo ========================================
echo ⚠ Google Gemini API Key Not Found
echo ========================================
echo.
echo The AI Assistant requires a Google Gemini API key.
echo.
echo Get your FREE API key from:
echo https://makersuite.google.com/app/apikey
echo.
echo You can:
echo   1. Enter your API key now
echo   2. Press Enter to skip (AI Assistant will NOT work)
echo.
set /p NEW_API_KEY=Paste your API key here:

if "%NEW_API_KEY%"=="" (
    echo.
    echo ⚠⚠⚠ WARNING ⚠⚠⚠
    echo API key not provided - AI Assistant will NOT work
    echo You can add it later by editing .env file
    echo Look for: GOOGLE_API_KEY=your-key-here
    echo.
    pause
) else (
    powershell -Command "(Get-Content .env) -replace 'GOOGLE_API_KEY=.*', 'GOOGLE_API_KEY=%NEW_API_KEY%' | Set-Content .env"
    echo ✓ API key saved to .env
)
echo.

:api_key_done

REM Migrations
echo [6/7] Running database migrations...
python manage.py migrate --run-syncdb
if errorlevel 1 (
    echo ⚠ Migration failed. Try deleting db.sqlite3 and running setup again.
    pause
    exit /b 1
)
echo ✓ Migrations complete
echo.

REM Superuser
echo [7/7] Admin account setup...
echo.
set /p CREATE_ADMIN=Create admin account now? (Y/N):
if /i "%CREATE_ADMIN%"=="Y" (
    python manage.py createsuperuser
) else (
    echo Skipped - run later: python manage.py createsuperuser
)
echo.

REM Complete
echo Finalizing...
echo.
echo ========================================
echo ✓ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Run: run_project.bat
echo   2. Visit: http://localhost:8501
echo.
if "%GEMINI_KEY%"=="" (
    echo Remember to add your API key to .env:
    echo   GOOGLE_API_KEY=your-key-here
    echo.
)
echo ========================================
pause
