@echo off

if "%COMPUTERNAME%"=="R5-2600X" (
    start /b "EmEditor" "E:\Program_Files\EmEditor\EmEditor.exe" "E:\Program_Files\RimeUserData\wubi_user.dict.yaml"
) else (
    start /b "EmEditor" "D:\Program_Files\EmEditor\EmEditor.exe" "D:\Program_Files\RimeUserData\wubi_user.dict.yaml"
)
