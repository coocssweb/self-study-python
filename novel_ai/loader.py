# ============================================================
# 文档加载器
# ============================================================
import os 
import sys
from langchain_core.documents import Document
from utils import generate_filehash, get_collections, set_collections
from vector_store import remove_store

def analyze_file(filename):
    """加载文本文件并封装为 Document 对象"""
    bookname = filename.split("_")[1].split('.')[0]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    collections = get_collections()
    book_collection = collections.get(filename)
    book_hash = generate_filehash(file_path)

    # 文件是否已存在
    if book_collection:
        if book_collection["hash"] == book_hash:
            return None
        else:
            remove_store(filename)

    collections[filename] = {
        "bookname": bookname,
        "hash": book_hash
    }
    
    set_collections(collections)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        docs = [Document(
            page_content=content,
            metadata={"source": filename, "bookname": bookname}
        )]
        return docs
    except FileNotFoundError:
        raise FileNotFoundError(f"文件不存在: {file_path}")
    except Exception as e:
        raise RuntimeError(f"文件读取失败: {e}")

    


    


