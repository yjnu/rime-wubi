@echo off

chcp 65001 > nul

setlocal enabledelayedexpansion

python "%~dp0zaddluafilter.py" %*

if errorlevel 1 (
    exit /b 1
)

endlocal