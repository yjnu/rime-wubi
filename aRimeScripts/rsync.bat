@echo off

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
        echo More than one folder found in %dirPath%.
        exit /b
    )
)

if defined fullPath (
    %fullPath% /sync
) else (
    echo No folder found in %dirPath%
)

rem Êä³ö¿ÕÐÐ echo.
echo.
echo User configuration is being synchronized