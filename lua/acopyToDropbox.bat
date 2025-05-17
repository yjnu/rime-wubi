@echo off

chcp 65001 > nul

if "%COMPUTERNAME%"=="R5-2600X" (
    set "target_dir=F:\Dropbox\RimeSync\lua"
) else (
    set "target_dir=E:\Dropbox\RimeSync\lua"
)

echo 电脑名: %COMPUTERNAME%
echo 目标目录: %target_dir%

echo.
echo 正在复制 acopyToDropbox.bat
copy /Y "acopyToDropbox.bat" "%target_dir%\acopyToDropbox.bat"
echo 正在复制 character_filter
copy /Y "character_filter.lua" "%target_dir%\character_filter.lua"
echo 正在复制 date_translator
copy /Y "date_translator.lua" "%target_dir%\date_translator.lua"
echo 正在复制 disable_soft_cursor
copy /Y "disable_soft_cursor.lua" "%target_dir%\disable_soft_cursor.lua"
echo 正在复制 force_gc
copy /Y "force_gc.lua" "%target_dir%\force_gc.lua"
echo 正在复制 helper
copy /Y "helper.lua" "%target_dir%\helper.lua"
echo 正在复制 lunar
copy /Y "lunar.lua" "%target_dir%\lunar.lua"
echo 正在复制 only_three_candidates
copy /Y "only_three_candidates.lua" "%target_dir%\only_three_candidates.lua"
echo 正在复制 unicode
copy /Y "unicode.lua" "%target_dir%\unicode.lua"
echo 正在复制 xnumber
copy /Y "xnumber.lua" "%target_dir%\xnumber.lua"
echo.
echo 复制完成



pause

