@echo off

chcp 65001 > nul

setlocal enabledelayedexpansion

python "%~dp0zaddluafilter.py" %*

if errorlevel 1 (
    exit /b 1
)

echo.
echo Sync successfully

if "%COMPUTERNAME%"=="R5-2600X" (
    set "num=3"
) else (
    set "num=2"
)

set "INI_FILE=%~dp0config.ini"
set "lineCount=1"

for /f "usebackq delims=" %%a in ("%INI_FILE%") do (
    if !lineCount! equ !num! (
        for /f "tokens=2 delims== " %%b in ("%%a") do (
            set "dirPath=%%b"
        )
        goto :next
    )
    set /a lineCount+=1 
)
:next

SET "fullPath="

for /d %%i in ("%dirPath%\*") do (
    if not defined fullPath (
        set "fullPath=%%i\WeaselDeployer.exe"
    ) else (
        echo More than one folder found in %dirPath%
        exit /b
    )
)

if defined fullPath (
    echo.
    echo Deploying
    timeout /t 1 /nobreak
    %fullPath% /deploy
) else (
    echo No folder found in %dirPath%
    exit /b
)

echo.
echo Successfully added and redeployed

enlocal