# ============================================================
# 任务三：读书笔记生成器 (LangChain)
# ============================================================
# 难度: ⭐⭐⭐
# 知识点: ChatPromptTemplate, JsonOutputParser, Pydantic, Chain
# ============================================================
#
# 要求:
# 1. 输入一本书的名字，用 LangChain chain 生成结构化读书笔记
# 2. 用 Pydantic BaseModel 定义数据结构，包含:
#    - title: 书名
#    - author: 作者
#    - key_points: 核心观点 (3个，用 list[str])
#    - recommendation: 推荐理由
# 3. 用 ChatPromptTemplate 创建提示词
# 4. 用 JsonOutputParser 解析输出
# 5. 用 | 管道连接成 chain: prompt | llm | parser
#
# 提示:
# - 参考 langchain/04_output.py 第 2 节的写法
# - parser = JsonOutputParser(pydantic_object=YourModel)
# - prompt 里要加 {format_instructions}
# - chain.invoke({..., "format_instructions": parser.get_format_instructions()})
#
# 期望输出类似:
#   《三体》读书笔记:
#   作者: 刘慈欣
#   核心观点:
#     1. 宇宙是一个黑暗森林...
#     2. 技术爆炸可能在短时间内...
#     3. 文明之间的猜疑链...
#   推荐理由: 这是一部融合了物理学...
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

book = "三体"

# 在下面写你的代码 👇

