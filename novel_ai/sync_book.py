import sys
from pathlib import Path
from loader import analyze_file
from splitter import recursive_splitter
from vector_store import create_store

files = [f.name for f in Path("books").glob("*.txt") if f.is_file()]

for filename in files:
    try:
        documents = analyze_file(f"./books/{filename}")
        if documents:
            spliter_documents = recursive_splitter.split_documents(documents)
            create_store(spliter_documents)    
    except Exception as e:
        print(f"加载文档失败: {e}")