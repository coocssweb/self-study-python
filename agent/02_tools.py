"""
02 - LangChain 自定义工具

上一节我们手动写了 Function Calling 的完整流程，比较繁琐。
LangChain 用 @tool 装饰器把这个过程简化了。

类比前端：@tool 就像 Vue 的 defineComponent 或 React 的 forwardRef，
把一堆样板代码封装成一个简洁的声明式 API。

本节学习：
1. 用 @tool 装饰器定义工具
2. 用 StructuredTool 定义更复杂的工具
3. 理解工具的 name、description、args_schema 如何影响 LLM 的决策
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

# ============================================================
# 初始化 LLM
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 方式一：@tool 装饰器（最简单）
# 函数的 docstring 会自动变成工具描述
# 参数类型注解会自动变成参数 schema
# ============================================================

@tool
def search_knowledge(query: str) -> str:
    """根据关键词搜索知识库，返回相关内容。当用户问专业问题时使用。"""
    # 模拟知识库搜索
    knowledge = {
        "python": "Python 是一种解释型、面向对象的高级编程语言",
        "langchain": "LangChain 是一个用于开发 LLM 应用的框架",
        "agent": "Agent 是能自主决策和执行任务的 AI 系统",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return value
    return f"未找到与 '{query}' 相关的内容"


@tool
def get_current_time() -> str:
    """获取当前时间。当用户询问现在几点时使用。"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 看看 @tool 自动生成了什么
print("=== @tool 装饰器生成的工具信息 ===")
print(f"工具名: {search_knowledge.name}")
print(f"描述: {search_knowledge.description}")
print(f"参数 schema: {search_knowledge.args_schema.model_json_schema()}")

# ============================================================
# 方式二：StructuredTool + Pydantic（更精细的控制）
# 当你需要多个参数、参数校验、详细描述时使用
# ============================================================

class TranslateInput(BaseModel):
    """翻译工具的输入参数"""
    text: str = Field(description="要翻译的文本")
    target_language: str = Field(
        default="英文",
        description="目标语言，如：英文、日文、法文"
    )


def translate_text(text: str, target_language: str = "英文") -> str:
    """模拟翻译（实际项目中可以调翻译 API）"""
    return f"[模拟翻译] 将 '{text}' 翻译为{target_language}: (翻译结果)"


# 用 StructuredTool 创建工具
translate_tool = StructuredTool.from_function(
    func=translate_text,
    name="translate",
    description="将文本翻译成指定语言。当用户需要翻译时使用。",
    args_schema=TranslateInput,
)

print(f"\n=== StructuredTool 生成的工具信息 ===")
print(f"工具名: {translate_tool.name}")
print(f"描述: {translate_tool.description}")
print(f"参数 schema: {translate_tool.args_schema.model_json_schema()}")

# ============================================================
# 把工具绑定到 LLM
# bind_tools 告诉 LLM "你有这些工具可以用"
# ============================================================

all_tools = [search_knowledge, get_current_time, translate_tool]
llm_with_tools = llm.bind_tools(all_tools)

print("\n=== 测试 LLM 工具选择 ===")

# 测试1：应该选择 search_knowledge
response = llm_with_tools.invoke("什么是 LangChain？")
print(f"\n问题: 什么是 LangChain？")
if response.tool_calls:
    for tc in response.tool_calls:
        print(f"  LLM 选择了工具: {tc['name']}, 参数: {tc['args']}")
else:
    print(f"  LLM 直接回答: {response.content[:100]}")

# 测试2：应该选择 get_current_time
response = llm_with_tools.invoke("现在几点了？")
print(f"\n问题: 现在几点了？")
if response.tool_calls:
    for tc in response.tool_calls:
        print(f"  LLM 选择了工具: {tc['name']}, 参数: {tc['args']}")
else:
    print(f"  LLM 直接回答: {response.content[:100]}")

# 测试3：应该选择 translate
response = llm_with_tools.invoke("帮我把'你好世界'翻译成日文")
print(f"\n问题: 帮我把'你好世界'翻译成日文")
if response.tool_calls:
    for tc in response.tool_calls:
        print(f"  LLM 选择了工具: {tc['name']}, 参数: {tc['args']}")
else:
    print(f"  LLM 直接回答: {response.content[:100]}")

# ============================================================
# 关键理解：工具描述的重要性
# ============================================================
print("\n=== 重要提示 ===")
print("""
工具的 description 非常关键，它直接影响 LLM 是否会选择这个工具。

好的描述：
  "根据关键词搜索知识库，返回相关内容。当用户问专业问题时使用。"
  → 告诉 LLM 什么时候用、能做什么

差的描述：
  "搜索"
  → LLM 不知道搜什么、什么时候该用

类比前端：就像组件的 props 文档。
写清楚了，别人（LLM）才知道怎么用你的组件（工具）。
""")
