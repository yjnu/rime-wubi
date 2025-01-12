@echo off

python "%~dp0zrewubilexicon.py" %*

if errorlevel 1 (
    exit /b 1
)

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
    echo Deploying and syncing
    timeout /t 1 /nobreak
    %fullPath% /deploy
    %fullPath% /sync
) else (
    echo No folder found in %dirPath%
    exit /b
)

echo.
echo Successfully replaced, redeployed, and synced