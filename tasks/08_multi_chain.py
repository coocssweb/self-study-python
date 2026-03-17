# ============================================================
# 任务八：多步 Chain — 故事生成器 (LangChain)
# ============================================================
# 难度: ⭐⭐⭐
# 知识点: 多个 Chain 串联, StrOutputParser, 变量传递
# ============================================================
#
# 要求:
# 1. 第一步: 输入一个主题，让 LLM 生成故事大纲 (3-5 个要点)
# 2. 第二步: 把大纲传给另一个 chain，扩写成完整短故事
# 3. 用 StrOutputParser 提取纯文本
# 4. 打印大纲和最终故事
#
# 提示:
# - 参考 langchain/03_chain.py
# - 第一个 chain: prompt1 | llm | StrOutputParser()
# - 拿到大纲后，作为第二个 chain 的输入
# - 第二个 chain: prompt2 | llm | StrOutputParser()
#
# 期望输出:
#   === 故事大纲 ===
#   1. ...
#   2. ...
#   3. ...
#
#   === 完整故事 ===
#   (一段完整的短故事)
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

topic = "一个程序员意外穿越到了古代"

# 在下面写你的代码 👇
