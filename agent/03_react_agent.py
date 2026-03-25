"""
03 - ReAct Agent：推理 + 行动循环

ReAct = Reasoning + Acting，是 Agent 最核心的模式。

流程：
1. 思考（Thought）：分析用户问题，决定下一步做什么
2. 行动（Action）：调用工具执行
3. 观察（Observation）：看工具返回了什么
4. 重复 1-3，直到能给出最终答案

类比前端：就像 Redux-Saga 的工作流。
接收 action → 执行 side effect → 根据结果 dispatch 新 action → 循环直到完成。

本节使用 LangChain 的 create_react_agent 快速构建一个 ReAct Agent。
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# ============================================================
# 初始化 LLM
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 定义工具集
# ============================================================

@tool
def search_web(query: str) -> str:
    """搜索互联网获取最新信息。当需要查找实时数据或最新资讯时使用。"""
    # 模拟搜索结果
    results = {
        "python 最新版本": "Python 3.12 是当前最新稳定版本，于 2024 年发布",
        "langchain": "LangChain 是最流行的 LLM 应用开发框架，最新版本 0.3.x",
        "天气": "今天天气晴朗，气温 25°C",
    }
    for key, value in results.items():
        if key in query.lower():
            return value
    return f"搜索 '{query}' 的结果：暂无相关信息"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式。当需要进行数学运算时使用。"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算出错: {e}"


@tool
def get_word_count(text: str) -> str:
    """统计文本的字数和词数。当需要分析文本长度时使用。"""
    char_count = len(text)
    word_count = len(text.split())
    return f"字符数: {char_count}, 词数: {word_count}"


tools = [search_web, calculator, get_word_count]

# ============================================================
# 创建 ReAct Agent
# create_react_agent 内部做了这些事：
# 1. 把工具绑定到 LLM
# 2. 构建 ReAct 循环（思考 → 调工具 → 观察 → 继续）
# 3. 设置终止条件（LLM 不再调工具时结束）
# ============================================================

# 系统提示词，定义 Agent 的角色和行为
system_message = "你是一个有用的助手，可以搜索信息、做数学计算、统计文本。请用中文回答。"

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_message,
)

# ============================================================
# 测试 Agent
# ============================================================

def test_agent(query: str):
    """测试 Agent 并打印执行过程"""
    print(f"\n{'='*60}")
    print(f"用户: {query}")
    print(f"{'='*60}")

    # invoke 返回完整的执行结果
    result = agent.invoke({"messages": [("user", query)]})

    print("++++++++++++++++++++++", result)

    # 打印执行过程中的每条消息
    for msg in result["messages"]:
        if msg.type == "human":
            continue  # 跳过用户消息，已经打印过了
        elif msg.type == "ai":
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"\n🔧 调用工具: {tc['name']}")
                    print(f"   参数: {tc['args']}")
            if msg.content:
                print(f"\n🤖 助手: {msg.content}")
        elif msg.type == "tool":
            print(f"   📋 工具结果: {msg.content[:200]}")


if __name__ == "__main__":
    # 场景1：简单问题，可能需要搜索
    # test_agent("Python 最新版本是什么？")

    # 场景2：需要计算
    test_agent("帮我算一下，如果每天存 100 块，一年能存多少？再算上 3% 的年利率呢？")

    # 场景3：多步骤任务，Agent 需要自己规划
    # test_agent("搜索一下 LangChain 是什么，然后统计你的回答有多少字")

    # ============================================================
    # 关键理解
    # ============================================================
    print(f"\n{'='*60}")
    print("关键理解：")
    print("""
    ReAct Agent 的核心价值：
    1. 自主决策 — LLM 自己决定用什么工具、什么顺序
    2. 多步推理 — 可以连续调用多个工具，逐步解决问题
    3. 错误恢复 — 如果一个工具返回不理想，可以换个方式再试

    类比前端路由：
    - 传统方式：写死每个 URL 对应哪个页面（硬编码逻辑）
    - Agent 方式：根据 URL 内容动态决定渲染什么（LLM 动态决策）
    """)
