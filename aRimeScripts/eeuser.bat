@echo off

:: 切换控制台代码页为 UTF-8
chcp 65001 > nul

setlocal enabledelayedexpansion

python "%~dp0zadduserdict.py" %*

if errorlevel 1 (
    exit /b 1
)

set "INI_FILE=%~dp0config.ini"
set "SECTION=rime_path"

:: 标记是否进入指定节
set "in_section=false"

:: 空格是因为 ini 文件的键有空格
if "%COMPUTERNAME%"=="R5-2600X" (
    set "rimepath=e_rime_path "
) else (
    set "rimepath=d_rime_path "
)

:: 逐行读取 INI 文件, 设置 dirPath
for /f "usebackq delims=" %%a in ("%INI_FILE%") do (
    set "line=%%a"
    rem 去除行首和行尾的空格
    for /f "tokens=*" %%b in ("!line!") do set "line=%%b"

    rem 检查是否为节开始
    if "!line:~0,1!"=="[" (
        set "current_section=!line:~1,-1!"
        if "!current_section!"=="%SECTION%" (
            set "in_section=true"
        ) else (
            set "in_section=false"
        )
    ) else if "!in_section!"=="true" (
        rem 检查是否为键值对
        if "!line:~0,1!" neq ";" (
            for /f "tokens=1,2 delims==" %%c in ("!line!") do (
                set "key=%%c"
                set "value=%%d"
                if defined key if defined value (
                    for /f "tokens=*" %%i in ("!key!") do set "key=%%i"
                    for /f "tokens=*" %%i in ("!value!") do set "value=%%i"
                    if "!key!"=="%rimepath%" (
                       set "dirPath=!value!"
                    )
                )
            )
        )
    )
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
    @REM echo.
    @REM echo Deploying and syncing
    @REM timeout /t 1 /nobreak
    %fullPath% /deploy
    @REM %fullPath% /sync
) else (
    echo No folder found in %dirPath%
    exit /b
)

@REM echo.
@REM echo Successfully added, redeployed, and synced

endlocal