# 词库文件最后一定要空一行

import sys
import re
from zzutils import CONFIG, detect_language, get_path, open_dict, get_active_window_exe


def transenlex(word1, word2, word3):
    # 检测 word1 最后一个字符是不是 `
    word1 = word1[:-1] + " " if word1.endswith('`') else word1
    # 如果 word2 是 no 则无需翻译
    word2 = "" if word2 == "no" else word2

    old_entry = f"{word1}\t{word3}\n"
    new_entry = f"{word1}[{word2}]\t{word3}\n"
    startline = CONFIG.getint("start_line", "en")
    dict_path = get_path("en")
    lines = open_dict(dict_path)
    vocab_lines = lines[startline:]
    if old_entry in vocab_lines:
        # 如果词条完全相同，则删除词条
        vocab_lines.remove(old_entry)
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
        print("Successfully Translated")
    else:
        print("\n\033[32mSuccessfully Translated\033[0m")
    print(f"Word:    {word1}\n"
          f"Trans:   {word2}\n")

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) == 3:
        word1, word2 = sys.argv[1], sys.argv[2]
    else:
        print("\nOnly one usage change to the easy_en dictionary: \n" 
              "python ztransen.py <English> <Chinese>")
        sys.exit(1)
    dicType = detect_language(word1)
    if dicType == "en":
        word3 = word1.lower()
        word3 = ''.join(re.findall(r'[a-zA-Z]', word3))
        transenlex(word1, word2, word3)
    else:
        print(f"{dicType} -> Error language type")
        sys.exit(1)
        