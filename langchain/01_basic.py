# ============================================================
# LangChain 基础 — 第一次用 LangChain 调用 LLM
# ============================================================
# 运行: python langchain/01_basic.py
# ============================================================
# 核心问题: LangChain 到底帮你做了什么?
# 答案: 它把你在 llm_api/ 里手写的那些代码封装成了标准接口
# ============================================================

import os
from langchain_openai import ChatOpenAI

# ============================================================
# 1. 创建 LLM 对象
# ============================================================
# 对比原生 API:
#   client = OpenAI(api_key=..., base_url=...)
#   response = client.chat.completions.create(model=..., messages=[...])
#
# LangChain 版:
#   llm = ChatOpenAI(api_key=..., base_url=..., model=...)
#   response = llm.invoke("你的问题")
# ============================================================

print("1. 创建 LLM 对象:")

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
)

print("   ✓ LLM 对象创建成功")
print(f"   模型: {llm.model_name}")


# ============================================================
# 2. 最简单的调用 — invoke()
# ============================================================

print("\n2. 最简单的调用:")

# 直接传字符串，LangChain 自动帮你包装成 messages
response = llm.invoke("用一句话解释什么是LangChain")

print(f"   类型: {type(response).__name__}")  # AIMessage
print(f"   回复: {response.content}")

# response 是一个 AIMessage 对象，不是原生 API 的 dict
# 常用属性:
print(f"\n   response.content       = {response.content[:50]}...")
print(f"   response.response_metadata = 包含 token 用量等信息")

# 取 token 用量
token_usage = response.response_metadata.get("token_usage", {})
print(f"   token 用量: {token_usage}")


# ============================================================
# 3. 用 Message 对象调用（更精确的控制）
# ============================================================

print("\n3. 用 Message 对象:")

from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="你是一个说话简洁的助手，每次回答不超过20个字。"),
    HumanMessage(content="Python是什么?"),
]

response = llm.invoke(messages)
print(f"   回复: {response.content}")

# 对比原生 API:
#   messages = [
#       {"role": "system", "content": "..."},
#       {"role": "user", "content": "..."},
#   ]
# LangChain 用 SystemMessage/HumanMessage/AIMessage 对象代替了 dict
# 本质一样，只是换了个写法


# ============================================================
# 4. 流式输出 — stream()
# ============================================================

print("\n4. 流式输出:")
print("   ", end="")

for chunk in llm.stream("用一句话介绍Python"):
    print(chunk.content, end="", flush=True)

print()  # 换行


# ============================================================
# 5. 批量调用 — batch()
# ============================================================

print("\n5. 批量调用:")

questions = [
    "1+1=?",
    "Python的创始人是谁?",
    "HTTP状态码200表示什么?",
]

# batch() 会并发发送请求，比循环调用快
responses = llm.batch(questions)

for q, r in zip(questions, responses):
    print(f"   Q: {q}")
    print(f"   A: {r.content}\n")


# ============================================================
# 6. 带参数的调用
# ============================================================

print("6. 带参数的调用:")

# 方式1: 创建时指定默认参数
creative_llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=1.5,    # 更有创意
    max_tokens=50,      # 限制回复长度
)

response = creative_llm.invoke("给我编一个笑话")
print(f"   创意模式: {response.content}")

# 方式2: 调用时临时覆盖参数 (bind)
precise_llm = llm.bind(temperature=0, max_tokens=30)
response = precise_llm.invoke("1+1等于几?")
print(f"   精确模式: {response.content}")


# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 50)
print("LangChain vs 原生 API 对比:")
print("=" * 50)
print("""
原生 API (你在 llm_api/ 学的):
  client = OpenAI(api_key=..., base_url=...)
  response = client.chat.completions.create(
      model="deepseek-chat",
      messages=[{"role": "user", "content": "你好"}]
  )
  print(response.choices[0].message.content)

LangChain:
  llm = ChatOpenAI(api_key=..., base_url=..., model="deepseek-chat")
  response = llm.invoke("你好")
  print(response.content)

看起来只是换了个写法? 没错，单独调用 LLM 时差别不大。
LangChain 的威力在后面 — 当你需要:
  - 组合多个步骤 (Chain)
  - 格式化输入 (PromptTemplate)
  - 解析输出 (OutputParser)
  - 管理记忆 (Memory)
这些才是 LangChain 真正省力的地方。下一个文件开始讲。
""")
