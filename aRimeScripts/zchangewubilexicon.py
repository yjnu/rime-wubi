# 词库最后一定要空一行

import sys
from zzutils import detect_language, get_path, open_dict, get_wubi_code, get_active_window_exe


def changewubilex(word1, word2, word3, dicType):
    startline = 27
    new_entry = f"{word1}\t{word2}\t{word3}\n"       
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    updated_vocab = []
    startnum = 0
    endnum = 0
    isfound = False
    count = 1
    # tmp = 0
    for line in vocab_lines:
        parts = line.strip().split("\t")
        # tmp += 1 
        if parts[1] < word2:
            pass
        elif parts[1] == word2:# and len(parts) >= 3:
            if parts[0] == word1:
                if int(parts[2]) == int(word3):
                    print("\nError: The sorting remains unchanged ")
                    sys.exit(1)
                else:
                    updated_vocab.append(new_entry)
            else:
                if count == int(word3) and int(parts[2]) >= int(word3): 
                    count = int(word3) + 1
                updated_vocab.append(f"{parts[0]}\t{parts[1]}\t{count}\n")
                count += 1
            if not isfound:
                isfound = True
                startnum = endnum

        elif parts[1] > word2 and not isfound:
            # print(tmp)
            print("\n\033[31mError:\033[0m The word is not in the dictionary. ")
            sys.exit(1)
        else:
            break
        endnum += 1
    # 排序
    print(updated_vocab)
    updated_vocab.sort(key=lambda x: (x.split("\t")[2]))
    count = 0
    for i, line in enumerate(updated_vocab):
        count += 1
        w1, w2, w3 = line.strip().split("\t")
        if w1 == word1: 
            word3 == w3
        updated_vocab[i] = f"{w1}\t{w2}\t{count}\n"
        
    # 重新写回文件
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + vocab_lines[:startnum] + updated_vocab + vocab_lines[endnum:])

    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully Changed")
    else:
        print("\n\033[32mSuccessfully Changed\033[0m")
    print(f"phrase: {word1}\n"
          f"code:   {word2}\n"
          f"weight: {word3}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) == 3:
        word1, word3 = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        word1 = sys.argv[1]
        word3 = "1"
    else:
        print("\nTwo usages changed to the wubi dictionary: \n" 
              "python zvocabulary.py <Chinese Word> <Weight>\n"
              "python zvocabulary.py <Chinese Word>")
        sys.exit(1)
    dicType = detect_language(word1)
    if dicType == "number":
        print("\nError: Numbers cannot be changed to dictionaries")
        sys.exit(1)
    elif dicType == "unknown":
        print("\nError: Unknown Parameter")
        sys.exit(1)
    elif dicType == "zh":
        if detect_language(word3) == "number":
            word2 = get_wubi_code(word1)
            print(f"\n 输入词组： {word1} {word2} {word3}")
            changewubilex(word1, word2, word3, dicType)
        else:
            print("\nError: the second parameter is not number")
            sys.exit(1)
    else:
       print("\nError: English is not supported") 
       sys.exit(1)