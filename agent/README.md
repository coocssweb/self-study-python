# Agent 学习 (智能体)

Agent = 能自主决策和执行任务的 AI 系统。

核心思路：LLM 不再只是"你问我答"，而是能"思考 → 决定用什么工具 → 执行 → 观察结果 → 继续思考"。

类比前端：Agent 就像一个带路由和状态机的应用。
- LLM 是路由器，根据输入决定走哪条路
- Tools 是各个页面组件，负责具体执行
- Agent Executor 是 App Shell，管理整个生命周期

## 为什么要学 Agent？

RAG 解决了"让 LLM 读资料"的问题，但现实场景往往需要：
- 查完资料还要调 API 执行操作
- 一个问题需要分多步完成
- 根据中间结果动态调整策略

Agent 就是让 LLM 从"回答问题"升级到"完成任务"。

## 环境准备

```bash
# 安装依赖
pip install langchain langchain-openai langchain-community langgraph
```

## 文件列表

```
01_function_calling.py  — Function Calling 基础：LLM 如何调用函数
02_tools.py             — 自定义工具：用 @tool 装饰器定义 Agent 可用的工具
03_react_agent.py       — ReAct Agent：推理 + 行动循环，Agent 的核心模式
04_langgraph_basic.py   — LangGraph 入门：用图结构编排 Agent 工作流
05_langgraph_tool.py    — LangGraph + 工具：在图节点中集成工具调用
06_multi_agent.py       — 多 Agent 协作：多个 Agent 分工合作完成复杂任务
```

## 前置知识

建议先学完以下内容：
- `langchain/` — 特别是 Chain 和 OutputParser
- `rag/` — 理解检索增强，Agent 中经常会把 RAG 作为一个工具

## 运行

```bash
python agent/01_function_calling.py
```
