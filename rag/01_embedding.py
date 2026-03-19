# ============================================================
# RAG 第一课 — Embedding 向量化基础
# ============================================================
# 运行: python rag/01_embedding.py
# ============================================================
# 核心问题: 计算机怎么理解"语义相似"？
#
# 人类一看就知道"我喜欢吃苹果"和"苹果很好吃"意思接近，
# 但计算机只认数字。Embedding 就是把文本变成一组数字（向量），
# 语义相近的文本，向量也相近。
#
# 类比前端: 你用过 CSS 的 rgb(255, 0, 0) 表示红色吧？
# Embedding 类似 — 用一组数字来"编码"文本的含义。
# 只不过 RGB 是 3 个维度，Embedding 通常是 384~1536 个维度。
# ============================================================

import numpy as np


# ============================================================
# 1. 什么是 Embedding？直观理解
# ============================================================

print("1. 什么是 Embedding？")
print("""
   文本 → Embedding 模型 → 向量 (一组浮点数)

   "我喜欢Python"  → [0.12, -0.34, 0.56, ..., 0.78]  (384维)
   "Python很好用"   → [0.11, -0.32, 0.55, ..., 0.77]  (384维)  ← 很接近!
   "今天天气不错"   → [0.89, 0.23, -0.45, ..., 0.12]  (384维)  ← 差很远!

   向量之间的"距离"反映了语义的相似程度。
   这就是 RAG 能"搜到相关内容"的数学基础。
""")


# ============================================================
# 2. 用 HuggingFace 本地模型生成 Embedding
# ============================================================

print("2. 生成 Embedding 向量:")

from langchain_huggingface import HuggingFaceEmbeddings

# 本地模型，免费，首次运行自动下载 (~80MB)
# 如果下载慢，可以设置镜像: HF_ENDPOINT=https://hf-mirror.com
embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
)

# --- 如果你想用 DeepSeek Embedding API，取消下面的注释 ---
# import os
# from langchain_openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com",
#     model="deepseek-chat",  # DeepSeek 的 embedding 模型
# )

# 单条文本向量化
text = "Python是一种流行的编程语言"
vector = embeddings.embed_query(text)

print(f"   文本: {text}")
print(f"   向量维度: {len(vector)}")
print(f"   前5个值: {vector[:5]}")
print(f"   值的范围: [{min(vector):.4f}, {max(vector):.4f}]")


# ============================================================
# 3. 批量向量化
# ============================================================

print("\n3. 批量向量化:")

texts = [
    "Python是一种流行的编程语言",
    "JavaScript用于前端开发",
    "今天天气真好适合出去玩",
    "机器学习是人工智能的分支",
    "我想吃火锅",
]

vectors = embeddings.embed_documents(texts)

print(f"   文本数量: {len(texts)}")
print(f"   向量数量: {len(vectors)}")
print(f"   每个向量维度: {len(vectors[0])}")


# ============================================================
# 4. 余弦相似度 — 衡量两个向量有多"像"
# ============================================================

print("\n4. 余弦相似度:")
print("""
   余弦相似度 = 两个向量夹角的余弦值
   范围: -1 到 1
   1 = 完全相同方向 (语义一致)
   0 = 正交 (毫无关系)
  -1 = 完全相反方向

   类比: 就像两个箭头的方向，方向越一致，相似度越高。
""")


def cosine_similarity(vec1, vec2):
    """计算余弦相似度"""
    a = np.array(vec1)
    b = np.array(vec2)
    print('----------------------------------- a', a)
    print('----------------------------------- b', b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 计算所有文本两两之间的相似度
print("   各文本之间的相似度:")
for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        sim = cosine_similarity(vectors[i], vectors[j])
        print(f"   {sim:.4f} | 「{texts[i]}」 vs 「{texts[j]}」")

print("""
   观察:
   - "Python编程语言" vs "JavaScript前端开发" → 相似度较高 (都是编程)
   - "Python编程语言" vs "今天天气真好" → 相似度较低 (不相关)
   - "Python编程语言" vs "机器学习AI" → 中等 (技术领域相关)
""")


# ============================================================
# 5. 实战：语义搜索 (RAG 的核心原理)
# ============================================================

print("5. 语义搜索 — RAG 的核心原理:")
print("""
   传统搜索: 关键词匹配 (搜"Python" 只能匹配包含"Python"的文本)
   语义搜索: 向量相似度 (搜"编程语言" 能匹配到"Python"、"JavaScript")
""")

# 模拟一个小型知识库
knowledge_base = [
    "LangChain是一个用于构建LLM应用的框架",
    "RAG通过检索外部知识来增强LLM的回答",
    "向量数据库用于存储和检索Embedding向量",
    "Python的装饰器是一种语法糖，用于修改函数行为",
    "React是一个用于构建用户界面的JavaScript库",
    "Docker是一个容器化平台，用于打包和部署应用",
    "Transformer是现代LLM的基础架构",
    "FastAPI是一个高性能的Python Web框架",
]

# 把知识库向量化
kb_vectors = embeddings.embed_documents(knowledge_base)

# 用户提问
query = "怎么让大模型回答更准确？"
query_vector = embeddings.embed_query(query)

# 计算相似度并排序
similarities = []
for i, kb_vec in enumerate(kb_vectors):
    sim = cosine_similarity(query_vector, kb_vec)
    similarities.append((sim, knowledge_base[i]))

similarities.sort(reverse=True)

print(f"   查询: 「{query}」")
print(f"   检索结果 (按相似度排序):")
for sim, text in similarities:
    marker = " ← 最相关" if sim == similarities[0][0] else ""
    print(f"     {sim:.4f} | {text}{marker}")

print("""
   这就是 RAG 的检索阶段:
   1. 用户提问 → 向量化
   2. 和知识库里每条内容计算相似度
   3. 取最相关的 Top-K 条
   4. 把这些内容塞进 prompt，让 LLM 回答

   当然，实际不会每次都遍历计算，向量数据库会用 ANN 算法加速。
   下一课讲文档切片，第三课讲向量数据库。
""")


# ============================================================
# 6. embed_query vs embed_documents 的区别
# ============================================================

print("6. embed_query vs embed_documents:")
print("""
   embeddings.embed_query("一段文本")
     → 返回一个向量 (list[float])
     → 用于: 用户的查询/问题

   embeddings.embed_documents(["文本1", "文本2", ...])
     → 返回多个向量 (list[list[float]])
     → 用于: 批量处理知识库文档

   为什么要分开？
   有些 Embedding 模型对"查询"和"文档"用不同的编码策略，
   查询通常更短，文档更长，分开处理效果更好。
   不过大部分模型（包括我们用的这个）两者结果是一样的。
""")


# ============================================================
# 总结
# ============================================================

print("=" * 50)
print("Embedding 要点:")
print("=" * 50)
print("""
1. Embedding 把文本变成向量 (一组浮点数)
   - 语义相近的文本，向量也相近
   - 这是 RAG "能搜到相关内容" 的数学基础

2. 余弦相似度衡量两个向量的相似程度
   - 1 = 完全相似, 0 = 无关, -1 = 完全相反

3. 语义搜索 vs 关键词搜索
   - 关键词: "Python" 只匹配包含 "Python" 的文本
   - 语义: "编程语言" 能匹配到 "Python"、"JavaScript"

4. Embedding 模型选择
   - 本地: sentence-transformers/all-MiniLM-L6-v2 (免费，384维)
   - 云端: OpenAI text-embedding-3-small (收费，1536维)
   - 维度越高不一定越好，要看具体场景

5. 下一步: 文档太长怎么办？→ 切片 (Text Splitting)
""")
