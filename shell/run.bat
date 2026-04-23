@echo off
title Rivals OSINT Scanner

color 0B
echo.
echo    ____       _ _       _
echo   ^|  _ \ ___ (_) ^| ___ ^| ^|
echo   ^| ^|_) / _ \^| ^| ^|/ _ \^| ^|
echo   ^|  _ ^< (_) ^| ^| ^| (_) ^| ^|
echo   ^|_^| \_\___/^|_^|_^|\___/^|_^|
echo.

:: Check for Go
where go >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Go is not installed
    pause
    exit /b 1
)

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed
    pause
    exit /b 1
)

:: Install Python dependencies
if not exist "venv" (
    echo Installing Python dependencies...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r scripts\requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Build Go binary
echo Building Rivals binary...
go build -o bin\rivals.exe cmd\rivals\*.go

:: Parse arguments
set USERNAME=%1
if "%USERNAME%"=="" (
    set /p USERNAME="Enter username: "
)

:: Run scanner
echo.
echo Starting scan for: %USERNAME%
echo.

bin\rivals.exe -u "%USERNAME%" -o results.json

deactivate
echo.
echo Scan completed! Results saved to results.json
pause
