import pickle
import os

def load_wsdict(file_path):
    """从 Pickle 文件加载五笔编码字典"""
    with open(file_path, 'rb') as f:
        wsdict = pickle.load(f)
    return wsdict

def load_txt(file_path):
    """从 Pickle 文件加载五笔编码字典"""
    wbdict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            key, value = line.strip().split('\t')  # 按制表符分割
            wbdict[key] = value
    return wbdict

def write_txt(file_path, wdict):
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, value in wdict.items():
            f.write(f"{key}\t{value}\n")

def write_pkl(file_path, wbdict):
    with open(file_path, 'wb') as f:
        pickle.dump(wbdict, f)

if __name__ == "__main__":
    """ 
       txt 是生成 txt
       pkl 是生成 pkl
       用法: 先生成 output.txt 修改后再生成 pkl 
    """
    switch = "txt"
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if switch == "pkl":
        wbdict = load_txt(os.path.join(current_dir, 'output.txt'))
        write_pkl(os.path.join(current_dir, 'wsdict.pkl'), wbdict)
        print("pkl 已更新")
    elif switch == "txt":
        wdict = load_wsdict(os.path.join(current_dir, 'wsdict.pkl'))
        write_txt(os.path.join(current_dir, 'output.txt'), wdict)
        print("txt 已生成")
        
