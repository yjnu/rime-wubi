import sys
from zzutils import get_active_window_exe

def print_help():
    # 定义颜色代码
    if get_active_window_exe() == "AutoHotkey64":
        GREEN = ""
        RESET = ""
    else:
        GREEN = "\033[32m"
        RESET = "\033[0m"
    
    print("\n" + f"{GREEN}eeadd{RESET} 添加词组")
    print(f"用法1: eeadd <词组> <释义>")
    print(f"用法2: eeadd <词组>")
    
    print("\n" + f"{GREEN}eemv{RESET} 改变词组候选位置")
    print(f"用法1: eemv <词组> <候选位>")
    print(f"用法2: eemv <词组>")
    
    print("\n" + f"{GREEN}eere{RESET} 替换词组")
    print(f"用法: eere <目标词组> <原词组>")
    
    print("\n" + f"{GREEN}eedel{RESET} 删除词组")
    print(f"用法: eedel <词组>")

    print("\n" + f"{GREEN}eelua{RESET} 添加生僻字")
    print(f"用法: eelua <字> <可选:注音>")
    
    print("\n---无参命令---\n" 
          f"{GREEN}eedep{RESET} 部署\n"
          f"{GREEN}eesync{RESET} 同步\n")

if __name__ == "__main__":
    # 设置标准输出编码为 UTF-8
    sys.stdout.reconfigure(encoding='utf-8')
    print_help()