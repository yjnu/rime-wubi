@echo off
setlocal enabledelayedexpansion

rem 设置EmEditor路径和文件名
if "%COMPUTERNAME%"=="R5-2600X" (
    set EMEDITOR_PATH="E:\Program_Files\EmEditor\EmEditor.exe"
    set FILE_NAME="E:\Program_Files\RimeUserData\wubi.dict.yaml"
) else (
    set EMEDITOR_PATH="D:\Program_Files\EmEditor\EmEditor.exe"
    set FILE_NAME="D:\Program_Files\RimeUserData\wubi_user.dict.yaml"
)

rem 检查文件是否存在
if not exist "%FILE_NAME%" (
    echo 文件 %FILE_NAME% 不存在，请检查文件路径是否正确。
    pause
    exit /b
)

rem 使用EmEditor打开文件
"%EMEDITOR_PATH%" "%FILE_NAME%"

endlocal