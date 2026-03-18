# ============================================================
# 任务六：代码审查助手 (LLM API)
# ============================================================
# 难度: ⭐⭐
# 知识点: DeepSeek API, system message, temperature
# ============================================================
#
# 要求:
# 1. 把下面故意写得有问题的代码发给 DeepSeek 做 code review
# 2. system message 设定为"资深 Python 工程师，做代码审查"
# 3. 用 temperature=0 保证输出稳定
# 4. 打印审查结果和 token 用量
#
# 提示:
# - 参考 llm_api/01_basic.py 的调用方式
# - 把 bad_code 作为 user message 的内容发过去
# - response.usage.total_tokens 取 token 用量
# ============================================================

import os
from openai import OpenAI

# 这段代码故意写了一些问题，让 AI 来审查
bad_code = """
def calc(x,y,t):
    if t == 'add':
        return x+y
    if t == 'sub':
        return x-y
    if t == 'mul':
        return x*y
    if t == 'div':
        return x/y

result = calc(10, 0, 'div')
print(result)

data = [1,2,3,4,5]
for i in range(10):
    print(data[i])
"""

API_KEY = "DEEPSEEK_API_KEY"

api_key = os.getenv(API_KEY)
if not api_key:
    print(f"错误：未设置 {API_KEY} 环境变量")
    sys.exit(1)

# 在下面写你的代码 👇
client = OpenAI(
    base_url = "https://api.deepseek.com",
    api_key = os.getenv("DEEPSEEK_API_KEY")
)

def code_review(language, code):
    """大模型code review"""
    response = client.chat.completions.create(
        model = "deepseek-chat",
        temperature = 0,
        messages = [
            { "role": "system", "content": f"资深 {language} 工程师，做代码审查" },
            { "role": "user", "content": code }
            ]
        )
    usage = response.usage.total_tokens
    print(f'{language}: ', response.choices[0].message.content, "\n", f"(tokens: {usage})")

code_review('Python', bad_code)