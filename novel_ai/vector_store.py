# ============================================================
# 向量数据
# ============================================================
from langchain_chroma import Chroma
from embedding import embedding

def create_store(documents):
    """创建向量数据库"""
    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embedding,
        persist_directory = "./chroma_data"
    )
    return vector_store

def read_store():
    """读取向量数据库"""
    vector_store = Chroma(
        persist_directory = "./chroma_data",
        embedding_function = embedding
    )
    return vector_store