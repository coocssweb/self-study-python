# ============================================================
# LangChain — PromptTemplate 提示词模板
# ============================================================
# 运行: python langchain/02_prompt.py
# ============================================================
# 为什么需要模板?
# 你在写应用时，提示词往往不是固定的，而是需要动态填入变量
# 比如: "把{text}翻译成{language}" — text 和 language 是变量
# PromptTemplate 就是帮你管理这些带变量的提示词
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
)


# ============================================================
# 1. 基础字符串模板 — PromptTemplate
# ============================================================

print("1. 基础字符串模板:")

# 用 {变量名} 做占位符
template = PromptTemplate.from_template(
    "用一句话解释什么是{concept}"
)

# 填入变量，生成最终的提示词
prompt = template.format(concept="递归")
print(f"   生成的提示词: {prompt}")

# 也可以直接 invoke
prompt_value = template.invoke({"concept": "递归"})
print(f"   类型: {type(prompt_value).__name__}")
print(f"   内容: {prompt_value.text}")


# ============================================================
# 2. 聊天模板 — ChatPromptTemplate (更常用)
# ============================================================

print("\n2. 聊天模板 (ChatPromptTemplate):")

# 这个更常用，因为 Chat API 需要 system/user 角色
chat_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，回答要简洁，不超过30个字。"),
    ("user", "{question}"),
])

# 填入变量
messages = chat_template.invoke({
    "role": "Python专家",
    "question": "list和tuple有什么区别?",
})

print(f"   生成的消息:")
for msg in messages.messages:
    print(f"     {msg.type}: {msg.content}")

# 直接发给 LLM
response = llm.invoke(messages)
print(f"   回复: {response.content}")


# ============================================================
# 3. 模板 + LLM 组合 (管道语法 |)
# ============================================================

print("\n3. 管道语法 (这是 LangChain 的精髓!):")

# 用 | 把模板和 LLM 连起来，形成一个 chain
chain = chat_template | llm

# 一步到位: 填变量 → 生成提示词 → 调用 LLM
response = chain.invoke({
    "role": "JavaScript专家",
    "question": "什么是闭包?",
})

print(f"   回复: {response.content}")

# 对比不用 LangChain 你要写:
#   prompt = f"你是一个{role}..."
#   messages = [{"role": "system", "content": prompt}, ...]
#   response = client.chat.completions.create(model=..., messages=messages)
#   print(response.choices[0].message.content)
#
# 用 LangChain:
#   chain = template | llm
#   response = chain.invoke({"role": ..., "question": ...})
#   print(response.content)


# ============================================================
# 4. 多个变量的实际例子 — 翻译器
# ============================================================

print("\n4. 实际例子 — 翻译器:")

translator = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业翻译，只输出翻译结果，不要解释。"),
    ("user", "把以下{source_lang}文本翻译成{target_lang}:\n\n{text}"),
])

chain = translator | llm

response = chain.invoke({
    "source_lang": "中文",
    "target_lang": "英文",
    "text": "今天天气真好，适合写代码。",
})

print(f"   翻译结果: {response.content}")


# ============================================================
# 5. FewShotPromptTemplate — 给模型看几个例子
# ============================================================

print("\n5. Few-Shot 提示 (给模型看例子):")

# 这是 prompt engineering 里很重要的技巧
# 与其告诉模型"怎么做"，不如直接给它看几个例子

few_shot = ChatPromptTemplate.from_messages([
    ("system", "你是一个情感分析助手。根据例子的格式回答。"),
    ("user", "这个电影太好看了!"),
    ("assistant", "正面"),
    ("user", "服务态度很差，再也不来了。"),
    ("assistant", "负面"),
    ("user", "还行吧，一般般。"),
    ("assistant", "中性"),
    ("user", "{text}"),
])

chain = few_shot | llm

texts = [
    "这家餐厅的菜太好吃了，强烈推荐!",
    "快递又丢了，气死我了",
    "今天下雨了",
]

for text in texts:
    response = chain.invoke({"text": text})
    print(f"   「{text}」 → {response.content}")


# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 50)
print("PromptTemplate 要点:")
print("=" * 50)
print("""
1. PromptTemplate     — 简单字符串模板，用 {变量} 占位
2. ChatPromptTemplate — 聊天模板，支持 system/user/assistant 角色
3. 管道语法 |         — template | llm 组成 chain，一步到位
4. Few-Shot           — 在模板里放几个例子，教模型怎么回答

管道语法 chain = template | llm 是 LangChain 的核心写法
后面所有内容都建立在这个基础上
""")
