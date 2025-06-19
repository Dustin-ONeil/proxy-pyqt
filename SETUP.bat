@echo off
echo === Setting up virtual environment and project ===

REM Step 1: Create virtual environment if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Step 2: Activate virtual environment
call venv\Scripts\activate.bat

REM Step 3: Install dependencies
if exist requirements.txt (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo WARNING: requirements.txt not found. Skipping dependency install.
)

REM Step 4: Create images folder if it doesn't exist
if not exist images (
    echo Creating 'images' folder...
    mkdir images
) else (
    echo 'images' folder already exists.
)

echo === Setup complete ===
pause
