# ============================================================
# 任务二：多语言翻译器 (LLM API)
# ============================================================
# 难度: ⭐⭐
# 知识点: DeepSeek API, system message, 多次调用
# ============================================================
#
# 要求:
# 1. 调用 DeepSeek API，把下面的中文翻译成英文、日文、韩文
# 2. 用 system message 设定翻译角色 (比如 "你是一个专业翻译...")
# 3. 每种语言调用一次 API (共 3 次)
# 4. 打印每种语言的翻译结果和 token 用量
#
# 提示:
# - 参考 llm_api/01_basic.py 的调用方式
# - client = OpenAI(api_key=..., base_url=...)
# - response = client.chat.completions.create(model=..., messages=[...])
# - response.choices[0].message.content 取回复
# - response.usage.total_tokens 取 token 用量
#
# 期望输出类似:
#   原文: 今天天气真好，我想去公园散步。
#
#   英文: The weather is really nice today, I want to take a walk in the park.
#   (tokens: 42)
#
#   日文: 今日はとてもいい天気で、公園を散歩したいです。
#   (tokens: 51)
#
#   韩文: 오늘 날씨가 정말 좋아서 공원에서 산책하고 싶어요.
#   (tokens: 48)
# ============================================================

import os
from openai import OpenAI

text = "今天天气真好，我想去公园散步。"
languages = ["英文", "日文", "韩文"]

# 在下面写你的代码 👇

