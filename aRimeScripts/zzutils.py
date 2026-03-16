import sys
import os
import re
import pickle
import configparser
import ctypes
from ctypes import wintypes

# 读取 config.ini 配置文件
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, 'config.ini')
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH, encoding='utf-8')

# def get_config():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     config_file_path = os.path.join(script_dir, 'config.ini')
#     script_config = configparser.ConfigParser()
#     script_config.read(config_file_path, encoding='utf-8')
#     return script_config

def detect_language(text):
    """检测字符串的语言类型
    
    Args:
        language(str): 输入一个字符串。

    Returns:    
        str: 值为 "unknown", "number", "zh" 或 "en"
    """
    if not text:
        return "unknown"
    if re.match(r'^[0-9]+$', text):
        return "number"
    for char in text:
        if ord(char) > 127:  # ASCII范围是0-127
            return 'zh'
    return 'en'

def get_path(dicType):
    """获取 rime 词库文件路径
    
    Args:
        dicType(str): 输入一个字符串，可能的值为 "zh"、"en"

    Returns:
        str: 字典文件路径
    """
    
    ddictpath = CONFIG.get("dict_path", "d_dict_path")
    edictpath = CONFIG.get("dict_path", "e_dict_path")

    name = os.environ.get("COMPUTERNAME")
    if name == "R5-2600X":
        dict_path = edictpath
    else: 
        dict_path = ddictpath
    if dicType == "en":
        dict_path = re.sub(r'wubi', 'easy_en', dict_path)        
    return dict_path

def get_user_dict_path():
    """获取 rime 用户词库文件路径
    
    Args:
        None

    Returns:
        str: 用户词库文件路径
    """
    dudictpath = CONFIG.get("udict_path", "d_udict_path")
    eudictpath = CONFIG.get("udict_path", "e_udict_path")
    name = os.environ.get("COMPUTERNAME")
    if name == "R5-2600X":
        user_dict_path = eudictpath
    else:
        user_dict_path = dudictpath
    return user_dict_path

def get_pinyin_dict_path():
    """获取 rime 拼音词库文件路径
    
    Args:
        None

    Returns:
        str: 拼音词库文件路径
    """
    dpydictpath = CONFIG.get("pydict_path", "d_pydict_path")
    epydictpath = CONFIG.get("pydict_path", "e_pydict_path")
    name = os.environ.get("COMPUTERNAME")
    if name == "R5-2600X":
        pinyin_dict_path = epydictpath
    else:
        pinyin_dict_path = dpydictpath
    return pinyin_dict_path

def open_dict(dict_path):
    """打开 rime 词库文件

    Args:
        dict_path(str): 词库文件路径

    Returns:
        list: 词库文件内容
    """
    with open(dict_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines

def load_wsdict(file_path):
    """从 Pickle 文件加载单字五笔编码字典
    Args:
        file_path(str): 单字五笔编码字典文件路径

    Returns:
        dict: 单字五笔编码字典
    """
    with open(file_path, 'rb') as f:
        wsdict = pickle.load(f)
    return wsdict

def get_wubi_code(phrase: str):
    """输入词组，返回五笔编码

    Args:
        phrase(str): 词组

    Returns:
        str: 五笔编码
    """
    # 获取脚本的运行路径
    script_path = os.path.abspath(__file__)
    # 获取脚本运行的目录
    wsdict_path = os.path.dirname(script_path)  + "\\wsdict.pkl"
    
    # 完整的CJK字符范围 + 英文字母 + 数字
    # CJK字符区域：
    # \u3400-\u4dbf: CJK扩展A
    # \u4e00-\u9fff: CJK基本区
    # \U00020000-\U0002a6df: CJK扩展B
    # \U0002a700-\U0002b73f: CJK扩展C
    # \U0002b740-\U0002b81f: CJK扩展D
    # \U0002b820-\U0002ceaf: CJK扩展E
    # \U0002ceb0-\U0002ebef: CJK扩展F
    # \U00030000-\U0003134f: CJK扩展G
    # a-zA-Z: 英文字母
    # 0-9: 数字
    pattern = r'[\u3400-\u4dbf\u4e00-\u9fff\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\U0002ceb0-\U0002ebef\U00030000-\U0003134fa-zA-Z0-9]'
    chars = re.findall(pattern, phrase)
    phrase = ''.join(chars)
    length = len(phrase)
    wsdict = load_wsdict(wsdict_path)
    # if length == 1:
    #     print("\n Please enter a phrase")
    #     sys.exit(1)
    # if re.search('[a-zA-Z]', phrase) and length <= 3:
    #     if length == 2:
    #         print("\n Please enter a Chinese phrase")
    #     if length == 3:
    #         if phrase[2].isalpha() == True:
    #             print("\n Please enter a Chinese phrase")
    #             sys.exit(1)
    try:
        if length == 1:
            # 一个字, 取其全部编码
            code = wsdict[phrase]
        elif length == 2:
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


def get_lua_path():
    """获取 rime 词库中 lua 文件路径
    Args:
        None

    Returns:
        list: lua 文件路径
    """
    
    name = os.environ.get("COMPUTERNAME")
    if name == "R5-2600X":
        return CONFIG.get('lua_path', 'e_lua_path')
    else:
        return CONFIG.get('lua_path', 'd_lua_path')

def get_active_window_exe():
    """获取当前活动窗口的exe文件名
    Args:
        None
        
    Returns:
        str: exe文件名
    """
    # 定义Windows API函数
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    # 获取前台窗口句柄
    hwnd = user32.GetForegroundWindow()

    # 获取进程ID
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    # 获取进程句柄
    PROCESS_QUERY_INFORMATION = 0x0400
    h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, pid)

    # 获取可执行文件路径
    if h_process:
        exe_path = wintypes.WCHAR * 4096  # 定义缓冲区
        buffer = exe_path()
        size = wintypes.DWORD(4096)
        if kernel32.QueryFullProcessImageNameW(h_process, 0, buffer, ctypes.byref(size)):
            kernel32.CloseHandle(h_process)
            exe_name = os.path.basename(buffer.value)
            return os.path.splitext(exe_name)[0]
        kernel32.CloseHandle(h_process)
    return "无法获取路径"

def remove_bracket(cand_text):
    '''
        从字符串中移除成对方括号及其中的内容
        
        Args:
            str: 输入字符串
        
        Returns:
            str: 移除方括号及其内容后的字符串 或 原字符串
    '''

    # 检查是否有配对的[], 且以 ] 结尾
    if cand_text.endswith(']') and '[' in cand_text:
        first_left = cand_text.find('[')
        # 确保 [ 不是第一个字符
        if first_left != 0:
            return cand_text[:first_left]
        else:
            return cand_text
    else:
        return cand_text

def pre_division(word_list):
    """
    对五笔词库进行预处理, 得到前两个英文字母第(a-y)第一次出现的位置, 并将索引保存为字典文件

    param : list
        五笔词库列表
    Returns: None
    """
    res = {}
    for index, item in enumerate(word_list):
        hanzi, code, num = item.split('\t')
        code_length = len(code)
        if (code_length == 2 or code_length == 1)  and num == "1\n":
            res[code] = index
    
    script_path = os.path.abspath(__file__)
    pre_division_path = os.path.dirname(script_path)  + "\\wsdict_division.pkl"
    with open(pre_division_path, 'wb') as file:
        pickle.dump(res, file)

def get_letter_position(letter):
    """
    获取前两个英文字母在五笔词库中第一次出现的位置索引

    param1 : str
        两个英文字母
    Returns: num
        字母在词库中的索引位置, 如果字母不存在则返回0
    """
    script_path = os.path.abspath(__file__)
    pre_division_path = os.path.dirname(script_path)  + "\\wsdict_division.pkl"
    with open(pre_division_path, 'rb') as file:
        res = pickle.load(file)
    letter_position = res.get(letter.lower(), 0)
    if letter_position == 0:
        first_char = letter[0]
        return res.get(first_char, 0)
    else:
        return letter_position
    