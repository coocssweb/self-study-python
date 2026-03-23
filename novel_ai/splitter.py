# ============================================================
# 切片器
# ============================================================
from langchain_text_splitters import RecursiveCharacterTextSplitter

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 300,
    chunk_overlap = 60,
    separators = ["\n\n", "\n", "。", "，", " ", ""]
)
