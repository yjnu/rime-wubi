import os
import sys
import pickle
import colorama
from datetime import datetime
from colorama import Fore, Style
from zzutils import get_path, CONFIG

colorama.init(autoreset=True)

class WubiDictManager:
    def __init__(self):
        self.start_line = CONFIG.getint("wubi", "start_line", fallback=32)
        self.file_path = get_path("zh")
        self.head = []
        self.body = []
        self.tail = []
        self.res_division = {}
        self.total_num = 0

    def load_data(self):
        """加载文件并切分头部、主体和尾部"""
        print("读取词库...\n")
        if not os.path.exists(self.file_path):
            print(f"{Fore.RED}错误：找不到文件 {self.file_path}")
            sys.exit(1)
            
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        self.head = lines[:self.start_line]
        self.body = lines[self.start_line:-6]
        self.tail = lines[-6:]

    def process_body(self):
        """重写序号并生成索引映射"""
        print("开始重新编写序号及更新词库索引...\n")
        prev_code = ""
        num = 0

        for i, line in enumerate(self.body):
            try:
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    raise IndexError
                
                word, code = parts[0], parts[1]
                
                # 序号递增逻辑
                if code == prev_code:
                    num += 1
                else:
                    num = 1
                    prev_code = code
                
                # 更新当前行
                self.body[i] = f"{word}\t{code}\t{num}\n"
                
                # 记录索引 (1-2位编码且为该码第一个词)
                if len(code) <= 2 and num == 1:
                    self.res_division[code] = i

            except IndexError:
                print(f"{Fore.RED}[格式错误] 第 {self.start_line + i + 1} 行不符合标准！")
                print(f"内容: {line.strip()}")
                input("\n按回车键退出并检查文件...")
                sys.exit(1)
        
        self.total_num = len(self.body)

    def update_history(self):
        """更新尾部的历史 znum 记录"""
        current_tag = datetime.now().strftime("[%Y-%m]")
        new_entry = f"{self.total_num}{current_tag}\tznum\t1"
        
        # 过滤出非 znum 行和现有的 history
        other_tail = [l.strip() for l in self.tail if "znum" not in l]
        history = [l.strip() for l in self.tail if "znum" in l]

        # 更新或追加
        updated = False
        for i, record in enumerate(history):
            if current_tag in record:
                history[i] = new_entry
                updated = True
                break
        
        if not updated:
            history.append(new_entry)
        
        # 保持最后 6 条并合并
        history = history[-6:]
        self.tail = [l + "\n" for l in (other_tail + history)]

    def save(self):
        """保存词库文件和 pickle 索引"""
        # 保存主文件
        with open(self.file_path, "w", encoding="utf-8", newline='\n') as f:
            f.writelines(self.head + self.body + self.tail)

        # 保存索引
        idx_path = os.path.join(os.path.dirname(__file__), "wsdict_division.pkl")
        with open(idx_path, 'wb') as f:
            pickle.dump(self.res_division, f)
        
        self._print_stats()

    def _print_stats(self):
        size = os.path.getsize(self.file_path)
        readable_size = self.format_size(size)
        print(f"更新完成！\n")
        print(f"文件大小: {Fore.GREEN}{readable_size}{Style.RESET_ALL} 词条数: {Fore.GREEN}{self.total_num}{Style.RESET_ALL} \n")

    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"

if __name__ == "__main__":
    manager = WubiDictManager()
    manager.load_data()
    manager.process_body()
    manager.update_history()
    manager.save()
    input("Press Enter to exit...")