# ============================================================
# 向量数据
# ============================================================
from langchain_chroma import Chroma

def create_store(documents, embedding):
    """创建向量数据库"""
    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embedding
    )
    return vector_store