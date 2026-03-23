# ============================================================
# LLM大模型
# ============================================================
import os
from openai import OpenAI

client = OpenAI(
    api_key = os.getenv("DEEPSEEK_API_KEY"),
    base_url = "https://api.deepseek.com"
)

