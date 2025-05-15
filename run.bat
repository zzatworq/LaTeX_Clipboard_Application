@echo off
ECHO Setting up and running LaTeX Clipboard Application...

:: Check if Python is installed
where python >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python is not installed or not in PATH. Please install Python 3.8+.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
IF NOT EXIST "venv" (
    ECHO Creating virtual environment...
    python -m venv venv
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
CALL venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install dependencies
ECHO Installing dependencies from requirements.txt...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    ECHO Failed to install dependencies.
    pause
    exit /b 1
)

:: Run the application
ECHO Starting LaTeX Clipboard Application...
python main.py
IF %ERRORLEVEL% NEQ 0 (
    ECHO Application failed to start.
    pause
    exit /b 1
)

:: Deactivate virtual environment
deactivate
ECHO Application closed.
pause'''