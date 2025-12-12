@echo off
setlocal enabledelayedexpansion

set GIT_EXE=C:\Program Files\Git\bin\git.exe

echo ===============================================
echo  SwiftRide GitHub Synchronization Script
echo ===============================================
echo.

REM Check if git is installed
if not exist "%GIT_EXE%" (
    echo [ERROR] Git is not found at %GIT_EXE%
    echo Please install Git from https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

cd /d "%~dp0"

echo [1/6] Initializing Git Repository...
if not exist .git (
    "%GIT_EXE%" init
) else (
    echo Git repository already initialized.
)

echo [2/6] Adding files...
"%GIT_EXE%" add -A

echo [3/6] Configuring user...
"%GIT_EXE%" config user.email "vikas@swiftride.com"
"%GIT_EXE%" config user.name "SwiftRide Developer"

echo [4/6] Committing changes...
"%GIT_EXE%" diff-index --quiet --cached HEAD 2>nul
if not errorlevel 1 (
    "%GIT_EXE%" commit -m "SwiftRide Final: Essentials Feature ^& Documentation Completed"
) else (
    echo No changes to commit.
)

echo [5/6] Configuring Remote Origin...
"%GIT_EXE%" remote remove origin 2>nul
"%GIT_EXE%" remote add origin https://github.com/vikasredd057-create/fsd_swiftride

REM Ensure we're on main branch
"%GIT_EXE%" branch -M main 2>nul

echo [6/6] Pushing to GitHub...
echo.
echo NOTE: You may be prompted to enter GitHub credentials.
echo If using a Personal Access Token, paste it as the password.
echo.
pause

"%GIT_EXE%" push -u origin main

if errorlevel 1 (
    echo.
    echo ===============================================
    echo  [ERROR] Push Failed!
    echo ===============================================
    echo Please check:
    echo - Internet connection
    echo - GitHub credentials
    echo - Repository URL and permissions
    echo.
) else (
    echo.
    echo ===============================================
    echo  Process Finished Successfully!
    echo  Repo: https://github.com/vikasredd057-create/fsd_swiftride
    echo ===============================================
)

pause
exit /b 0
