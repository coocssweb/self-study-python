# ============================================================
# 向量数据
# ============================================================
from langchain_chroma import Chroma
from embedding import embedding

# 创建数据库
def create_store(documents):
    """创建向量数据库"""
    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embedding,
        persist_directory = "./chroma_data"
    )
    return vector_store

# 读取数据库
def read_store():
    """读取向量数据库"""
    vector_store = Chroma(
        persist_directory = "./chroma_data",
        embedding_function = embedding
    )
    return vector_store


# 删除数据库
def remove_store(filename):
    """删除书籍"""
    print("="*50)
    print(filename)
    
    vector_store = Chroma(
        persist_directory = "./chroma_data", 
        embedding_function = embedding
    )

    vector_store.delete(where={"source": filename})
