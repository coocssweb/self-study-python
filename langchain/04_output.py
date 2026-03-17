# ============================================================
# LangChain — OutputParser 输出解析
# ============================================================
# 运行: python langchain/04_output.py
# ============================================================
# 问题: LLM 返回的是自然语言文本，但你的程序需要结构化数据
# 比如你想让 LLM 返回一个 JSON，而不是一段话
# OutputParser 就是解决这个问题的
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0,  # 结构化输出用低温度，减少随机性
)


# ============================================================
# 1. StrOutputParser — 最简单的，提取纯文本
# ============================================================

print("1. StrOutputParser (你已经见过了):")

chain = ChatPromptTemplate.from_messages([
    ("user", "1+1=?"),
]) | llm | StrOutputParser()

result = chain.invoke({})
print(f"   类型: {type(result).__name__}")  # str
print(f"   结果: {result}")


# ============================================================
# 2. JsonOutputParser — 让 LLM 返回 JSON
# ============================================================

print("\n2. JsonOutputParser:")

# 先定义你想要的数据结构 (用 Pydantic)
class BookInfo(BaseModel):
    title: str = Field(description="书名")
    author: str = Field(description="作者")
    year: int = Field(description="出版年份")
    summary: str = Field(description="一句话简介")

# 创建 parser
parser = JsonOutputParser(pydantic_object=BookInfo)

# parser.get_format_instructions() 会生成一段提示词
# 告诉 LLM 应该返回什么格式的 JSON
print(f"   格式指令 (会自动加到提示词里):")
print(f"   {parser.get_format_instructions()[:100]}...")

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个图书信息助手。{format_instructions}"),
    ("user", "介绍一下《{book}》这本书"),
])

chain = prompt | llm | parser

# partial 可以预填一些变量
result = chain.invoke({
    "book": "三体",
    "format_instructions": parser.get_format_instructions(),
})

print(f"\n   类型: {type(result).__name__}")  # dict
print(f"   结果: {result}")
print(f"   书名: {result['title']}")
print(f"   作者: {result['author']}")


# ============================================================
# 3. with_structured_output — 更简单的方式 (推荐)
# ============================================================

print("\n3. with_structured_output (推荐方式):")

# 这是 LangChain 推荐的方式，更简洁
# 直接告诉 LLM "我要这个结构的数据"

class CityInfo(BaseModel):
    """城市信息"""
    name: str = Field(description="城市名称")
    country: str = Field(description="所属国家")
    population: str = Field(description="大约人口")
    famous_for: str = Field(description="以什么闻名")

# 用 with_structured_output 创建一个新的 LLM 对象
structured_llm = llm.with_structured_output(CityInfo)

prompt = ChatPromptTemplate.from_messages([
    ("user", "介绍一下{city}这个城市"),
])

chain = prompt | structured_llm

result = chain.invoke({"city": "东京"})

print(f"   类型: {type(result).__name__}")  # CityInfo
print(f"   城市: {result.name}")
print(f"   国家: {result.country}")
print(f"   人口: {result.population}")
print(f"   闻名: {result.famous_for}")


# ============================================================
# 4. 实际例子 — 从文本中提取结构化信息
# ============================================================

print("\n4. 实际例子 — 信息提取:")

class PersonInfo(BaseModel):
    """从文本中提取的人物信息"""
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")
    occupation: str = Field(description="职业")
    skills: list[str] = Field(description="技能列表")

structured_llm = llm.with_structured_output(PersonInfo)

prompt = ChatPromptTemplate.from_messages([
    ("system", "从用户提供的文本中提取人物信息。"),
    ("user", "{text}"),
])

chain = prompt | structured_llm

text = "小王今年28岁，是一名全栈工程师，擅长Python、React和Docker。"
result = chain.invoke({"text": text})

print(f"   原文: {text}")
print(f"   姓名: {result.name}")
print(f"   年龄: {result.age}")
print(f"   职业: {result.occupation}")
print(f"   技能: {result.skills}")


# ============================================================
# 5. 实际例子 — 批量分类
# ============================================================

print("\n5. 实际例子 — 文本分类:")

class Classification(BaseModel):
    """文本分类结果"""
    category: str = Field(description="分类: 技术/生活/娱乐/财经")
    confidence: float = Field(description="置信度 0-1")
    reason: str = Field(description="分类理由，一句话")

structured_llm = llm.with_structured_output(Classification)

prompt = ChatPromptTemplate.from_messages([
    ("system", "对用户提供的文本进行分类。"),
    ("user", "{text}"),
])

chain = prompt | structured_llm

texts = [
    "Python 3.12 发布了，新增了类型参数语法",
    "周末去爬山，风景特别好",
    "这部电影的特效太震撼了",
]

for text in texts:
    result = chain.invoke({"text": text})
    print(f"   「{text}」")
    print(f"    → {result.category} (置信度: {result.confidence}) - {result.reason}\n")


# ============================================================
# 总结
# ============================================================

print("=" * 50)
print("OutputParser 要点:")
print("=" * 50)
print("""
1. StrOutputParser     — AIMessage → 纯字符串 (最常用)
2. JsonOutputParser    — AIMessage → dict (需要手动加格式指令)
3. with_structured_output — 直接返回 Pydantic 对象 (推荐!)

with_structured_output 是最推荐的方式:
  class MyData(BaseModel):
      field1: str
      field2: int

  structured_llm = llm.with_structured_output(MyData)
  result = structured_llm.invoke("...")  # 直接得到 MyData 对象

这在实际项目中非常有用:
  - 从文本中提取结构化信息
  - 文本分类
  - 情感分析
  - 生成 API 参数
""")
