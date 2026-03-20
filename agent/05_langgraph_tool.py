"""
05 - LangGraph + 工具调用：在图节点中集成工具

上一节的 LangGraph 每个节点都是纯 LLM 调用。
本节把工具调用集成进来，实现"有控制的 Agent"。

核心思路：
- 用 LangGraph 控制整体流程（什么时候该做什么）
- 在需要的节点里让 LLM 调用工具（具体怎么做由 LLM 决定）

类比前端：
- LangGraph 是路由配置（/search → /analyze → /report）
- 每个路由页面内部可以自由发起 API 请求（工具调用）
"""

import os
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# ============================================================
# 初始化
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 定义工具
# ============================================================

@tool
def search_product(keyword: str) -> str:
    """搜索商品信息。根据关键词返回商品名称和价格。"""
    products = {
        "手机": [
            {"name": "iPhone 15", "price": 5999},
            {"name": "小米 14", "price": 3999},
        ],
        "耳机": [
            {"name": "AirPods Pro", "price": 1899},
            {"name": "索尼 WH-1000XM5", "price": 2499},
        ],
        "笔记本": [
            {"name": "MacBook Air M3", "price": 8999},
            {"name": "ThinkPad X1 Carbon", "price": 9999},
        ],
    }
    for key, items in products.items():
        if key in keyword:
            return str(items)
    return "未找到相关商品"


@tool
def calculate_discount(price: float, discount_percent: float) -> str:
    """计算折扣后的价格。传入原价和折扣百分比。"""
    final_price = price * (1 - discount_percent / 100)
    saved = price - final_price
    return f"原价: {price}元, 折扣: {discount_percent}%, 折后价: {final_price:.0f}元, 节省: {saved:.0f}元"


tools = [search_product, calculate_discount]
# 工具名到工具对象的映射
tool_map = {t.name: t for t in tools}

# 把工具绑定到 LLM
llm_with_tools = llm.bind_tools(tools)

# ============================================================
# 定义状态
# add_messages 是 LangGraph 提供的消息累加器
# 每次返回新消息时，会追加到列表而不是覆盖
# ============================================================

class ShoppingState(TypedDict):
    messages: Annotated[list, add_messages]  # 消息历史（自动累加）


# ============================================================
# 定义节点
# ============================================================

def chatbot(state: ShoppingState) -> dict:
    """聊天节点：LLM 决定是回答还是调工具"""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}


def tool_executor(state: ShoppingState) -> dict:
    """工具执行节点：执行 LLM 请求的工具调用"""
    messages = state["messages"]
    last_message = messages[-1]

    tool_results = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        print(f"  🔧 执行工具: {tool_name}({tool_args})")

        # 执行工具
        result = tool_map[tool_name].invoke(tool_args)
        print(f"  📋 结果: {result}")

        # 构造 ToolMessage 返回给 LLM
        tool_results.append(
            ToolMessage(content=str(result), tool_call_id=tool_call["id"])
        )

    return {"messages": tool_results}


# ============================================================
# 定义条件边：决定下一步走哪个节点
# ============================================================

def should_use_tool(state: ShoppingState) -> str:
    """判断是否需要调用工具"""
    last_message = state["messages"][-1]
    # 如果 LLM 返回了 tool_calls，就去执行工具
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    # 否则结束
    return "end"


# ============================================================
# 构建图
# ============================================================

workflow = StateGraph(ShoppingState)

# 添加节点
workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", tool_executor)

# 添加边
workflow.add_edge(START, "chatbot")

# 条件边：chatbot 之后，根据是否有工具调用决定下一步
workflow.add_conditional_edges(
    "chatbot",
    should_use_tool,
    {
        "tools": "tools",   # 有工具调用 → 执行工具
        "end": END,          # 无工具调用 → 结束
    }
)

# 工具执行完后，回到 chatbot 让 LLM 处理结果
workflow.add_edge("tools", "chatbot")

# 编译
app = workflow.compile()

# ============================================================
# 测试
# ============================================================

def chat(user_input: str):
    """发送消息并打印结果"""
    print(f"\n{'='*60}")
    print(f"🛒 用户: {user_input}")

    result = app.invoke({
        "messages": [
            SystemMessage(content="你是一个购物助手，可以搜索商品和计算折扣。请用中文回答。"),
            HumanMessage(content=user_input),
        ]
    })

    # 打印最终回答（最后一条 AI 消息）
    final_message = result["messages"][-1]
    print(f"\n🤖 助手: {final_message.content}")


if __name__ == "__main__":
    # 场景1：搜索商品
    chat("我想买个耳机，有什么推荐？")

    # 场景2：搜索 + 计算折扣（多步骤）
    chat("帮我查一下手机，然后算算 iPhone 15 打 85 折多少钱")

    # 场景3：不需要工具
    chat("你好，你能帮我做什么？")

    print(f"\n{'='*60}")
    print("""
    本节的图结构：
    
    START → chatbot → (有工具调用?) → tools → chatbot → ... → END
                    → (无工具调用?) → END
    
    这就是一个"受控的 Agent"：
    - 整体流程由图控制（chatbot ↔ tools 循环）
    - 具体决策由 LLM 做（选什么工具、传什么参数）
    - 你可以在任何节点加入自定义逻辑（日志、审核、限流等）
    """)
