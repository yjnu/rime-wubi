@echo off
setlocal enabledelayedexpansion

rem ����EmEditor·�����ļ���
if "%COMPUTERNAME%"=="R5-2600X" (
    set EMEDITOR_PATH="E:\Program_Files\EmEditor\EmEditor.exe"
    set FILE_NAME="E:\Program_Files\RimeUserData\wubi.dict.yaml"
) else (
    set EMEDITOR_PATH="D:\Program_Files\EmEditor\EmEditor.exe"
    set FILE_NAME="D:\Program_Files\RimeUserData\wubi_user.dict.yaml"
)

rem ����ļ��Ƿ����
if not exist "%FILE_NAME%" (
    echo �ļ� %FILE_NAME% �����ڣ������ļ�·���Ƿ���ȷ��
    pause
    exit /b
)

rem ʹ��EmEditor���ļ�
"%EMEDITOR_PATH%" "%FILE_NAME%"

endlocal