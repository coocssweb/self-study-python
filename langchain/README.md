# LangChain 学习

学习 LangChain 框架的基础用法，理解它如何封装 LLM 调用。

使用 DeepSeek 作为底层模型（通过 langchain-openai 兼容层）。

## 环境准备

```bash
python -m pip install langchain langchain-openai
```

## 设置 API Key

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-你的密钥"
```

## 文件列表

```
01_basic.py    — 第一次用 LangChain 调 LLM（对比原生 API）
02_prompt.py   — PromptTemplate 提示词模板
03_chain.py    — Chain 链式调用（LCEL 管道语法）
04_output.py   — OutputParser 输出解析（让 LLM 返回结构化数据）
05_memory.py   — Memory 对话记忆（多轮对话管理）
```

## 运行

```bash
python langchain/01_basic.py
```

## 前置知识

建议先学完 `llm_api/` 目录下的内容，理解 Chat Completion API 的基本概念。
