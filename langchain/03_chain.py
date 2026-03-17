# ============================================================
# LangChain — Chain 链式调用 (LCEL)
# ============================================================
# 运行: python langchain/03_chain.py
# ============================================================
# LCEL = LangChain Expression Language
# 就是用 | 管道符把多个步骤串起来
# 类似 Linux 的管道: cat file | grep error | sort
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
)


# ============================================================
# 1. 最基础的 Chain: prompt | llm | parser
# ============================================================

print("1. 基础 Chain:")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个编程助手，回答简洁。"),
    ("user", "{question}"),
])

# StrOutputParser 把 AIMessage 对象变成纯字符串
# 没有它: response 是 AIMessage(content="...")
# 有了它: response 就是 "..." 字符串
parser = StrOutputParser()

chain = prompt | llm | parser

# 现在 chain 的流程: 输入dict → prompt生成消息 → llm调用 → parser提取字符串
response = chain.invoke({"question": "Python的GIL是什么?"})

print(f"   类型: {type(response).__name__}")  # str，不再是 AIMessage
print(f"   回复: {response}")


# ============================================================
# 2. 多步骤 Chain — 先翻译再总结
# ============================================================

print("\n2. 多步骤 Chain (翻译 → 总结):")

# 第一步: 翻译
translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个翻译，只输出翻译结果。"),
    ("user", "把以下文本翻译成英文:\n{text}"),
])

translate_chain = translate_prompt | llm | StrOutputParser()

# 第二步: 总结 (用翻译结果作为输入)
summary_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the following text in one sentence."),
    ("user", "{text}"),
])

summary_chain = summary_prompt | llm | StrOutputParser()

# 手动串联两步
chinese_text = "Python是一种广泛使用的高级编程语言，由Guido van Rossum于1991年创建。它强调代码的可读性，语法简洁优雅。"

print(f"   原文: {chinese_text}")

translated = translate_chain.invoke({"text": chinese_text})
print(f"   翻译: {translated}")

summary = summary_chain.invoke({"text": translated})
print(f"   总结: {summary}")


# ============================================================
# 3. RunnablePassthrough 和 RunnableLambda
# ============================================================

print("\n3. RunnablePassthrough 和 RunnableLambda:")

from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# RunnableLambda — 把普通函数变成 chain 的一环
def word_count(text: str) -> str:
    """统计字数并附加到文本后面"""
    count = len(text)
    return f"{text}\n\n(以上回复共 {count} 个字符)"

chain = prompt | llm | StrOutputParser() | RunnableLambda(word_count)

response = chain.invoke({"question": "什么是API?"})
print(f"   {response}")

# RunnablePassthrough — 原样传递输入，常用于保留原始数据
# 后面讲 RAG 时会大量用到，这里先知道有这个东西


# ============================================================
# 4. Chain 的流式输出
# ============================================================

print("\n4. Chain 也支持流式输出:")

chain = prompt | llm | StrOutputParser()

print("   ", end="")
for chunk in chain.stream({"question": "用一句话解释什么是Docker"}):
    print(chunk, end="", flush=True)
print()


# ============================================================
# 5. Chain 的批量调用
# ============================================================

print("\n5. Chain 批量调用:")

questions = [
    {"question": "什么是REST API?"},
    {"question": "什么是WebSocket?"},
    {"question": "什么是GraphQL?"},
]

responses = chain.batch(questions)

for q, r in zip(questions, responses):
    print(f"   Q: {q['question']}")
    print(f"   A: {r[:60]}...\n")


# ============================================================
# 6. 实际例子 — 代码审查 Chain
# ============================================================

print("6. 实际例子 — 代码审查:")

review_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个代码审查专家。请审查用户提供的代码，指出:
1. 潜在的 bug
2. 可以改进的地方
回答简洁，用中文。"""),
    ("user", "请审查这段{language}代码:\n```\n{code}\n```"),
])

review_chain = review_prompt | llm | StrOutputParser()

code = """
def get_user(users, name):
    for i in range(len(users)):
        if users[i] == name:
            return users[i]
"""

response = review_chain.invoke({"language": "Python", "code": code})
print(f"   {response}")


# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 50)
print("Chain 要点:")
print("=" * 50)
print("""
1. LCEL 管道语法: prompt | llm | parser
   - 每个组件的输出是下一个组件的输入
   - 类似 Linux 管道 或 JavaScript 的 Promise.then()

2. StrOutputParser() — 把 AIMessage 变成纯字符串

3. RunnableLambda(fn) — 把普通函数插入 chain

4. chain 统一支持:
   - chain.invoke()  — 单次调用
   - chain.stream()  — 流式输出
   - chain.batch()   — 批量调用

5. 这就是 LangChain 的核心思想:
   把 LLM 调用拆成可组合的小步骤，用管道串起来
""")
