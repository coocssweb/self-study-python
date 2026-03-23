# ============================================================
# Embedding 向量化
# ============================================================
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name = "shibing624/text2vec-base-chinese"
)