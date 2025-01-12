import sys
import os
import shutil

def get_path():
    name = os.environ.get("COMPUTERNAME")
    lua_paths = []
    if name == "R5-2600X":
        lua_paths.append("E:\\Program_Files\\RimeUserData\\lua\\wubi_character_filter.lua")
        lua_paths.append("F:\\Dropbox\\RimeSync\\lua\\wubi_character_filter.lua")
    else: 
        lua_paths.append("D:\\Program_Files\\RimeUserData\\lua\\wubi_character_filter.lua")
        lua_paths.append("E:\\Dropbox\\RimeSync\\lua\\wubi_character_filter.lua")
    return lua_paths

def add_entry_to_lua_file(lua_file, entry):
    # 读取文件内容
    with open(lua_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 在第七行插入新的一行, 确保文件前面有注释后, 插入位置依然在数组内
    lines.insert(6, f'    ["{entry}"] = true,\n')

    # 将修改后的内容写回文件
    with open(lua_file, 'w', encoding='utf-8', newline='\n') as file:
        file.writelines(lines)
    
    print(f"\nword: \033[32m{entry}\033[0m")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("用法: python add.py <汉字>")
        sys.exit(1)

    entry = sys.argv[1]
    lua_files = get_path()
    add_entry_to_lua_file(lua_files[0], entry)
    shutil.copy2(lua_files[0], lua_files[1])              # 手动备份

