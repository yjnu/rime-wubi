import sys
import os
import re
import pickle
import configparser
import ctypes
from ctypes import wintypes

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

def detect_language(language):
    """检测字符串的语言类型
    
    Args:
        language(str): 输入一个字符串。

    Returns:    
        str: 可能的值为 "zh"、"en"、"unknown"
    """
    if re.search(r'\d', language):
        return "number"
    elif re.search('[\u4e00-\u9fff]', language):
        return "zh"
    elif re.search('[a-zA-Z]', language):
        return "en"
    else:
        return "unknown"

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


def get_lua_path():
    """获取 rime 词库中 lua 文件路径与 Dropbox lua 备份路径
    Args:
        None

    Returns:
        list: lua 文件路径与 Dropbox lua 备份路径
    """

    dluapath = CONFIG.get('lua_path', 'd_lua_path')
    eluapath = CONFIG.get('lua_path', 'e_lua_path')
    edropluapath = CONFIG.get('lua_path', 'edrop_lua_path')
    fdropluapath = CONFIG.get('lua_path', 'fdrop_lua_path')
    
    name = os.environ.get("COMPUTERNAME")
    lua_paths = []
    if name == "R5-2600X":
        lua_paths.append(eluapath)
        lua_paths.append(fdropluapath)
    else:
        lua_paths.append(dluapath)
        lua_paths.append(edropluapath)
    return lua_paths

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