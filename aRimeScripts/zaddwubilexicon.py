# 词库文件最后一定要空一行

import sys
import re
from zzutils import CONFIG, detect_language, get_path, open_dict, get_wubi_code, get_active_window_exe, pre_division, get_letter_position
from ztransen import transenlex


def remake_division():
    startline = CONFIG.getint("start_line", "wubi")
    dict_path = get_path("zh")
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    pre_division(vocab_lines)
    print("Remake division done")

def addwubilex(word1, word2, word3, dicType):
    startline = CONFIG.getint("start_line", "wubi")
    new_entry = f"{word1}\t{word2}\t{word3}"       
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    updated_vocab = []
    inserted = False
    woldlist = []
    match_index = get_letter_position(word2[:2])
    endnum = match_index
    changed_wordlist = []
    for line in vocab_lines[match_index:]:
        parts = line.strip().split("\t")
        # print(parts)  # 调试用 
        if parts[1] == word2 and len(parts) >= 3:
            if parts[0] == word1:
                # 如果新词条完全相同，直接跳过添加
                print(f"\nphrase: {word1} already exists, skipping adding")
                if get_active_window_exe() == "AutoHotkey64":
                    print(f"code:   {word2}\n")   
                else:    
                    print(f"code:   \033[31m{word2}\033[0m\n")
                sys.exit(1)
            else:
                # 如果编码相同，但词条不同，增加词频
                if int(parts[2]) < int(word3):
                    updated_vocab.append(line)
                    changed_wordlist.append(parts[0])
                elif int(parts[2]) == int(word3):
                    count = int(parts[2]) + 1
                    updated_vocab.append(f"{new_entry}\n")
                    updated_vocab.append(f"{parts[0]}\t{parts[1]}\t{count}\n")
                    changed_wordlist.append(word1)
                    changed_wordlist.append(parts[0])
                    inserted = True
                else:
                    count = int(parts[2]) + 1
                    updated_vocab.append(f"{parts[0]}\t{parts[1]}\t{count}\n")
                    changed_wordlist.append(parts[0])
        else:
            if parts[1] > word2:
                if not inserted:
                    if updated_vocab and updated_vocab[-1].strip().split("\t")[1] == word2:
                        count = int(updated_vocab[-1].strip().split("\t")[2]) + 1
                        updated_vocab.append(f"{word1}\t{word2}\t{count}\n")
                        changed_wordlist.append(word1)
                        word3 = count
                    else:
                        updated_vocab.append(f"{word1}\t{word2}\t1\n")
                        changed_wordlist.append(word1)
                        word3 = 1
                    inserted = True
                break
            updated_vocab.append(line)
        endnum += 1
    
    # 如果加的词条在最后,那么需要判断是否加上
    if not inserted:
        if updated_vocab[-1].strip().split("\t")[1] == word2:
            count = int(updated_vocab[-1].strip().split("\t")[2]) + 1
        else:
            count = 1
        updated_vocab.append(f"{word1}\t{word2}\t{count}\n")
        changed_wordlist.append(word1)
        word3 = count

    # 重新写回文件
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + vocab_lines[:match_index] + updated_vocab + vocab_lines[endnum:])
    
    # print(f"endnum: {endnum}")
    # print(updated_vocab)
    # print("中断后",vocab_lines[endnum:])
    
    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully Added")
    else:
        print("\n\033[32mSuccessfully Added\033[0m")
    
    print(f"phrase: {word1}\n"
          f"code:   {word2}\n"
          f"weight: {word3}\n"
          f"dict:   {dicType}\n")

    print(f"changed wordlist: {changed_wordlist}\n")

def addenlex(word1, word2, dicType):
    # 检测 word1 最后一个字符是不是 `
    # word1 = word1[:-1] if word1.endswith('`') else word1 + " "
    word1 = word1[:-1] + " " if word1.endswith('`') else word1
    new_entry = f"{word1}\t{word2}\n"
    startline = CONFIG.getint("start_line", "en")
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    if new_entry in vocab_lines:
        # 如果新词条完全相同，直接跳过添加
        if get_active_window_exe() == "AutoHotkey64":
            print(f"\nphrase: {word1} already exists, skipping adding\n"
                    f"code:   {word2}\n")
        else:    
            print(f"\nphrase: \033[31m{word1}\033[0m already exists, skipping adding\n"
                    f"code:   \033[31m{word2}\033[0m\n")
        sys.exit(1)
    vocab_lines.append(new_entry)
    # 按照第一个单词的字母顺序升序排序
    u_vocab_lines = list(set(vocab_lines))
    
    # 按字母顺序排序
    # u_vocab_lines.sort(key=lambda x: x.split("\t")[1])
    # 按大小写排, 再按字母顺序排序
    u_vocab_lines.sort(key=lambda line: (line.split("\t")[0].islower(), line.split("\t")[0].lower()))
    
    updated_lines = lines[:startline] + u_vocab_lines
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(updated_lines)
    
    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully Added")
    else:
        print("\n\033[32mSuccessfully Added\033[0m")
    print(f"word: {word1}\n"
          f"code: {word2}\n"
          f"dict: {dicType}\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) == 4:
        word1, word2, word3 = sys.argv[1], sys.argv[2], sys.argv[3]
    elif len(sys.argv) == 3:
        word1, word2 = sys.argv[1], sys.argv[2]
        word3 = "1"
    elif len(sys.argv) == 2:
        word1 = word2 = sys.argv[1]
        word3 = "1"
        if word1.lower() == 'r':
            # 重新索引 wubi 编码
            remake_division()
            sys.exit(1)
    else:
        print("\nFour usages added to the wubi dictionary: \n" 
              "python zvocabulary.py <Chinese Word> <Code> <Weight>\n"
              "python zvocabulary.py <Chinese or English> <Code>\n"
              "python zvocabulary.py <Chinese> <Weight>\n"
              "python zvocabulary.py <English>")
        sys.exit(1)
    dicType = detect_language(word1)
    if dicType == "zh":
        if detect_language(word2) == "zh":
            word2 = get_wubi_code(word2)
        elif detect_language(word2) == "number":
            word3 = word2
            word2 = get_wubi_code(word1)
        addwubilex(word1, word2, word3, dicType)
    elif dicType == "en":
        word4 = word2.lower()
        word4 = ''.join(re.findall(r'[a-zA-Z]', word4))
        # 加个判断, 如果 word2 长度大于 Word1, 真接调整用 eeen 
        if len(word4) > len(word1):
            word5 = word1.lower()
            word5 = ''.join(re.findall(r'[a-zA-Z]', word5))
            transenlex(word1, word2, word5)
            # print(f"Warning: {word2} is longer than {word1}, maybe you want to use eeen instead")
            # sys.exit(1)
        else:
            addenlex(word1, word4, dicType)
    else:
        print(f"{dicType} -> Error: Unknown language type")
        sys.exit(1)