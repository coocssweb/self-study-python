# ============================================================
# 主程序
# ============================================================
import sys
from pathlib import Path
from llm import client
from splitter import recursive_splitter
from vector_store import create_store,read_store
from loader import analyze_file
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

files = [f.name for f in Path("books").glob("*.txt") if f.is_file()]

for filename in files:
    try:
        documents = analyze_file(f"./books/{filename}")
        if documents:
            print("x"*50)
            print(filename)
            print("x"*50)
            spliter_documents = recursive_splitter.split_documents(documents)
            create_store(spliter_documents)    
    except Exception as e:
        print(f"加载文档失败: {e}")

store = read_store()
retriever = store.as_retriever(search_kwargs={"k": 3})
# store.as_retriever(search_type="mmr", search_kwargs={"k": 6, "fetch_k": 20})

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个小说阅读助手。基于提供的参考资料回答问题。
规则:
- 只基于参考资料回答，不要编造信息
- 如果参考资料中没有相关内容，明确说"根据现有资料无法回答"
- 回答要简洁准确，适当引用原文"""),
    ("user", """参考资料:
{context}

问题: {question}"""),
])


# 格式话文档为字符串
def format_docs(docs):
    """Document文档格式化为纯文本"""
    return "\n\n".join(f"[来源:{doc.metadata.get('bookname', '未知')}]\n{doc.page_content}" for doc in docs)

# RAG管道
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | client
    | StrOutputParser()
)

while True:
    user_input = input("请输入内容：")
    retrieved_docs = retriever.invoke(user_input)
    answer  = rag_chain.invoke(user_input)
    print(answer)