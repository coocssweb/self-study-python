"""
06 - 多 Agent 协作：让多个 Agent 分工合作

前面的例子都是单个 Agent 干所有事。
实际复杂场景中，一个 Agent 很难面面俱到，就像一个全栈工程师不可能什么都精通。

解决方案：多个专业 Agent 协作，各司其职。

类比前端：
- 单 Agent ≈ 单体应用（一个 App 干所有事）
- 多 Agent ≈ 微前端架构（每个子应用负责一个领域，主应用负责调度）

常见的多 Agent 模式：
1. 主管模式（Supervisor）：一个主管 Agent 分配任务给专业 Agent
2. 顺序模式（Sequential）：Agent 按顺序接力，像流水线
3. 辩论模式（Debate）：多个 Agent 互相讨论，得出更好的结论

本节实现"主管模式"：一个 Supervisor 根据用户需求，把任务分给不同的专业 Agent。
"""

import os
from typing import TypedDict, Literal, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# ============================================================
# 初始化 LLM
# ============================================================
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# ============================================================
# 定义状态
# ============================================================

class MultiAgentState(TypedDict):
    messages: Annotated[list, add_messages]  # 消息历史
    next_agent: str                          # 下一个要执行的 Agent
    task: str                                # 用户原始任务
    results: dict                            # 各 Agent 的执行结果


# ============================================================
# 定义专业 Agent（每个 Agent 有自己的系统提示词和专业领域）
# ============================================================

def researcher_agent(state: MultiAgentState) -> dict:
    """研究员 Agent：负责信息收集和分析"""
    print("\n🔍 研究员 Agent 开始工作...")

    response = llm.invoke([
        SystemMessage(content="""你是一个专业的研究员。
你的职责是对给定主题进行深入分析，提供关键信息和数据。
请用简洁的要点形式输出，不超过 150 字。"""),
        HumanMessage(content=f"请研究以下主题：{state['task']}")
    ])

    results = state.get("results", {})
    results["research"] = response.content
    print(f"  研究结果: {response.content[:100]}...")
    return {"results": results}


def writer_agent(state: MultiAgentState) -> dict:
    """写作 Agent：负责内容创作"""
    print("\n✍️ 写作 Agent 开始工作...")

    # 拿到研究员的成果作为参考
    research = state.get("results", {}).get("research", "无参考资料")

    response = llm.invoke([
        SystemMessage(content="""你是一个专业的技术写作者。
根据提供的研究资料，撰写一篇简短的技术文章。
要求：通俗易懂，200 字以内。"""),
        HumanMessage(content=f"主题：{state['task']}\n\n参考资料：\n{research}")
    ])

    results = state.get("results", {})
    results["article"] = response.content
    print(f"  文章: {response.content[:100]}...")
    return {"results": results}


def reviewer_agent(state: MultiAgentState) -> dict:
    """审核 Agent：负责质量把关"""
    print("\n🔍 审核 Agent 开始工作...")

    article = state.get("results", {}).get("article", "无文章内容")

    response = llm.invoke([
        SystemMessage(content="""你是一个严格的内容审核员。
请审核文章的准确性、可读性和完整性。
给出评分（1-10）和简短的改进建议，不超过 100 字。"""),
        HumanMessage(content=f"请审核以下文章：\n{article}")
    ])

    results = state.get("results", {})
    results["review"] = response.content
    print(f"  审核意见: {response.content[:100]}...")
    return {"results": results}


# ============================================================
# Supervisor（主管）：决定任务分配
# ============================================================

def supervisor(state: MultiAgentState) -> dict:
    """主管 Agent：分析任务，决定下一步交给谁"""
    results = state.get("results", {})

    # 简单的路由逻辑：按顺序分配
    # 实际项目中，这里可以用 LLM 来动态决策
    if "research" not in results:
        next_agent = "researcher"
        print("\n📋 主管: 先让研究员收集资料")
    elif "article" not in results:
        next_agent = "writer"
        print("\n📋 主管: 资料有了，让写手写文章")
    elif "review" not in results:
        next_agent = "reviewer"
        print("\n📋 主管: 文章写好了，让审核员把关")
    else:
        next_agent = "done"
        print("\n📋 主管: 所有工作完成")

    return {"next_agent": next_agent}


# ============================================================
# 路由函数：根据 supervisor 的决定走不同分支
# ============================================================

def route_to_agent(state: MultiAgentState) -> str:
    """根据 next_agent 字段路由到对应节点"""
    return state["next_agent"]


# ============================================================
# 构建多 Agent 图
# ============================================================

workflow = StateGraph(MultiAgentState)

# 添加节点
workflow.add_node("supervisor", supervisor)
workflow.add_node("researcher", researcher_agent)
workflow.add_node("writer", writer_agent)
workflow.add_node("reviewer", reviewer_agent)

# 入口 → 主管
workflow.add_edge(START, "supervisor")

# 主管通过条件边分配任务
workflow.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {
        "researcher": "researcher",
        "writer": "writer",
        "reviewer": "reviewer",
        "done": END,
    }
)

# 每个 Agent 完成后回到主管，由主管决定下一步
workflow.add_edge("researcher", "supervisor")
workflow.add_edge("writer", "supervisor")
workflow.add_edge("reviewer", "supervisor")

# 编译
app = workflow.compile()

# ============================================================
# 运行
# ============================================================

if __name__ == "__main__":
    print("=== 多 Agent 协作演示 ===")
    print("任务：写一篇关于 RAG 技术的短文\n")

    result = app.invoke({
        "messages": [],
        "next_agent": "",
        "task": "RAG（检索增强生成）技术的原理和应用场景",
        "results": {},
    })

    # 打印最终成果
    print(f"\n{'='*60}")
    print("📊 最终成果汇总")
    print(f"{'='*60}")

    results = result["results"]
    print(f"\n🔍 研究资料:\n{results.get('research', '无')}")
    print(f"\n📄 文章:\n{results.get('article', '无')}")
    print(f"\n✅ 审核意见:\n{results.get('review', '无')}")

    print(f"\n{'='*60}")
    print("""
    多 Agent 架构的优势：
    
    1. 专业分工 — 每个 Agent 专注一个领域，提示词更精准
    2. 可扩展 — 新增能力只需加一个 Agent，不影响其他
    3. 可替换 — 某个 Agent 效果不好，换一个实现就行
    4. 可观测 — 每个 Agent 的输入输出都清晰可见
    
    类比前端微服务：
    - Supervisor = API Gateway（路由分发）
    - 各专业 Agent = 微服务（独立部署、独立迭代）
    - State = 消息队列（Agent 之间通过状态传递数据）
    """)
