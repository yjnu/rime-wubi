import sys
import os
import re
import pickle

# 词库最后一定要空一行

def detect_language(string):
    if re.search(r'\d', string):
        return "number"
    elif re.search('[\u4e00-\u9fff]', string):
        return "zh"
    elif re.search('[a-zA-Z]', string):
        return "en"
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
    
    print("\n\033[32mSuccessfully replaced\033[0m\n"
           f"destword:   {word1}\n"
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
    
    print("\n\033[32mSuccessfully replaced\033[0m\n"
          f"destword:   {word1}\n"
          f"sourceword: {word2}")

if __name__ == "__main__":
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
