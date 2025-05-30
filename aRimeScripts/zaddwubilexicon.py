# 词库文件最后一定要空一行

import sys
from zzutils import detect_language, get_path, open_dict, get_wubi_code, get_active_window_exe


def addwubilex(word1, word2, word3, dicType):
    startline = 27
    new_entry = f"{word1}\t{word2}\t{word3}"       
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    updated_vocab = []
    endnum = 0
    inserted = False
    for line in vocab_lines:
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
                elif int(parts[2]) == int(word3):
                    count = int(parts[2]) + 1
                    updated_vocab.append(f"{new_entry}\n")
                    updated_vocab.append(f"{parts[0]}\t{parts[1]}\t{count}\n")
                    inserted = True
                else:
                    count = int(parts[2]) + 1
                    updated_vocab.append(f"{parts[0]}\t{parts[1]}\t{count}\n")
        else:
            if parts[1] > word2 and not inserted:
                if updated_vocab and updated_vocab[-1].strip().split("\t")[1] == word2:
                    count = int(updated_vocab[-1].strip().split("\t")[2]) + 1
                    updated_vocab.append(f"{word1}\t{word2}\t{count}\n")
                    word3 = count
                else:
                    updated_vocab.append(f"{word1}\t{word2}\t1\n")
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
        word3 = count

    # 重新写回文件
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + updated_vocab + vocab_lines[endnum:])
    
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

def addenlex(word1, word2, dicType):
    new_entry = f"{word1}\t{word2}"
    startline = 18      
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    new_entry = new_entry+"\n"
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
    u_vocab_lines.sort(key=lambda x: x.split("\t")[1])
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
    else:
        print("\nFour usages added to the wubi dictionary: \n" 
              "python zvocabulary.py <Chinese Word> <Code> <Weight>\n"
              "python zvocabulary.py <Chinese or English> <Code>\n"
              "python zvocabulary.py <Chinese> <Weight>\n"
              "python zvocabulary.py <English>")
        sys.exit(1)
    dicType = detect_language(word1)
    if dicType == "number":
        print("\nError: Numbers cannot be added to dictionaries")
        sys.exit(1)
    elif dicType == "unknown":
        print("\nError: Unknown Parameter")
        sys.exit(1)
    elif dicType == "zh":
        if detect_language(word2) == "zh":
            word2 = get_wubi_code(word2)
        elif detect_language(word2) == "number":
            word3 = word2
            word2 = get_wubi_code(word1)
        addwubilex(word1, word2, word3, dicType)
    else:
        word2 = word2.lower()
        if detect_language(word2) == "zh" or word1.lower() != word2:
            print("\nError: the second parameter is incorrect")
            sys.exit(1)
        else: 
            if detect_language(word2) == "number":
                word2 = word1.lower()
            else:
                word2 = word2.lower()
            addenlex(word1, word2, dicType)
