# 词库最后一定要空一行

import sys
from zzutils import detect_language, get_path, open_dict, get_wubi_code, get_active_window_exe


def rewubilex(word1, word2, dicType="zh"):
    startline = 27     
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    isfound = False
    for index, line in enumerate(vocab_lines):
        parts = line.strip().split("\t") 
        if parts[0] == word2 and len(parts) >= 3:
            isfound = True
            vocab_lines[index] = f"{word1}\t{parts[1]}\t{parts[2]}\n"
    if not isfound:
        print("\nError: The second parameter must be in the dictionary")
        sys.exit(1)

    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + vocab_lines)

    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully replaced")
    else: 
        print("\n\033[32mSuccessfully replaced\033[0m")
    print(f"destword:   {word1}\n"
          f"sourceword: {word2}")

def reenlex(word1, word2, dicType="en"):
    startline = 18      
    dict_path = get_path(dicType)
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    isfound = False
    for index, line in enumerate(vocab_lines):
        parts = line.strip().split("\t")
        if parts[0] == word2:
            isfound = True
            vocab_lines[index] = f"{word1}\t{parts[1]}\n"
    if not isfound:
        print("\nError: The second parameter must be in the dictionary")
        sys.exit(1)
    
    with open(dict_path, "w", encoding="utf-8", newline='\n') as file:
        file.writelines(lines[:startline] + vocab_lines)
    
    if get_active_window_exe() == "AutoHotkey64":
        print("Successfully replaced")
    else:
        print("\n\033[32mSuccessfully replaced\033[0m")
    print(f"destword:   {word1}\n"
          f"sourceword: {word2}")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    
    if len(sys.argv) == 3:
        word1, word2 = sys.argv[1], sys.argv[2]
    else:
        print("\nOnly one usage replaced to the wubi dictionary: \n" 
              "python zvocabulary.py <destword> <sourceword>")
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
            word3 = get_wubi_code(word1)
            word4 = get_wubi_code(word2)
            if word3 == word4:
                rewubilex(word1, word2)
            else:
                print("\nError: The two word must be the same code")
                sys.exit(1)
        else:
            print("\nError: The second parameter must be Chinese")
            sys.exit(1)
    else:
        word3 = word1.lower()
        if word1.lower() == word2.lower():
            reenlex(word1, word2)
        else:
            print("\nError: The two word must be the same lowercase word")
            sys.exit(1)
