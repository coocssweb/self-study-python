# ============================================================
# DeepSeek Chat Completion API — 流式输出 (Streaming)
# ============================================================
# 运行: python llm_api/04_stream.py
# ============================================================

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MODEL = "deepseek-chat"


# ============================================================
# 为什么要流式输出?
# - 普通调用: 等模型生成完所有内容，一次性返回 (可能等好几秒)
# - 流式调用: 模型边生成边返回，像打字机一样逐字显示
# - 用户体验好很多! ChatGPT/DeepSeek 网页版就是流式输出
# ============================================================


# 1. 普通调用 (对比用)
print("1. 普通调用 (等待完整响应):")
print("   请求中...", end="", flush=True)

r = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "user", "content": "用3句话介绍Python"}]
)
print(f"\n   {r.choices[0].message.content}\n")


# 2. 流式调用
print("2. 流式调用 (逐字输出):")
print("   ", end="")

stream = client.chat.completions.create(
    model=MODEL,
    stream=True,  # 开启流式!
    messages=[{"role": "user", "content": "用3句话介绍Python"}]
)

# stream 是一个迭代器，每次 yield 一个 chunk (片段)
for chunk in stream:
    # 每个 chunk 里可能有内容，也可能是空的
    delta = chunk.choices[0].delta
    if delta.content:
        print(delta.content, end="", flush=True)  # flush=True 立即输出

print("\n")  # 换行


# 3. 流式调用 — 收集完整内容
print("3. 流式 + 收集完整内容:")
print("   ", end="")

full_content = []

stream = client.chat.completions.create(
    model=MODEL,
    stream=True,
    messages=[{"role": "user", "content": "用一句话解释什么是AI"}]
)

for chunk in stream:
    delta = chunk.choices[0].delta
    if delta.content:
        full_content.append(delta.content)
        print(delta.content, end="", flush=True)

print()
complete_text = "".join(full_content)
print(f"   完整文本: {complete_text}")
print(f"   总片段数: {len(full_content)}")


# 4. 流式调用 — chunk 的结构
print("\n4. chunk 结构解析:")

stream = client.chat.completions.create(
    model=MODEL,
    stream=True,
    max_tokens=20,
    messages=[{"role": "user", "content": "你好"}]
)

for i, chunk in enumerate(stream):
    choice = chunk.choices[0]
    print(f"   chunk[{i}]: delta.content={choice.delta.content!r}, finish_reason={choice.finish_reason}")

print("""
   说明:
   - 每个 chunk 的 delta.content 是一小段文本 (可能是一个字或几个字)
   - 最后一个 chunk 的 finish_reason 不为 None (通常是 "stop")
   - 中间的 chunk 的 finish_reason 都是 None
""")
