# ============================================================
# DeepSeek Chat Completion API — 多轮对话
# ============================================================
# 运行: python llm_api/05_multi_turn.py
# ============================================================

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MODEL = "deepseek-chat"


# ============================================================
# 核心概念: API 是无状态的!
#
# 每次调用 chat.completions.create() 都是独立的
# 模型不会"记住"之前的对话
# 要实现多轮对话，你需要自己维护消息历史，每次都发过去
# ============================================================


# 1. 错误示范 — 模型不记得上一轮
print("1. 错误示范 (没有历史):")

r1 = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "我叫小明"}]
)
print(f"   第1轮: {r1.choices[0].message.content}")

r2 = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "我叫什么名字?"}]
)
print(f"   第2轮: {r2.choices[0].message.content}")
print("   → 模型不知道你叫什么，因为两次调用是独立的!\n")


# 2. 正确做法 — 维护消息历史
print("2. 正确做法 (带历史):")

messages = [
    {"role": "system", "content": "你是一个友好的助手，回答简洁。"}
]

# 第1轮
messages.append({"role": "user", "content": "我叫小明"})
r1 = client.chat.completions.create(model=MODEL, messages=messages)
reply1 = r1.choices[0].message.content
messages.append({"role": "assistant", "content": reply1})  # 把 AI 回复也加进去!
print(f"   第1轮: {reply1}")

# 第2轮
messages.append({"role": "user", "content": "我叫什么名字?"})
r2 = client.chat.completions.create(model=MODEL, messages=messages)
reply2 = r2.choices[0].message.content
messages.append({"role": "assistant", "content": reply2})
print(f"   第2轮: {reply2}")

# 第3轮
messages.append({"role": "user", "content": "把我的名字倒过来写"})
r3 = client.chat.completions.create(model=MODEL, messages=messages)
reply3 = r3.choices[0].message.content
print(f"   第3轮: {reply3}")

print(f"\n   当前消息历史长度: {len(messages)} 条")
print(f"   总 token: {r3.usage.total_tokens} (越聊越多!)")


# 3. 封装成一个简单的聊天函数
print("\n\n3. 封装聊天函数:")

def chat(messages, user_input):
    """发送消息并更新历史"""
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply, response.usage.total_tokens

# 使用
history = [{"role": "system", "content": "你是一个数学老师，用简单的语言解释概念。"}]

reply, tokens = chat(history, "什么是质数?")
print(f"   Q: 什么是质数?")
print(f"   A: {reply}")
print(f"   (tokens: {tokens})")

reply, tokens = chat(history, "给我举3个例子")
print(f"\n   Q: 给我举3个例子")
print(f"   A: {reply}")
print(f"   (tokens: {tokens})")

reply, tokens = chat(history, "最小的质数是几?")
print(f"\n   Q: 最小的质数是几?")
print(f"   A: {reply}")
print(f"   (tokens: {tokens} — 注意越来越多)")


# 4. 交互式聊天 (取消注释可以体验)
# print("\n\n4. 交互式聊天 (输入 quit 退出):")
#
# history = [{"role": "system", "content": "你是一个友好的AI助手。"}]
#
# while True:
#     user_input = input("\n你: ")
#     if user_input.lower() in ("quit", "exit", "q"):
#         print("再见!")
#         break
#
#     reply, tokens = chat(history, user_input)
#     print(f"AI: {reply}")
#     print(f"(tokens: {tokens})")


# 5. Token 管理策略
print("\n\n" + "=" * 50)
print("Token 管理策略:")
print("=" * 50)
print("""
问题: 对话越长，messages 越大，token 越多，越贵越慢

解决方案:

a) 限制历史长度 — 只保留最近 N 轮
   if len(messages) > 20:
       messages = [messages[0]] + messages[-10:]  # 保留 system + 最近10条

b) 摘要压缩 — 让 AI 总结之前的对话
   summary = "之前聊了: 用户叫小明，问了质数的问题..."
   messages = [system_msg, {"role": "system", "content": summary}, latest_msg]

c) 设置 max_tokens — 控制回复长度，避免意外高消费
""")
