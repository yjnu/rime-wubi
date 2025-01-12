@echo off

python "%~dp0zaddluafilter.py" %*

if errorlevel 1 (
    exit /b 1
)

echo.
echo Sync successfully

if "%COMPUTERNAME%"=="R5-2600X" (
     set "dirPath=E:\Program_Files\Rime"
) else (
     set "dirPath=D:\Program_Files\Rime"
)

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

rem ±àÂëÉèÖÃÎª UTF-8
rem chcp 65001 >nul
echo.
echo Successfully added and redeployed