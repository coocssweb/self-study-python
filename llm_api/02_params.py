# ============================================================
# DeepSeek Chat Completion API — 核心参数详解
# ============================================================
# 运行: python llm_api/02_params.py
# ============================================================

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

MODEL = "deepseek-chat"


# ============================================================
# 1. temperature — 控制随机性 (最重要的参数!)
# ============================================================
print("1. temperature — 控制随机性:")
print("   范围: 0 ~ 2，默认 1")
print("   越低 → 越确定、越一致 (适合代码、数据提取)")
print("   越高 → 越随机、越有创意 (适合写故事、头脑风暴)")
print()

# temperature = 0: 几乎每次回答都一样
print("   temperature=0 (确定性):")
for i in range(3):
    r = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[{"role": "user", "content": "用一个词形容太阳"}]
    )
    print(f"     第{i+1}次: {r.choices[0].message.content}")

print()

# temperature = 1.5: 每次回答可能不同
print("   temperature=1.5 (高随机性):")
for i in range(3):
    r = client.chat.completions.create(
        model=MODEL,
        temperature=1.5,
        messages=[{"role": "user", "content": "用一个词形容太阳"}]
    )
    print(f"     第{i+1}次: {r.choices[0].message.content}")


# ============================================================
# 2. max_tokens — 限制回复长度
# ============================================================
print("\n\n2. max_tokens — 限制回复长度:")
print("   控制模型最多生成多少个 token")
print("   不设置 = 模型自己决定什么时候停")
print()

# 限制很短的回复
r = client.chat.completions.create(
    model=MODEL,
    max_tokens=10,  # 最多 10 个 token
    messages=[{"role": "user", "content": "讲一个笑话"}]
)
print(f"   max_tokens=10: {r.choices[0].message.content}")
print(f"   finish_reason: {r.choices[0].finish_reason}")  # 应该是 "length" (被截断)

print()

# 正常长度
r = client.chat.completions.create(
    model=MODEL,
    max_tokens=200,
    messages=[{"role": "user", "content": "讲一个笑话"}]
)
print(f"   max_tokens=200: {r.choices[0].message.content}")
print(f"   finish_reason: {r.choices[0].finish_reason}")  # 应该是 "stop" (正常结束)


# ============================================================
# 3. top_p — 另一种控制随机性的方式 (核采样)
# ============================================================
print("\n\n3. top_p — 核采样:")
print("   范围: 0 ~ 1，默认 1")
print("   top_p=0.1 → 只从概率最高的 10% token 里选")
print("   top_p=1   → 从所有 token 里选")
print("   一般只调 temperature 或 top_p 其中一个，不要同时调!")


# ============================================================
# 4. stop — 自定义停止词
# ============================================================
print("\n\n4. stop — 自定义停止词:")

r = client.chat.completions.create(
    model=MODEL,
    stop=["。", ".", "\n"],  # 遇到句号或换行就停
    messages=[{"role": "user", "content": "用中文介绍一下Python语言"}]
)
print(f"   stop=['。','.',换行]: {r.choices[0].message.content}")
print("   (只输出了第一句)")


# ============================================================
# 5. 参数速查表
# ============================================================
print("\n\n" + "=" * 50)
print("参数速查表:")
print("=" * 50)
print("""
参数            默认值    说明
─────────────────────────────────────────────────
model           必填      模型名称
messages        必填      消息列表
temperature     1         随机性 (0~2)
max_tokens      无限制    最大回复 token 数
top_p           1         核采样 (0~1)
stop            None      停止词列表
stream          False     是否流式输出
frequency_penalty  0      重复惩罚 (-2~2)，越高越不重复
presence_penalty   0      话题惩罚 (-2~2)，越高越倾向新话题

常用组合:
  代码生成:    temperature=0
  日常对话:    temperature=0.7
  创意写作:    temperature=1.5
  数据提取:    temperature=0, max_tokens=按需设置

注意: DeepSeek 不支持 n 参数 (一次生成多个回复)
      如果需要多个回复，调用多次即可
""")
