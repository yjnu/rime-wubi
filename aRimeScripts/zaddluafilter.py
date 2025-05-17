import sys
import shutil
from zzutils import get_lua_path, get_active_window_exe

def add_entry_to_lua_file(lua_file, entry, zhuyin=None):
    with open(lua_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if zhuyin is None:
        for i, line in enumerate(lines):
            if f'local hanzi_set' in line:
                serial_num = i
                break
        lines.insert(serial_num+1, f'    ["{entry}"] = true,\n')
    else:
        for i, line in enumerate(lines):
            if f'local error_prone_pronunciations' in line:
                serial_num = i
                break
        lines.insert(serial_num+1, f'    ["{entry}"] = {{comment = "{zhuyin}"}},\n')

    with open(lua_file, 'w', encoding='utf-8', newline='\n') as file:
        file.writelines(lines)
    
    if get_active_window_exe() == "AutoHotkey64":
        if zhuyin is None:
            print(f"word: {entry}")
        else:
            print(f"word: {entry}\n注音: {zhuyin}")
    else:
        if zhuyin is None:
            print(f"\nword: \033[32m{entry}\033[0m")
        else:
            print(f"\nword: \033[32m{entry}\033[0m\n注音: \033[32m{zhuyin}\033[0m")


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) == 3:    
        zhuyin = sys.argv[2]
    elif len(sys.argv) != 2:
        print("用法: python zaddluafilter.py <汉字> <可选:注音>")
        sys.exit(1)

    entry = sys.argv[1]
    
    lua_files = get_lua_path()
    if len(sys.argv) == 2:
        add_entry_to_lua_file(lua_files[0], entry)
    else:
        add_entry_to_lua_file(lua_files[0], entry, zhuyin)

    shutil.copy2(lua_files[0], lua_files[1])              # 手动备份

