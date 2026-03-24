# ============================================================
# 主程序
# ============================================================
import sys
from pathlib import Path
from llm import client
from vector_store import read_store
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

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

contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", """根据对话历史和最新问题，生成一个独立的、完整的搜索查询。
如果最新问题已经是独立的，直接返回原问题。
只输出改写后的查询，不要解释。"""),
    ("user", """对话历史：{chat_history}
    最新问题:{question}
    """)
])

compress_prompt = ChatPromptTemplate.from_messages([
    ("system", """请简要总结以下对话的关键信息，保留重要的问题和结论。
用简洁的语言概括，不要遗漏关键细节。"""),
    ("user", """文档片段:{context}""")
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

# 历史记录管道
contextualize_chain = contextualize_prompt | client | StrOutputParser()

# 压缩管道
compress_chain = compress_prompt | client | StrOutputParser()


MAX_HISTORY_LENGTH = 3

chat_summary = ""
chat_history = []
def conversational_rag(question):
    """带对话历史的RAG"""
    global chat_summary, chat_history
    if chat_history:
        if len(chat_history) > MAX_HISTORY_LENGTH:
            old_history = chat_history[:-MAX_HISTORY_LENGTH]
            old_history_text = "\n".join(f"{'用户' if isinstance(message, HumanMessage) else '助手'}： {message.content}" for message in old_history)
            chat_summary = compress_chain.invoke({
                "context": old_history_text
            })
        
        recent_history_text = "\n".join(
            f"{'用户' if isinstance(message, HumanMessage) else '助手'}： {message.content}" 
            for message in chat_history[-MAX_HISTORY_LENGTH:]
        )
        if (chat_summary):
            old_history_text = f"之前的对话摘要：{chat_summary}\n" + old_history_text
        
        chat_summary = compress_chain.invoke({"context": old_history_text})
        chat_history = chat_history[-MAX_HISTORY_LENGTH:]
        standalone_question = contextualize_chain.invoke({
            "chat_history": history_text,
            "question": question
        })
    else:
        standalone_question = question
    print('='*50)
    print(standalone_question)
    answer = rag_chain.invoke(standalone_question)
    return answer


while True:
    user_input = input("请输入内容：")
    if user_input == "clear":
        print("清空会话")
        chat_history = []
    else:
        answer  = conversational_rag(user_input)
        chat_history.extend([HumanMessage(content = user_input), AIMessage(content = answer)])
        print(answer)
