# ============================================================
# LLM大模型
# 使用 LangChain 封装的 ChatOpenAI，兼容 LCEL 管道调用
# ============================================================
import os
from langchain_openai import ChatOpenAI

# ChatOpenAI 是 LangChain 对 OpenAI 兼容接口的封装，实现了 Runnable 协议
# 可以直接用 | 操作符串进 chain
client = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
)
