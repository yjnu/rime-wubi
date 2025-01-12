import pickle

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
            f.write(f"{key}: {value}\n")

def write_pkl(file_path, wbdict):
    with open(file_path, 'wb') as f:
        pickle.dump(wbdict, f)

def write_txt(file_path, wdict):
    with open(file_path, 'w', encoding='utf-8') as f:
        for key, value in wdict.items():
            f.write(f"{key}\t{value}\n")


if __name__ == "__main__":
    wbdict = load_txt('f:/Dropbox/RimeSync/aRimeScripts/output.txt')
    write_pkl('f:/Dropbox/RimeSync/aRimeScripts/wsdict.pkl', wbdict)
    wdict = load_wsdict('f:/Dropbox/RimeSync/aRimeScripts/wsdict.pkl')
    word = '有'
    print(f"word: {wdict[word]}")
