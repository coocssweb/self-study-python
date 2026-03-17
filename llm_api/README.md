# LLM API 学习

学习 Chat Completion API 的基础用法 (使用 DeepSeek)。

DeepSeek 的 API 兼容 OpenAI 格式，所以用的是 openai 这个 Python 库。
学会了 DeepSeek 的调用方式，切换到其他兼容 OpenAI 格式的模型 (如通义千问、智谱、Moonshot) 只需要改 base_url 和 model。

## 环境准备

```bash
python -m pip install openai
```

## 设置 API Key

```bash
# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-你的密钥"

# Linux/Mac
export DEEPSEEK_API_KEY=sk-你的密钥
```

API Key 在 https://platform.deepseek.com/api_keys 获取。

## 文件列表

```
01_basic.py        — 第一次调用 Chat Completion API
02_params.py       — temperature、max_tokens 等核心参数
03_messages.py     — system/user/assistant 消息角色详解
04_stream.py       — 流式输出 (打字机效果)
05_multi_turn.py   — 多轮对话
```

## 运行

```bash
python llm_api/01_basic.py
```
