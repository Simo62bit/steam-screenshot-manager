@echo off
setlocal enabledelayedexpansion

:: Define ESC for ANSI colors
for /f %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

:: ANSI Colors
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "RESET=%ESC%[0m"

set "error_flag=0"

echo %YELLOW%=======================================%RESET%
echo %YELLOW%Checking for Python 3.8+...%RESET%
echo %YELLOW%=======================================%RESET%

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%RESET% Python not found in PATH.
    echo Please install Python from https://www.python.org/ and add it to PATH.
    set "error_flag=1"
    goto end
) else (
    for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set "PY_VERSION=%%v"
    echo Version found: !PY_VERSION!

    for /f "tokens=1,2 delims=." %%a in ("!PY_VERSION!") do (
        set "PY_MAJOR=%%a"
        set "PY_MINOR=%%b"
    )

    if !PY_MAJOR! lss 3 (
        echo %RED%[ERROR]%RESET% Python 3.8 or higher is required.
        set "error_flag=1"
        goto end
    ) else (
        if !PY_MAJOR! equ 3 if !PY_MINOR! lss 8 (
            echo %RED%[ERROR]%RESET% Python 3.8 or higher is required.
            set "error_flag=1"
            goto end
        )
    )

    echo %GREEN%[OK]%RESET% Python 3.8+ found.
)

echo.
echo %YELLOW%=======================================%RESET%
echo %YELLOW%Checking for pip...%RESET%
echo %YELLOW%=======================================%RESET%

where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%RESET% pip not found in PATH.
    echo Try reinstalling Python with the "Add pip to PATH" option enabled.
    set "error_flag=1"
    goto end
) else (
    echo %GREEN%[OK]%RESET% pip found.
)

echo.
echo %YELLOW%=======================================%RESET%
echo %YELLOW%Google Chrome requirement%RESET%
echo %YELLOW%=======================================%RESET%

echo Make sure Google Chrome is installed on your system.
echo You can download it from: https://www.google.com/chrome/
echo.

echo %YELLOW%=======================================%RESET%
echo %YELLOW%Installing required Python packages...%RESET%
echo %YELLOW%=======================================%RESET%

pip install selenium pillow requests
if %errorlevel% neq 0 (
    echo %RED%[ERROR]%RESET% Package installation failed.
    set "error_flag=1"
    goto end
) else (
    echo %GREEN%[OK]%RESET% Packages installed successfully.
)

echo.
echo %GREEN%[SUCCESS]%RESET% All requirements are satisfied. Environment ready.

:end
if "%error_flag%"=="0" pause
endlocal
