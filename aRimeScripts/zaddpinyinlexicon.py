# 词库文件最后一定要空一行

import sys
from zzutils import get_pinyin_dict_path, open_dict, get_active_window_exe


def addpinyinlex(word1, word2, word3="1"):
    new_entry = f"{word1}\t{word2}\t{word3}\n"
    dict_path = get_pinyin_dict_path()
    lines = open_dict(dict_path)
    lines.append(new_entry)

    # lines.sort(key=lambda x: x.split('\t')[1])
    
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines)
    
    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully Appended to pinyin_simp")
    else:
        print("\n\033[32mSuccessfully Appended to pinyin_simp\033[0m")
    print(f"\ncustom: {word1}\n"
          f"code:   {word2}\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) == 3:
        word1, word2 = sys.argv[1], sys.argv[2]
        word3 = "1"
    elif len(sys.argv) == 4:
        word1, word2, word3 = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        print("\nOnly one usage to append custom words to the wubi_user dictionary:\n" 
              "python zaddpinyindict.py <Chinese Word> <Code>\n"
              "python zaddpinyindict.py <Chinese Word> <Code> <Weight>\n")
        sys.exit(1)
    addpinyinlex(word1, word2, word3)


