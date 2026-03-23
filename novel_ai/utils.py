# ============================================================
# 工具函数
# ============================================================
import hashlib
import json
import os

def generate_filehash(file_path):
    """生成文件md5 hash"""
    with open(file_path, "rb") as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


base_dir = os.path.dirname(os.path.abspath(__file__))
COLLECTIONS_JSON_PATH = os.path.join(base_dir, 'collections.json')

def get_collections():
    """获取文件指纹信息"""
    with open(COLLECTIONS_JSON_PATH, "r",  encoding="utf-8") as f:
        data = json.load(f)
    return data


def set_collections(data):
    """设置文件指纹信息"""
    with open(COLLECTIONS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
