# ============================================================
# RAG 第三课 — 向量数据库 (ChromaDB)
# ============================================================
# 运行: python rag/03_vector_store.py
# ============================================================
# 核心问题: Embedding 向量生成了，存哪里？怎么快速检索？
#
# 第一课里我们手动遍历计算余弦相似度，数据量大了根本不行。
# 向量数据库专门干这个事：存向量、建索引、快速检索 Top-K。
#
# 类比前端: 向量数据库就像 Elasticsearch，
# 只不过 ES 做的是关键词倒排索引，向量数据库做的是向量近似搜索。
# ============================================================

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# --- 如果你想用 DeepSeek Embedding API，取消下面的注释 ---
# import os
# from langchain_openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com",
#     model="deepseek-chat",
# )

# 初始化 Embedding 模型
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)


# ============================================================
# 1. 准备数据 — 模拟一个知识库
# ============================================================

print("1. 准备知识库数据:")

# 模拟一份 Python 学习文档
documents = [
    Document(
        page_content="""Python的列表(list)是最常用的数据结构。列表是有序的、可变的，可以包含任意类型的元素。
创建列表用方括号: fruits = ["苹果", "香蕉", "橙子"]。
常用操作: append()添加元素, pop()删除元素, sort()排序, len()获取长度。
列表推导式是Python的特色语法: squares = [x**2 for x in range(10)]。""",
        metadata={"source": "python_basics.md", "topic": "列表"},
    ),
    Document(
        page_content="""Python的字典(dict)用于存储键值对。字典是无序的(Python 3.7+保持插入顺序)、可变的。
创建字典: person = {"name": "小明", "age": 25}。
常用操作: get()安全取值, keys()获取所有键, values()获取所有值, items()获取键值对。
字典推导式: {k: v for k, v in pairs}。""",
        metadata={"source": "python_basics.md", "topic": "字典"},
    ),
    Document(
        page_content="""Python的装饰器(decorator)是一种语法糖，用于修改函数的行为。
装饰器本质上是一个高阶函数，接收函数作为参数，返回新函数。
使用@语法: @timer 等价于 func = timer(func)。
常见用途: 日志记录、权限验证、缓存、计时、重试机制。
functools.wraps可以保留原函数的元信息。""",
        metadata={"source": "python_advanced.md", "topic": "装饰器"},
    ),
    Document(
        page_content="""Python的生成器(generator)用于惰性求值，节省内存。
用yield关键字定义生成器函数，每次调用next()时执行到下一个yield。
生成器表达式: (x**2 for x in range(10))，注意用圆括号不是方括号。
适用场景: 处理大文件、无限序列、数据流管道。
类比前端: 类似JavaScript的Generator和Iterator协议。""",
        metadata={"source": "python_advanced.md", "topic": "生成器"},
    ),
    Document(
        page_content="""LangChain是一个用于构建LLM应用的Python框架。
核心概念: Chain(链式调用)、Prompt Template(提示词模板)、OutputParser(输出解析)、Memory(记忆)。
LCEL管道语法: chain = prompt | llm | parser，类似Linux管道。
LangChain封装了各种LLM的调用接口，切换模型只需改配置。""",
        metadata={"source": "langchain_guide.md", "topic": "LangChain"},
    ),
    Document(
        page_content="""RAG(检索增强生成)是让LLM基于外部知识回答问题的技术。
核心流程: 文档切片 → Embedding向量化 → 存入向量数据库 → 用户提问时检索 → 拼入prompt生成回答。
优势: 不需要微调模型，知识可以实时更新，成本低。
适用场景: 企业知识库问答、文档助手、客服机器人。""",
        metadata={"source": "rag_tutorial.md", "topic": "RAG"},
    ),
]

print(f"   共 {len(documents)} 篇文档")

# 切片
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30,
    separators=["。\n", "。", "\n", "，", " ", ""],
)

split_docs = splitter.split_documents(documents)
print(f"   切片后: {len(split_docs)} 个 chunk")


# ============================================================
# 2. 创建向量数据库 (内存模式)
# ============================================================

print("\n2. 创建 Chroma 向量数据库 (内存模式):")

# from_documents: 一步完成 向量化 + 存储
vector_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    # 不指定 persist_directory 就是纯内存模式，程序退出就没了
)

print(f"   ✓ 向量数据库创建成功")
print(f"   存储了 {vector_store._collection.count()} 个向量")


# ============================================================
# 3. 相似度搜索 — similarity_search
# ============================================================

print("\n3. 相似度搜索:")

query = "Python列表怎么用？"
results = vector_store.similarity_search(query, k=3)  # 取 Top 3

print(f"   查询: 「{query}」")
print(f"   找到 {len(results)} 条相关结果:\n")

for i, doc in enumerate(results):
    print(f"   --- 结果 {i + 1} ---")
    print(f"   来源: {doc.metadata.get('source', '未知')}")
    print(f"   主题: {doc.metadata.get('topic', '未知')}")
    print(f"   内容: {doc.page_content[:80]}...")
    print()


# ============================================================
# 4. 带分数的搜索 — similarity_search_with_score
# ============================================================

print("4. 带相似度分数的搜索:")

query = "怎么让LLM回答更准确？"
results_with_scores = vector_store.similarity_search_with_score(query, k=5)

print(f"   查询: 「{query}」\n")

for doc, score in results_with_scores:
    # Chroma 返回的是 L2 距离，越小越相似（和余弦相似度相反）
    print(f"   距离: {score:.4f} | {doc.metadata.get('topic', '?')} | {doc.page_content[:50]}...")

print("""
   注意: Chroma 默认返回的是 L2 距离（欧氏距离），越小越相似。
   如果想用余弦相似度，创建时指定:
   Chroma(..., collection_metadata={"hnsw:space": "cosine"})
""")


# ============================================================
# 5. 元数据过滤 — 缩小搜索范围
# ============================================================

print("5. 元数据过滤:")

# 只在 python_advanced.md 里搜索
query = "函数相关的高级特性"
results = vector_store.similarity_search(
    query,
    k=3,
    filter={"source": "python_advanced.md"},  # 只搜这个文件
)

print(f"   查询: 「{query}」(限定来源: python_advanced.md)")
for doc in results:
    print(f"   [{doc.metadata['topic']}] {doc.page_content[:60]}...")

print("""
   元数据过滤在实际项目中很有用:
   - 按文件来源过滤: 只搜某个文档
   - 按时间过滤: 只搜最近更新的内容
   - 按分类过滤: 只搜某个主题
   类比前端: 就像 SQL 的 WHERE 条件，先过滤再排序。
""")


# ============================================================
# 6. 持久化存储 — 数据不丢失
# ============================================================

print("6. 持久化存储:")

import os
import shutil

persist_dir = os.path.join(os.path.dirname(__file__), "chroma_data")

# 清理旧数据（演示用）
if os.path.exists(persist_dir):
    shutil.rmtree(persist_dir)

# 创建持久化的向量数据库
persistent_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    persist_directory=persist_dir,  # 指定存储目录
)

print(f"   ✓ 数据已持久化到: {persist_dir}")

# 模拟"重新加载" — 实际项目中就是重启程序后加载
loaded_store = Chroma(
    persist_directory=persist_dir,
    embedding_function=embeddings,
)

# 验证数据还在
results = loaded_store.similarity_search("Python列表", k=1)
print(f"   ✓ 重新加载后搜索正常: {results[0].page_content[:40]}...")

# 清理演示数据
shutil.rmtree(persist_dir)
print(f"   ✓ 演示数据已清理")


# ============================================================
# 7. 作为 Retriever 使用 — 接入 Chain
# ============================================================

print("\n7. 转换为 Retriever (接入 LangChain Chain):")

# 向量数据库 → Retriever，就可以接入 LangChain 的 Chain 了
retriever = vector_store.as_retriever(
    search_type="similarity",  # 相似度搜索
    search_kwargs={"k": 3},    # 返回 Top 3
)

# Retriever 的 invoke 方法接收查询字符串，返回 Document 列表
docs = retriever.invoke("装饰器怎么用？")

print(f"   Retriever 返回 {len(docs)} 个文档:")
for doc in docs:
    print(f"   [{doc.metadata.get('topic')}] {doc.page_content[:50]}...")

print("""
   Retriever 是 RAG Chain 的关键组件:
   chain = retriever | format_docs | prompt | llm | parser
   下一课就用 Retriever 构建完整的 RAG Chain。
""")


# ============================================================
# 8. 其他搜索类型
# ============================================================

print("8. 其他搜索类型:")

# MMR (最大边际相关性) — 结果更多样化
mmr_retriever = vector_store.as_retriever(
    search_type="mmr",  # Maximal Marginal Relevance
    search_kwargs={
        "k": 3,              # 最终返回 3 个
        "fetch_k": 10,       # 先取 10 个候选
        "lambda_mult": 0.5,  # 多样性参数: 0=最多样, 1=最相关
    },
)

docs = mmr_retriever.invoke("Python有哪些高级特性？")

print(f"   MMR 搜索结果 (更多样化):")
for doc in docs:
    print(f"   [{doc.metadata.get('topic')}] {doc.page_content[:50]}...")

print("""
   similarity vs MMR:
   - similarity: 返回最相似的 K 个，可能内容重复
   - MMR: 在相关性和多样性之间平衡，结果覆盖面更广

   类比: similarity 像搜索引擎只看相关度排序，
   MMR 像推荐系统，既要相关又要多样。
""")


# ============================================================
# 总结
# ============================================================

print("=" * 50)
print("向量数据库要点:")
print("=" * 50)
print("""
1. Chroma 是轻量级向量数据库，适合开发和小规模项目
   - 内存模式: 快速原型验证
   - 持久化模式: 数据不丢失

2. 核心操作:
   - from_documents(): 批量导入文档
   - similarity_search(): 相似度搜索
   - similarity_search_with_score(): 带分数的搜索
   - as_retriever(): 转成 Retriever 接入 Chain

3. 搜索类型:
   - similarity: 纯相似度排序
   - mmr: 相关性 + 多样性平衡

4. 元数据过滤: 用 filter 参数缩小搜索范围

5. 生产环境的向量数据库选择:
   - Chroma: 轻量，适合原型和小项目
   - Milvus: 高性能，适合大规模数据
   - Pinecone: 全托管云服务，免运维
   - Weaviate: 功能丰富，支持混合搜索
   - pgvector: PostgreSQL 扩展，适合已有 PG 的团队

6. 下一步: 把 Retriever 接入 Chain，构建完整 RAG 流程
""")
