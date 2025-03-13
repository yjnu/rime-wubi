@echo off
setlocal enabledelayedexpansion

if "%COMPUTERNAME%"=="R5-2600X" (
    set EMEDITOR_PATH="E:\Program_Files\EmEditor\EmEditor.exe"
    set FILE_NAME="E:\Program_Files\RimeUserData\wubi.dict.yaml"
) else (
    set EMEDITOR_PATH="D:\Program_Files\EmEditor\EmEditor.exe"
    set FILE_NAME="D:\Program_Files\RimeUserData\wubi_user.dict.yaml"
)

if not exist "%FILE_NAME%" (
    echo %FILE_NAME% not found.
    pause
    exit /b
)

if not exist "%EMEDITOR_PATH%" (
    echo %EMEDITOR_PATH% not found.
    pause
    exit /b 
)

"%EMEDITOR_PATH%" "%FILE_NAME%"

endlocal