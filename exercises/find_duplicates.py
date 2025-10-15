import hashlib
from pathlib import Path
from collections import defaultdict

def find_duplicates_basic(directory):
    hash_dict = defaultdict(list)

    for filepath in Path(directory).rglob("*"):
        if filepath.is_file():
            file_hash = get_file_hash(filepath)
            hash_dict[file_hash].append(filepath)

    duplicates = {h:files for h, files in hash_dict.items() if len(files)>1}
    return duplicates

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        # while chunk:
        #     hasher.update(chunk)
        #     chunk = f.read(8192)

        ## 海象运算符简化写法：
        while chunk := f.read(8192):  # 边赋值边判断
            hasher.update(chunk)
    
    return hasher.hexdigest()

if __name__ == "__main__":
    duplicates = find_duplicates_basic(".")
    
    for file_hash, files in duplicates.items():
        print(f"Hash:")
        for f in files:
            print(f" - {f}")
        
        print("/n")
