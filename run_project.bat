@echo off
echo Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    pause
    exit /b
)

echo Activating virtual environment...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found at venv\Scripts\activate.bat.
    echo Please ensure the venv is created.
    pause
    exit /b
)

echo Installing requirements...
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Skipping installation.
)

echo Starting Django Server...
start "Django Server" python manage.py runserver

echo Opening Browser...
start http://127.0.0.1:8000


echo Opening VS Code...
code .
