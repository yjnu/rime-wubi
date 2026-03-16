@echo off

:: 切换控制台代码页为 UTF-8
chcp 65001 > nul

setlocal enabledelayedexpansion

python "%~dp0zadduserdict.py" %*

if errorlevel 1 (
    exit /b 1
)

endlocal