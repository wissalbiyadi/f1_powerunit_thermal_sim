@echo off
title F1 Thermal Control System Toolkit

:menu
echo ================================
echo       F1 Cooling Toolkit
echo ================================
echo [1] Run Simulation (main.py)
echo [2] Launch GUI Dashboard
echo [3] Run Tests
echo [4] View Coverage Report
echo [5] Analyze Log
echo [6] Clean Logs ^& Reports
echo [0] Exit
echo.

set /p choice="Choose an option: "

if "%choice%"=="1" python main.py
if "%choice%"=="2" python ui/dashboard.py
if "%choice%"=="3" pytest --cov=core tests/
if "%choice%"=="4" (
    coverage html
    start htmlcov\index.html
)
if "%choice%"=="5" python scripts/analyze_log.py
if "%choice%"=="6" (
    del /Q /F data\*.csv
    del /Q /F htmlcov\*.*
)
if "%choice%"=="0" exit

pause
cls
goto menu

