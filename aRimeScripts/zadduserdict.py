# 词库文件最后一定要空一行

import sys
from zzutils import get_user_dict_path, open_dict, get_active_window_exe


def addwubilex(word1, word2):
    new_entry = f"{word1}\t{word2}\n"
    dict_path = get_user_dict_path()
    lines = open_dict(dict_path)
    if new_entry in lines:
        # 如果新词条完全相同，直接跳过添加
        if get_active_window_exe() == "AutoHotkey64":
            print(f"\nphrase: {word1} already exists, skipping adding\n"
                    f"code:   {word2}\n")
        else:    
            print(f"\nphrase: \033[31m{word1}\033[0m already exists, skipping adding\n"
                    f"code:   \033[31m{word2}\033[0m\n")
        sys.exit(1)
    lines.append(new_entry)

    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines)
    
    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully Added")
    else:
        print("\n\033[32mSuccessfully Added\033[0m")
    print(f"word: {word1}\n"
          f"code: {word2}\n"
          f"dict: user\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) == 3:
        word1, word2 = sys.argv[1], sys.argv[2]
    else:
        print("\nFour usages added to the wubi_user dictionary: \n" 
              "python zadduserdict.py <Chinese Word> <Code>")
        sys.exit(1)
    addwubilex(word1, word2)
