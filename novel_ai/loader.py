# ============================================================
# 文档加载器
# ============================================================
import os 
from langchain_core.documents import Document


def analyze_file(filepath, bookname):
    """加载文本文件并封装为 Document 对象"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filepath)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    docs = [Document(
        page_content=content,
        metadata={"source": filepath, "bookname": bookname}
    )]
    return docs

    


