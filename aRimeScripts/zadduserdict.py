# 词库文件最后一定要空一行

import sys
from zzutils import get_user_dict_path, open_dict, get_active_window_exe


def addWubiUserLex(word1, word2):
    has_hash_tag = '#' in word1
    new_entry = f"{word1}\t{word2}\n"
    
    dict_path = get_user_dict_path()
    lines = open_dict(dict_path)
    lines[-1] = lines[-1].rstrip('\n') + '\n'

    # 定位区间
    try:
        user_index = lines.index("## 自造词\n")
        hash_tag_index = lines.index("# no comment\n", user_index)
    except ValueError:
        print("Error: Dictionary headers not found!")
        sys.exit(1)

    # 确定操作区间
    start_mark = hash_tag_index if has_hash_tag else user_index
    end_mark = len(lines) if has_hash_tag else hash_tag_index-1

    # 整个文件中查找是否已存在该词条
    if new_entry in lines[start_mark:end_mark]:
        color_start = "" if get_active_window_exe() == "AutoHotkey64" else "\033[31m"
        color_end = "" if get_active_window_exe() == "AutoHotkey64" else "\033[0m"
        print(f"\nphrase: {color_start}{word1}{color_end} already exists, skipping...")
        sys.exit(1)

    current_section = lines[start_mark + 1 : end_mark]
    current_section.append(new_entry)
    
    # 排序 (按编码 word2 排序)
    current_section.sort(key=lambda x: x.split('\t')[1] if '\t' in x else x)

    # 重新拼接完整列表（确保不丢失 end_mark 之后的内容）
    if has_hash_tag:
        end_section = []
    else:
        end_section = ["\n"] + lines[hash_tag_index:]
    lines = lines[:start_mark + 1] + current_section + end_section

    # 保存
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines)
    
    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully Appended to wubi_user")
    else:
        print("\n\033[32mSuccessfully Appended to wubi_user\033[0m")
    print(f"\ncustom: {word1}\n"
          f"code:   {word2}\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) == 3:
        word1, word2 = sys.argv[1], sys.argv[2]
    else:
        print("\nOnly one usage to append custom words to the wubi_user dictionary:\n" 
              "python zadduserdict.py <Chinese Word> <Code>\n")
        sys.exit(1)
    addWubiUserLex(word1, word2)
