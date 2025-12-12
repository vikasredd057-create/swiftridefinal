@echo off
echo ===============================================
echo  SwiftRide GitHub Synchronization Script
echo ===============================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not in your PATH.
    echo Please install Git from https://git-scm.com/download/win
    echo After installing, restart your terminal or computer and run this script again.
    echo.
    pause
    exit /b
)

echo [1/6] Initializing Git Repository...
if not exist .git (
    git init
) else (
    echo Git repository already initialized.
)

echo [2/6] Adding files...
git add .

echo [3/6] Committing changes...
git commit -m "SwiftRide Final: Essentials Feature & Documentation Completed"

echo [4/6] Renaming branch to main...
git branch -M main

echo [5/6] Configuration Remote Origin...
git remote remove origin 2>nul
git remote add origin https://github.com/vikasredd057-create/fsd_swiftride

echo [6/6] Pushing to GitHub...
echo.
echo NOTE: If a browser window opens, please sign in to GitHub to authorize.
echo.
git push -u origin main

echo.
echo ===============================================
echo  Process Finished.
echo  Repo: https://github.com/vikasredd057-create/fsd_swiftride
echo ===============================================
pause
