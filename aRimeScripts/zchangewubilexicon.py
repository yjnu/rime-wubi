import sys
import os
import re
import pickle

# 词库最后一定要空一行

def detect_language(string):
    if re.search(r'\d', string):
        return "number"
    elif re.search('[a-zA-Z]', string):
        return "en"
    elif re.search('[\u4e00-\u9fff]', string):
        return "zh"
    else:
        return "unknown"

def get_path(dicType):
    name = os.environ.get("COMPUTERNAME")
    if name == "R5-2600X":
        dict_path = "E:\\Program_Files\\RimeUserData\\wubi.dict.yaml"
    else: 
        dict_path = "D:\\Program_Files\\RimeUserData\\wubi.dict.yaml"
    if dicType == "en":
        dict_path = re.sub(r'wubi', 'easy_en', dict_path)        
    return dict_path

def open_dict(dict_path):
    with open(dict_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines

def load_wsdict(file_path):
    """从 Pickle 文件加载五笔编码字典"""
    with open(file_path, 'rb') as f:
        wsdict = pickle.load(f)
    return wsdict

def get_wubi_code(phrase: str):
    """根据输入的词组和五笔字典生成词组的编码"""
    # 获取脚本的运行路径
    script_path = os.path.abspath(__file__)
    # 获取脚本运行的目录
    wsdict_path = os.path.dirname(script_path)  + "\wsdict.pkl"
    length = len(phrase)
    wsdict = load_wsdict(wsdict_path)
    if length == 1:
        print("\n Please enter a phrase")
        sys.exit(1)
    if re.search('[a-zA-Z]', phrase) and length <= 3:
        if length == 2:
            print("\n Please enter a Chinese phrase")
        if length == 3:
            if phrase[2].isalpha() == True:
                print("\n Please enter a Chinese phrase")
                sys.exit(1)
    try:
        if length == 2:
            # 两个字，取每个字的前两个编码
            code = wsdict[phrase[0]][:2] + wsdict[phrase[1]][:2]
        elif length == 3:
            # 三个字，取前两个字第一个编码，最后一个字前两个编码
            code = wsdict[phrase[0]][:1] + wsdict[phrase[1]][:1] + wsdict[phrase[2]][:2]
        else:
            # 四个及以上字，取前三个字第一个编码，最后一个字第一个编码
            code = wsdict[phrase[0]][:1] + wsdict[phrase[1]][:1] + wsdict[phrase[2]][:1] + wsdict[phrase[-1]][:1]
    except KeyError as e:
        # 捕获 KeyError 异常，如果字典中没有对应的汉字编码
        missing_char = e.args[0]
        print(f"错误：'{missing_char}' 没有对应的五笔编码。")
        sys.exit(1)
    return code

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
    
    print("\n\033[32mSuccessfully Changed\033[0m\n"
          f"phrase: {word1}\n"
          f"code:   {word2}\n"
          f"weight: {word3}")



if __name__ == "__main__":
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