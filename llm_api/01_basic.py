# ============================================================
# DeepSeek Chat Completion API — 第一次调用
# ============================================================
# 安装: python -m pip install openai
# 设置环境变量: DEEPSEEK_API_KEY=sk-你的密钥
# 运行: python llm_api/01_basic.py
# ============================================================
# DeepSeek 的 API 兼容 OpenAI 格式，所以直接用 openai 库
# 只需要改 base_url 和 api_key
# ============================================================

import os
from openai import OpenAI

# 创建客户端 — 指向 DeepSeek 的 API 地址
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",  # DeepSeek 的 API 地址
)

# ---- 最简单的调用 ----
print("1. 最简单的调用:")

response = client.chat.completions.create(
    model="deepseek-chat",     # DeepSeek 的模型名称
    messages=[
        {"role": "user", "content": "用一句话解释什么是API"}
    ]
)

# 打印完整响应对象，看看结构
print("\n   完整响应对象:")
print(f"   id: {response.id}")
print(f"   model: {response.model}")
print(f"   created: {response.created}")

# 取出回复内容
reply = response.choices[0].message.content
print(f"\n   回复: {reply}")

# 取出 token 用量
usage = response.usage
print(f"\n   Token 用量:")
print(f"     prompt_tokens: {usage.prompt_tokens}")       # 你发送的
print(f"     completion_tokens: {usage.completion_tokens}") # 模型回复的
print(f"     total_tokens: {usage.total_tokens}")           # 总计


# ---- 概念解释 ----
print("\n" + "=" * 50)
print("核心概念:")
print("=" * 50)

print("""
1. Token (令牌)
   - LLM 不是按"字"处理文本的，而是按 token
   - 英文大约 1 个单词 ≈ 1-2 个 token
   - 中文大约 1 个字 ≈ 1-2 个 token
   - API 按 token 数量计费
   - DeepSeek 非常便宜: 输入 ¥1/百万token, 输出 ¥2/百万token (缓存命中更便宜)

2. Model (模型)
   DeepSeek 模型:
   - deepseek-chat      — 通用对话模型 (推荐，便宜好用)
   - deepseek-reasoner  — 推理模型 (类似 o1，擅长数学/编程)

   其他兼容 OpenAI 格式的国产模型 (改 base_url 即可切换):
   - 通义千问 (阿里)    — https://dashscope.aliyuncs.com/compatible-mode/v1
   - 智谱 GLM (清华)    — https://open.bigmodel.cn/api/paas/v4
   - Moonshot (月之暗面) — https://api.moonshot.cn/v1

3. Messages (消息列表)
   - 这是 Chat Completion 的核心输入
   - 是一个消息数组，每条消息有 role 和 content
   - role 有三种: system, user, assistant (下一个文件详细讲)

4. choices
   - 响应里的 choices 是一个数组
   - 通常只有一个元素 choices[0]
   - choices[0].message.content 就是模型的回复
   - choices[0].finish_reason 表示停止原因:
     "stop" = 正常结束
     "length" = 达到 max_tokens 限制被截断
""")
