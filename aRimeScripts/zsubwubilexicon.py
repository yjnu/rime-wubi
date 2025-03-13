# 注意: 词库最后一定要空一行

import sys
from zzutils import detect_language, get_path, open_dict, get_active_window_exe


def subwubilex(word1, dicType):
    startline = 27
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    updated_vocab = []
    tmpnum = 0
    startnum = 0
    endnum = len(vocab_lines)
    found_match = False
    wubi_code = "zzzaaabbb"
    for line in vocab_lines:
        parts = line.strip().split("\t")
        if (parts[0] == word1 or wubi_code == parts[1]) and len(parts) >= 3:
            if startnum == 0 and not found_match:
                found_match = True
                startnum = tmpnum
                wubi_code = parts[1]
            else:
                updated_vocab.append(f"{parts[0]}\t{parts[1]}\t{int(parts[2])-1}\n")
        if found_match and parts[1] != wubi_code:
            endnum = tmpnum
            break
        tmpnum += 1

    if not found_match:
        print("\n\033[31mError:\033[0m phrase not found")
        sys.exit(1)
    
    # 重新写回文件
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + vocab_lines[:startnum] + updated_vocab + vocab_lines[endnum:])
    
    # print(f"startnum: {startnum}")
    # print(f"endnum: {endnum}")
    # print(updated_vocab)
    if get_active_window_exe() == "AutoHotkey64":
        print(f"deleted and sorted: {word1}")
    else:
        print(f"\nsubtracted and sorted: \033[32m{word1}\033[0m")

def subenlex(word1, dicType):
    startline = 18
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    updated_vocab = lines[startline:]
    isfound = False
    for item in updated_vocab:
        key, _ = item.split("\t")
        # if item.startswith(word1):
        if key == word1:
            updated_vocab.remove(item)
            isfound = True
            break

    if not isfound:
        print("\n\033[31mError:\033[0m English Word not found")
        sys.exit(1)
    
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + updated_vocab)
    
    if get_active_window_exe() == "AutoHotkey64":
        print(f"deleted and sorted: {word1}")
    else:
        print(f"\nsubtracted and sorted: \033[32m{word1}\033[0m") 

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    # 获取命令行参数
    if len(sys.argv) == 2:
        word1 = sys.argv[1]
    else:
        print("\nUsage: python zsubwubilexicon.py <word>")
        sys.exit(1)
    dicType = detect_language(word1)
    if dicType == "unknown":
        print("\nError: Unknown Parameter")
        sys.exit(1)
    elif dicType == "zh":
        subwubilex(word1, dicType)
    else:
        subenlex(word1, dicType)
