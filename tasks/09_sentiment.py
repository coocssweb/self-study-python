# ============================================================
# 任务九：批量情感分析 (LangChain)
# ============================================================
# 难度: ⭐⭐⭐
# 知识点: JsonOutputParser, Pydantic, 批量处理
# ============================================================
#
# 要求:
# 1. 用 Pydantic 定义情感分析结果:
#    - sentiment: str  (正面/负面/中性)
#    - score: float    (0-1 置信度)
#    - keywords: list[str] (关键词列表)
# 2. 用 JsonOutputParser 解析输出
# 3. 用 for 循环对下面 5 条评论逐条分析
# 4. 打印每条评论的分析结果
#
# 提示:
# - 参考 langchain/04_output.py 第 5 节的分类写法
# - parser = JsonOutputParser(pydantic_object=YourModel)
# - prompt 里加 {format_instructions}
# - chain = prompt | llm | parser
#
# 期望输出类似:
#   「这家餐厅太好吃了，下次还来！」
#    → 正面 (0.95) 关键词: ['好吃', '下次还来']
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

reviews = [
    "这家餐厅太好吃了，服务也很好，下次还来！",
    "等了一个小时才上菜，味道也一般，不推荐。",
    "环境还行，菜品中规中矩，价格偏贵。",
    "老板人很好，送了我们一份甜品，孩子很开心。",
    "外卖送到的时候已经凉了，包装也破了，差评。",
]

# 在下面写你的代码 👇
