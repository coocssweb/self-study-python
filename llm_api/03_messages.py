# ============================================================
# DeepSeek Chat Completion API — 消息角色详解
# ============================================================
# 运行: python llm_api/03_messages.py
# ============================================================

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MODEL = "deepseek-chat"


# ============================================================
# messages 是 Chat Completion 的核心，它是一个消息列表
# 每条消息有两个字段: role (角色) 和 content (内容)
#
# 三种角色:
#   system    — 系统指令，设定 AI 的行为和人设
#   user      — 用户的输入
#   assistant — AI 的回复 (用于提供对话历史)
# ============================================================


# 1. 没有 system 消息 — AI 用默认行为回答
print("1. 没有 system 消息:")

r = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "1+1等于几?"}
    ]
)
print(f"   {r}\n")


# 2. system 消息 — 设定 AI 的角色和行为
print("2. system 消息 — 设定角色:")

# 例子: 让 AI 扮演一个海盗
r = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你是一个说话像海盗的助手，每句话都要带点海盗风格。"},
        {"role": "user", "content": "1+1等于几?"}
    ]
)
print(f"   海盗风格: {r}\n")

# 例子: 让 AI 只用 JSON 格式回复
r = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你只用 JSON 格式回复。不要输出任何其他内容。"},
        {"role": "user", "content": "介绍一下Python语言"}
    ]
)
print(f"   JSON格式: {r}\n")


# 3. system 消息的常见用法
print("3. system 消息常见用法:")
print("""
   a) 设定角色:
      "你是一个资深Python开发者，回答简洁专业。"

   b) 限制输出格式:
      "只用JSON格式回复，包含 name, description, example 三个字段。"

   c) 限制回答范围:
      "你是一个客服机器人，只回答关于我们产品的问题。其他问题回复'这超出了我的服务范围'。"

   d) 设定语言:
      "始终用中文回答。"

   e) 组合使用:
      "你是一个英语老师。用户会给你中文句子，你翻译成英文，
       并解释语法要点。输出格式: 翻译 + 语法说明。"
""")


# 4. assistant 消息 — 提供对话历史 (Few-shot 技巧)
print("4. assistant 消息 — Few-shot 示例:")

# 通过给几个 user/assistant 的示例，教 AI 你想要的格式
r = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "你是一个情感分析助手，只回复: 正面/负面/中性"},
        # 给两个示例 (few-shot)
        {"role": "user", "content": "这个餐厅太好吃了!"},
        {"role": "assistant", "content": "正面"},
        {"role": "user", "content": "等了一个小时还没上菜"},
        {"role": "assistant", "content": "负面"},
        # 真正的问题
        {"role": "user", "content": "味道还行，就是有点贵"}
    ]
)
print(f"   情感分析: {r.choices[0].message.content}\n")


# 5. 消息顺序很重要
print("5. 消息顺序:")
print("""
   messages 的顺序就是对话的时间线:
   
   [
     system    → 最前面，设定全局行为
     user      → 第1轮用户输入
     assistant → 第1轮 AI 回复
     user      → 第2轮用户输入
     assistant → 第2轮 AI 回复
     user      → 当前用户输入 (最后一条)
   ]
   
   注意:
   - system 消息通常只有一条，放在最前面
   - 最后一条消息通常是 user (你在问问题)
   - API 本身是无状态的! 每次调用都要把完整对话历史发过去
   - 这就是为什么 token 会越来越多 (对话越长越贵)
""")


# 6. 实用示例: 翻译助手
print("6. 实用示例 — 翻译助手:")

r = client.chat.completions.create(
    model=MODEL,
    temperature=0,  # 翻译要确定性
    messages=[
        {
            "role": "system",
            "content": (
                "你是一个翻译助手。"
                "用户输入中文，你翻译成英文。"
                "用户输入英文，你翻译成中文。"
                "只输出翻译结果，不要解释。"
            )
        },
        {"role": "user", "content": "今天天气真好"}
    ]
)
print(f"   中→英: {r.choices[0].message.content}")

r = client.chat.completions.create(
    model=MODEL,
    temperature=0,
    messages=[
        {
            "role": "system",
            "content": (
                "你是一个翻译助手。"
                "用户输入中文，你翻译成英文。"
                "用户输入英文，你翻译成中文。"
                "只输出翻译结果，不要解释。"
            )
        },
        {"role": "user", "content": "The weather is beautiful today"}
    ]
)
print(f"   英→中: {r.choices[0].message.content}")


# 7. 实用示例: 代码解释器
print("\n7. 实用示例 — 代码解释器:")

code = """
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b
"""

r = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "你是一个Python老师。用中文逐行解释用户给你的代码。简洁明了。"
        },
        {"role": "user", "content": f"解释这段代码:\n```python\n{code}\n```"}
    ]
)
print(f"   {r.choices[0].message.content}")
