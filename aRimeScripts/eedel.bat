@echo off

chcp 65001 > nul

setlocal enabledelayedexpansion

python "%~dp0zsubwubilexicon.py" %*

if errorlevel 1 (
    exit /b 1
)

endlocal