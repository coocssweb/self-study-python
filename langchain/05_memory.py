# ============================================================
# LangChain — Memory 对话记忆
# ============================================================
# 运行: python langchain/05_memory.py
# ============================================================
# 你在 llm_api/05_multi_turn.py 里学过:
#   API 是无状态的，要自己维护 messages 列表
# LangChain 把这个封装成了 Memory，帮你自动管理对话历史
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
)


# ============================================================
# 1. 手动管理历史 (回顾)
# ============================================================

print("1. 手动管理历史 (你已经会的方式):")

# 这就是你在 llm_api/05_multi_turn.py 里学的
history = [
    ("system", "你是一个友好的助手，回答简洁。"),
]

prompt = ChatPromptTemplate.from_messages(
    history + [("user", "{input}")]
)

chain = prompt | llm

r1 = chain.invoke({"input": "我叫小明"})
print(f"   第1轮: {r1.content}")

# 问题: 第二轮模型不记得你叫什么
r2 = chain.invoke({"input": "我叫什么?"})
print(f"   第2轮: {r2.content}")
print("   → 模型不记得，因为没有传历史\n")


# ============================================================
# 2. MessagesPlaceholder — 在模板里留个位置放历史
# ============================================================

print("2. MessagesPlaceholder:")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手，回答简洁。"),
    MessagesPlaceholder(variable_name="history"),  # 历史消息插在这里
    ("user", "{input}"),
])

chain = prompt | llm

# 手动维护历史
history = []

# 第1轮
r1 = chain.invoke({"input": "我叫小明", "history": history})
print(f"   第1轮: {r1.content}")
# 把这轮对话加入历史
history.append(HumanMessage(content="我叫小明"))
history.append(AIMessage(content=r1.content))

# 第2轮 — 带上历史
r2 = chain.invoke({"input": "我叫什么?", "history": history})
print(f"   第2轮: {r2.content}")
history.append(HumanMessage(content="我叫什么?"))
history.append(AIMessage(content=r2.content))

# 第3轮
r3 = chain.invoke({"input": "把我的名字倒过来", "history": history})
print(f"   第3轮: {r3.content}")
print(f"   历史长度: {len(history)} 条消息")


# ============================================================
# 3. RunnableWithMessageHistory — 自动管理历史
# ============================================================

print("\n3. RunnableWithMessageHistory (自动管理):")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数学老师，用简单的语言解释。"),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}"),
])

chain = prompt | llm

# 用 dict 存储不同会话的历史 (类似 session)
store = {}

def get_session_history(session_id: str):
    """根据 session_id 获取对应的历史"""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 包装成自动管理历史的 chain
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 使用时需要指定 session_id
config = {"configurable": {"session_id": "user_001"}}

r1 = chain_with_history.invoke({"input": "什么是质数?"}, config=config)
print(f"   Q: 什么是质数?")
print(f"   A: {r1.content}")

r2 = chain_with_history.invoke({"input": "举3个例子"}, config=config)
print(f"\n   Q: 举3个例子")
print(f"   A: {r2.content}")

r3 = chain_with_history.invoke({"input": "最小的是哪个?"}, config=config)
print(f"\n   Q: 最小的是哪个?")
print(f"   A: {r3.content}")

# 查看存储的历史
history = store["user_001"]
print(f"\n   session user_001 的历史: {len(history.messages)} 条消息")


# ============================================================
# 4. 多个会话互不干扰
# ============================================================

print("\n4. 多会话隔离:")

# 用户A
config_a = {"configurable": {"session_id": "user_A"}}
chain_with_history.invoke({"input": "我叫张三"}, config=config_a)

# 用户B
config_b = {"configurable": {"session_id": "user_B"}}
chain_with_history.invoke({"input": "我叫李四"}, config=config_b)

# 用户A 问自己叫什么
r = chain_with_history.invoke({"input": "我叫什么?"}, config=config_a)
print(f"   用户A问'我叫什么': {r.content}")

# 用户B 问自己叫什么
r = chain_with_history.invoke({"input": "我叫什么?"}, config=config_b)
print(f"   用户B问'我叫什么': {r.content}")

print(f"   → 不同 session_id 的历史是隔离的")


# ============================================================
# 5. 限制历史长度 (防止 token 爆炸)
# ============================================================

print("\n5. 限制历史长度:")

from langchain_core.messages import trim_messages

# 创建一个 trimmer，只保留最近的消息
trimmer = trim_messages(
    max_tokens=200,          # 最多保留约200个token的历史
    strategy="last",         # 保留最后的消息
    token_counter=llm,       # 用 LLM 来计算 token 数
    include_system=True,     # 始终保留 system 消息
    allow_partial=False,     # 不截断单条消息
)

# 模拟一个很长的历史
long_history = [
    HumanMessage(content="你好"),
    AIMessage(content="你好!有什么可以帮你的?"),
    HumanMessage(content="Python是什么?"),
    AIMessage(content="Python是一种高级编程语言，以简洁优雅著称。"),
    HumanMessage(content="它有什么特点?"),
    AIMessage(content="动态类型、缩进语法、丰富的标准库、跨平台。"),
    HumanMessage(content="谁创建的?"),
    AIMessage(content="Guido van Rossum在1991年创建的。"),
]

trimmed = trimmer.invoke(long_history)
print(f"   原始历史: {len(long_history)} 条")
print(f"   裁剪后:   {len(trimmed)} 条")
print(f"   保留的消息:")
for msg in trimmed:
    print(f"     {msg.type}: {msg.content[:40]}...")


# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 50)
print("Memory 要点:")
print("=" * 50)
print("""
1. MessagesPlaceholder — 在模板里留位置放历史消息

2. RunnableWithMessageHistory — 自动管理对话历史
   - 需要提供 get_session_history 函数
   - 用 session_id 区分不同用户/会话
   - 自动把每轮对话追加到历史

3. trim_messages — 裁剪历史，防止 token 太多

4. InMemoryChatMessageHistory — 内存存储 (重启就没了)
   实际项目中会用:
   - Redis — 快速，适合短期会话
   - 数据库 — 持久化，适合长期存储

5. 对比你在 llm_api/ 里手写的:
   之前: 自己维护 messages 列表，手动 append
   现在: LangChain 帮你自动管理，还支持多会话隔离
""")
