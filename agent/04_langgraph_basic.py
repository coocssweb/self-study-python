"""
04 - LangGraph 入门：用图结构编排工作流

上一节的 ReAct Agent 是"全自动"的，LLM 自己决定一切。
但实际项目中，你往往需要更精细的控制：
- 某些步骤必须按固定顺序执行
- 某些条件下走不同的分支
- 需要人工审核后才能继续

LangGraph 就是解决这个问题的。它用"图"来编排工作流。

类比前端：
- ReAct Agent ≈ 自动路由（LLM 决定去哪）
- LangGraph ≈ 手动路由配置（你定义路由表，但每个页面的内容由 LLM 生成）
- 更准确地说，LangGraph ≈ XState 状态机，节点是状态，边是转换条件

核心概念：
- Node（节点）：执行具体任务的函数
- Edge（边）：节点之间的连接，定义执行顺序
- Conditional Edge（条件边）：根据条件走不同路径
- State（状态）：在节点之间传递的数据
"""

import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

# ============================================================
# 初始化 LLM
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 第一步：定义状态（State）
# 状态就是在各个节点之间传递的数据结构
# 类比前端：就像 Redux 的 store，或 Vue 的 reactive state
# ============================================================

class ArticleState(TypedDict):
    """文章处理工作流的状态"""
    topic: str           # 用户输入的主题
    outline: str         # 生成的大纲
    draft: str           # 生成的草稿
    review: str          # 审核意见
    final_article: str   # 最终文章
    status: str          # 当前状态


# ============================================================
# 第二步：定义节点（Node）
# 每个节点是一个函数，接收 state，返回更新后的 state
# 类比前端：每个节点就像一个 reducer，接收旧 state，返回新 state
# ============================================================

def generate_outline(state: ArticleState) -> dict:
    """节点1：生成文章大纲"""
    print("\n📝 正在生成大纲...")
    response = llm.invoke(
        f"请为主题「{state['topic']}」生成一个简短的文章大纲，包含 3 个要点。只输出大纲，不要其他内容。"
    )
    return {"outline": response.content, "status": "大纲已生成"}


def write_draft(state: ArticleState) -> dict:
    """节点2：根据大纲写草稿"""
    print("\n✍️ 正在写草稿...")
    response = llm.invoke(
        f"根据以下大纲写一篇短文（200字以内）：\n{state['outline']}"
    )
    return {"draft": response.content, "status": "草稿已完成"}


def review_article(state: ArticleState) -> dict:
    """节点3：审核文章"""
    print("\n🔍 正在审核...")
    response = llm.invoke(
        f"请审核以下文章，给出简短的改进建议（50字以内）：\n{state['draft']}"
    )
    return {"review": response.content, "status": "审核完成"}


def finalize(state: ArticleState) -> dict:
    """节点4：根据审核意见定稿"""
    print("\n✅ 正在定稿...")
    response = llm.invoke(
        f"根据审核意见修改文章。\n\n原文：\n{state['draft']}\n\n审核意见：\n{state['review']}\n\n请输出修改后的最终版本（200字以内）。"
    )
    return {"final_article": response.content, "status": "已定稿"}


# ============================================================
# 第三步：构建图（Graph）
# 把节点和边组装起来
# ============================================================

# 创建图，指定状态类型
workflow = StateGraph(ArticleState)

# 添加节点
workflow.add_node("generate_outline", generate_outline)
workflow.add_node("write_draft", write_draft)
workflow.add_node("review_article", review_article)
workflow.add_node("finalize", finalize)

# 添加边（定义执行顺序）
workflow.add_edge(START, "generate_outline")       # 入口 → 生成大纲
workflow.add_edge("generate_outline", "write_draft")  # 生成大纲 → 写草稿
workflow.add_edge("write_draft", "review_article")    # 写草稿 → 审核
workflow.add_edge("review_article", "finalize")       # 审核 → 定稿
workflow.add_edge("finalize", END)                    # 定稿 → 结束

# 编译图（类似前端的 build 过程）
app = workflow.compile()

# ============================================================
# 运行工作流
# ============================================================

if __name__ == "__main__":
    print("=== LangGraph 文章生成工作流 ===\n")

    # 传入初始状态，启动工作流
    result = app.invoke({
        "topic": "为什么前端工程师应该学习 AI",
        "outline": "",
        "draft": "",
        "review": "",
        "final_article": "",
        "status": ""
    })

    # 打印最终结果
    print(f"\n{'='*60}")
    print(f"📋 大纲:\n{result['outline']}")
    print(f"\n📄 最终文章:\n{result['final_article']}")
    print(f"\n📊 状态: {result['status']}")

    # ============================================================
    # 关键理解
    # ============================================================
    print(f"\n{'='*60}")
    print("""
    LangGraph vs ReAct Agent：
    
    ReAct Agent（上一节）：
    - LLM 完全自主决策
    - 适合简单的工具调用场景
    - 不可预测，难以调试
    
    LangGraph（本节）：
    - 你定义流程，LLM 负责每个步骤的具体执行
    - 适合有固定流程的业务场景
    - 可预测，容易调试和监控
    
    类比：
    - ReAct = 给实习生一堆工具，让他自己想办法
    - LangGraph = 给实习生一份 SOP，每一步该做什么写清楚
    """)
