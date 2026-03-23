# ============================================================
# 主程序
# ============================================================
import sys
from llm import client
from splitter import recursive_splitter
from vector_store import create_store
from loader import analyze_file
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

try:
    documents = analyze_file("book.txt", "孔乙己")
    if documents:
        store = create_store(documents)
    else:
        store = read_store()
except Exception as e:
    print(f"加载文档失败: {e}")
    sys.exit(1)

retriever = store.as_retriever(search_kwargs={"k": 3})

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


def format_docs(docs):
    """Document文档格式化为纯文本"""
    return "\n\n".join(f"[来源:{doc.metadata.get('bookname', '未知')}]\n{doc.page_content}" for doc in docs)

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