# ============================================================
# 任务七：对话摘要器 (LLM API)
# ============================================================
# 难度: ⭐⭐
# 知识点: 多轮对话, messages 列表, 摘要压缩
# ============================================================
#
# 要求:
# 1. 构造一段模拟的多轮对话历史 (5-6 轮 user/assistant 消息)
# 2. 在末尾追加一条 user 消息: "请用 2-3 句话总结以上对话的关键信息"
# 3. 调用 DeepSeek 生成摘要
# 4. 打印摘要结果
#
# 提示:
# - 参考 llm_api/05_multi_turn.py 的多轮对话写法
# - messages 是一个列表，每条消息有 role 和 content
# - 先把模拟对话放进去，最后 append 一条总结请求
#
# 这就是之前讲的"摘要压缩"策略的实际实现!
# 实际项目中，当对话太长时，就用这种方式压缩历史
# ============================================================

import os
from openai import OpenAI

# 模拟的对话历史 — 一个用户在咨询 Python 学习路线
conversation = [
    {"role": "system", "content": "你是一个编程学习顾问。"},
    {"role": "user", "content": "我想学 Python，应该从哪里开始？"},
    {"role": "assistant", "content": "建议从基础语法开始：变量、数据类型、条件判断、循环。推荐《Python编程：从入门到实践》这本书。"},
    {"role": "user", "content": "我已经会 JavaScript 了，可以跳过基础吗？"},
    {"role": "assistant", "content": "可以快速过一遍，重点关注 Python 和 JS 的差异：缩进语法、列表推导式、装饰器、生成器这些。"},
    {"role": "user", "content": "学完基础之后呢？我想做 AI 方向。"},
    {"role": "assistant", "content": "AI 方向建议路线：LLM API 调用 → LangChain → RAG → Agent。不需要深入学机器学习数学，工程方向更看重应用能力。"},
    {"role": "user", "content": "LangChain 和直接调 API 有什么区别？"},
    {"role": "assistant", "content": "LangChain 是对 LLM API 的封装，提供了 Chain、Prompt Template、OutputParser 等抽象。类似前端的框架和原生 JS 的关系。"},
]

# 在下面写你的代码 👇
# 1. 在 conversation 末尾追加一条总结请求
# 2. 调用 DeepSeek API
# 3. 打印摘要结果
