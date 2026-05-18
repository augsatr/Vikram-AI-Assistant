@echo off
title Vikram AI Assistant - Setup
echo ========================================
echo   Vikram - JARVIS-like AI Assistant
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+ from python.org
    pause
    exit /b 1
)
echo [OK] Python found

:: Check Ollama
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing Ollama...
    curl -L https://ollama.com/download/OllamaSetup.exe -o "%TEMP%\OllamaSetup.exe"
    start /wait "" "%TEMP%\OllamaSetup.exe"
)

:: Install Python packages
echo [INFO] Installing Python packages...
pip install -r requirements.txt

:: Setup .env
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo [INFO] Created .env file - please add your Picovoice API key
    )
)

:: Pull Ollama model (optional)
echo.
set /p PULL_MODEL="Download Qwen 2.5 model now? (y/n, default: n): "
if /i "%PULL_MODEL%"=="y" (
    echo Pulling qwen2.5 (this may take a while)...
    ollama pull qwen2.5
)

echo.
echo ========================================
echo   Setup complete! Run vikram.bat to start
echo ========================================
pause
