# ============================================================
# RAG 第五课 — 进阶 RAG 技巧
# ============================================================
# 运行: python rag/05_advanced_rag.py
# ============================================================
# 第四课跑通了基础 RAG，但实际项目中会遇到很多问题:
#
# 1. 用户问题太模糊，检索不到好结果
# 2. 检索到的内容有噪音，LLM 被误导
# 3. 单次检索不够，需要多角度搜索
# 4. 需要结合对话历史来理解问题
#
# 这一课讲几个实用的优化技巧。
#
# 类比前端: 基础 RAG 像是写了个能跑的 MVP，
# 这一课是做性能优化和用户体验提升。
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0,
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

# 准备知识库（复用第四课的数据，内容更丰富一些）
knowledge_docs = [
    Document(page_content="""FastAPI 是一个现代的 Python Web 框架，基于 Starlette 和 Pydantic。
核心特点：自动生成 API 文档（Swagger UI）、原生支持异步、类型注解驱动、性能接近 Go。
安装: pip install fastapi uvicorn。启动: uvicorn main:app --reload。
适合构建 RESTful API 和微服务。""", metadata={"topic": "FastAPI基础"}),

    Document(page_content="""FastAPI 路由定义使用装饰器: @app.get("/path"), @app.post("/path")。
路径参数: @app.get("/users/{user_id}")，自动校验类型。
查询参数: 函数参数加默认值即可，如 skip: int = 0。
请求体: 用 Pydantic BaseModel 定义，自动校验和文档生成。""", metadata={"topic": "FastAPI路由"}),

    Document(page_content="""FastAPI 依赖注入用 Depends() 实现，支持嵌套依赖。
常见用途: 数据库会话管理、用户认证、权限校验。
示例: async def get_current_user(token: str = Depends(oauth2_scheme))。
依赖可以是函数、类、生成器(yield)。生成器依赖支持清理逻辑。""", metadata={"topic": "FastAPI依赖注入"}),

    Document(page_content="""FastAPI 中间件处理请求/响应的通用逻辑，执行顺序是洋葱模型。
CORS 配置: app.add_middleware(CORSMiddleware, allow_origins=["*"])。
自定义中间件: @app.middleware("http")，可以记录日志、统计耗时。
和 Express/Koa 的中间件概念一样。""", metadata={"topic": "FastAPI中间件"}),

    Document(page_content="""FastAPI 支持 WebSocket 实时通信。
定义: @app.websocket("/ws")，参数是 WebSocket 对象。
用法: await websocket.accept(), await websocket.receive_text(), await websocket.send_text()。
适合聊天、实时通知、数据推送等场景。""", metadata={"topic": "FastAPI WebSocket"}),

    Document(page_content="""FastAPI 的测试用 TestClient（基于 httpx）。
from fastapi.testclient import TestClient; client = TestClient(app)。
支持同步和异步测试，可以测试路由、中间件、WebSocket。
推荐用 pytest 框架，配合 fixture 管理测试数据。""", metadata={"topic": "FastAPI测试"}),

    Document(page_content="""FastAPI 部署方案:
开发环境: uvicorn main:app --reload。
生产环境: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app。
Docker 部署: 用官方 Python 镜像，多阶段构建减小体积。
云部署: 支持 AWS Lambda、Google Cloud Run、Azure Functions 等 Serverless 方案。""", metadata={"topic": "FastAPI部署"}),
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=250, chunk_overlap=40,
    separators=["。\n", "。", "\n", "，", ""],
)
split_docs = splitter.split_documents(knowledge_docs)

vector_store = Chroma.from_documents(
    documents=split_docs, embedding=embeddings,
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})


def format_docs(docs: list[Document]) -> str:
    """格式化文档列表"""
    return "\n\n".join(
        f"[{doc.metadata.get('topic', '未知')}] {doc.page_content}"
        for doc in docs
    )


# ============================================================
# 1. 多查询检索 (Multi-Query Retriever)
# ============================================================

print("1. 多查询检索 (Multi-Query):")
print("""
   问题: 用户的提问方式可能不是最佳的检索 query。
   比如用户问"FastAPI快不快"，但文档里写的是"性能接近Go"。

   解决: 让 LLM 把用户问题改写成多个不同角度的查询，
   分别检索，合并去重，覆盖面更广。

   类比前端: 就像搜索引擎的"同义词扩展"，
   搜"JS框架"时也会匹配"JavaScript库"。
""")

# 用 LLM 生成多个查询
multi_query_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个搜索查询优化助手。
用户会给你一个问题，请从不同角度生成 3 个搜索查询，用于检索相关文档。
每个查询一行，不要编号，不要解释。"""),
    ("user", "{question}"),
])

multi_query_chain = multi_query_prompt | llm | StrOutputParser()


def multi_query_retrieve(question: str) -> list[Document]:
    """多查询检索: 生成多个查询 → 分别检索 → 合并去重"""
    # 生成多个查询
    queries_text = multi_query_chain.invoke({"question": question})
    queries = [q.strip() for q in queries_text.strip().split("\n") if q.strip()]

    print(f"   原始问题: {question}")
    print(f"   扩展查询:")
    for q in queries:
        print(f"     - {q}")

    # 分别检索
    all_docs = []
    seen_contents = set()

    for query in queries:
        docs = retriever.invoke(query)
        for doc in docs:
            # 用内容哈希去重
            content_hash = hash(doc.page_content)
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                all_docs.append(doc)

    print(f"   去重后共 {len(all_docs)} 个文档片段")
    return all_docs


# 测试
docs = multi_query_retrieve("FastAPI快不快？适合什么场景？")
print()


# ============================================================
# 2. 上下文压缩 (Contextual Compression)
# ============================================================

print("2. 上下文压缩:")
print("""
   问题: 检索到的 chunk 可能很长，但只有一小部分和问题相关。
   把整个 chunk 塞进 prompt 会浪费 token，还可能引入噪音。

   解决: 用 LLM 对检索到的内容做"压缩"，只保留和问题相关的部分。

   类比前端: 就像 GraphQL 只请求需要的字段，而不是 REST 返回整个对象。
""")

compress_prompt = ChatPromptTemplate.from_messages([
    ("system", """从以下文档片段中，提取与用户问题直接相关的信息。
只保留相关内容，去掉无关的部分。如果整段都不相关，回复"无相关信息"。
保持原文表述，不要改写或添加信息。"""),
    ("user", """文档片段:
{document}

用户问题: {question}

相关内容:"""),
])

compress_chain = compress_prompt | llm | StrOutputParser()


def compress_docs(question: str, docs: list[Document]) -> str:
    """压缩检索到的文档，只保留相关内容"""
    compressed_parts = []

    for doc in docs:
        compressed = compress_chain.invoke({
            "document": doc.page_content,
            "question": question,
        })
        if "无相关信息" not in compressed:
            compressed_parts.append(compressed)

    return "\n\n".join(compressed_parts)


# 测试
question = "FastAPI怎么部署到生产环境？"
raw_docs = retriever.invoke(question)

print(f"   问题: {question}")
print(f"   原始检索内容 ({sum(len(d.page_content) for d in raw_docs)} 字符):")
for doc in raw_docs:
    print(f"     {doc.page_content[:60]}...")

compressed = compress_docs(question, raw_docs)
print(f"\n   压缩后 ({len(compressed)} 字符):")
print(f"     {compressed[:200]}...")


# ============================================================
# 3. 查询重写 (Query Rewriting)
# ============================================================

print("\n\n3. 查询重写 — 处理模糊问题:")
print("""
   问题: 用户的提问可能很口语化或者太模糊。
   "那个东西怎么弄" → 检索不到任何有用的结果。

   解决: 先让 LLM 把模糊问题改写成清晰的检索查询。
""")

rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个查询优化助手。把用户的口语化问题改写成适合搜索的精确查询。
只输出改写后的查询，不要解释。"""),
    ("user", "{question}"),
])

rewrite_chain = rewrite_prompt | llm | StrOutputParser()

# 测试几个模糊问题
vague_questions = [
    "那个自动生成文档的功能怎么弄",
    "怎么让接口跑得更快",
    "测试怎么写",
]

for q in vague_questions:
    rewritten = rewrite_chain.invoke({"question": q})
    print(f"   原始: {q}")
    print(f"   改写: {rewritten}")

    # 用改写后的查询检索
    docs = retriever.invoke(rewritten)
    if docs:
        print(f"   检索到: [{docs[0].metadata.get('topic')}] {docs[0].page_content[:50]}...")
    print()


# ============================================================
# 4. 带对话历史的 RAG (Conversational RAG)
# ============================================================

print("4. 带对话历史的 RAG:")
print("""
   问题: 用户可能会追问，比如:
   Q1: "FastAPI怎么定义路由？"
   Q2: "那 POST 请求呢？"  ← "那"指的是什么？需要结合上文理解

   解决: 先用 LLM 结合对话历史，把追问改写成独立的完整问题，
   再用改写后的问题去检索。
""")

from langchain_core.messages import HumanMessage, AIMessage

# 历史感知的查询改写
contextualize_prompt = ChatPromptTemplate.from_messages([
    ("system", """根据对话历史和最新问题，生成一个独立的、完整的搜索查询。
如果最新问题已经是独立的，直接返回原问题。
只输出改写后的查询，不要解释。"""),
    ("user", """对话历史:
{chat_history}

最新问题: {question}

独立查询:"""),
])

contextualize_chain = contextualize_prompt | llm | StrOutputParser()

# RAG prompt
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个技术文档助手。基于参考资料回答问题。
只基于参考资料回答，不要编造。如果资料不足，说明无法回答。"""),
    ("user", """参考资料:
{context}

问题: {question}"""),
])


def conversational_rag(question: str, chat_history: list) -> str:
    """带对话历史的 RAG"""
    # 如果有历史，先改写问题
    if chat_history:
        history_text = "\n".join(
            f"{'用户' if isinstance(m, HumanMessage) else '助手'}: {m.content}"
            for m in chat_history
        )
        standalone_question = contextualize_chain.invoke({
            "chat_history": history_text,
            "question": question,
        })
        print(f"   (改写后的查询: {standalone_question})")
    else:
        standalone_question = question

    # 检索
    docs = retriever.invoke(standalone_question)
    context = format_docs(docs)

    # 生成回答
    answer = (rag_prompt | llm | StrOutputParser()).invoke({
        "context": context,
        "question": question,  # 用原始问题回答，更自然
    })

    return answer


# 模拟多轮对话
chat_history = []

q1 = "FastAPI怎么定义路由？"
print(f"   Q: {q1}")
a1 = conversational_rag(q1, chat_history)
print(f"   A: {a1}\n")
chat_history.extend([HumanMessage(content=q1), AIMessage(content=a1)])

q2 = "那怎么处理 POST 请求的请求体？"
print(f"   Q: {q2}")
a2 = conversational_rag(q2, chat_history)
print(f"   A: {a2}\n")
chat_history.extend([HumanMessage(content=q2), AIMessage(content=a2)])

q3 = "有没有自动校验的功能？"
print(f"   Q: {q3}")
a3 = conversational_rag(q3, chat_history)
print(f"   A: {a3}")


# ============================================================
# 5. 自定义评分 + 重排序 (Re-ranking)
# ============================================================

print("\n\n5. 重排序 (Re-ranking):")
print("""
   问题: 向量相似度不一定等于"真正相关"。
   Embedding 模型可能把"Python Web框架"和"Python数据分析"都判为高相似度，
   但用户问的是 Web 相关的问题。

   解决: 先用向量搜索取 Top-K 候选，再用 LLM 对候选做精细排序。
   这就是"粗筛 + 精排"的两阶段检索策略。

   类比前端: 就像电商搜索，先用 ES 召回 1000 个商品，
   再用推荐算法精排出 Top 20 展示给用户。
""")

rerank_prompt = ChatPromptTemplate.from_messages([
    ("system", """对以下文档片段按照与用户问题的相关性打分（0-10分）。
每个片段一行，格式: 分数|片段编号
只输出分数，不要解释。"""),
    ("user", """用户问题: {question}

文档片段:
{documents}

评分:"""),
])


def rerank_docs(question: str, docs: list[Document], top_k: int = 3) -> list[Document]:
    """用 LLM 对检索结果重排序"""
    if not docs:
        return []

    # 格式化文档供 LLM 评分
    docs_text = "\n".join(
        f"[{i}] {doc.page_content[:100]}"
        for i, doc in enumerate(docs)
    )

    # LLM 评分
    scores_text = (rerank_prompt | llm | StrOutputParser()).invoke({
        "question": question,
        "documents": docs_text,
    })

    # 解析分数
    scored_docs = []
    for line in scores_text.strip().split("\n"):
        try:
            parts = line.strip().split("|")
            if len(parts) == 2:
                score = float(parts[0].strip())
                idx = int(parts[1].strip())
                if 0 <= idx < len(docs):
                    scored_docs.append((score, docs[idx]))
        except (ValueError, IndexError):
            continue

    # 按分数降序排列
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    return [doc for _, doc in scored_docs[:top_k]]


# 测试: 先取 Top 6 候选，再精排到 Top 3
broad_retriever = vector_store.as_retriever(search_kwargs={"k": 6})
question = "FastAPI怎么做用户认证？"

candidates = broad_retriever.invoke(question)
print(f"   问题: {question}")
print(f"   粗筛候选 ({len(candidates)} 个):")
for doc in candidates:
    print(f"     [{doc.metadata.get('topic')}] {doc.page_content[:50]}...")

reranked = rerank_docs(question, candidates, top_k=3)
print(f"\n   精排结果 ({len(reranked)} 个):")
for doc in reranked:
    print(f"     [{doc.metadata.get('topic')}] {doc.page_content[:50]}...")


# ============================================================
# 6. 混合检索 (Hybrid Search)
# ============================================================

print("\n\n6. 混合检索策略:")
print("""
   向量搜索擅长语义匹配，但对精确关键词匹配不太行。
   比如搜索 "uvicorn" 这个具体的工具名，关键词搜索更准。

   混合检索 = 向量搜索 + 关键词搜索，取两者的并集。

   实现思路:
   1. 向量搜索: 语义相关的 Top-K
   2. 关键词搜索: 包含关键词的文档
   3. 合并去重，综合排序

   生产环境中，Elasticsearch + 向量搜索 是常见的混合方案。
   这里用简单的关键词匹配演示思路。
""")


def keyword_search(query: str, docs: list[Document], k: int = 3) -> list[Document]:
    """简单的关键词搜索"""
    keywords = query.lower().split()
    scored = []
    for doc in docs:
        content_lower = doc.page_content.lower()
        # 计算匹配到的关键词数量
        match_count = sum(1 for kw in keywords if kw in content_lower)
        if match_count > 0:
            scored.append((match_count, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored[:k]]


def hybrid_search(question: str, all_docs: list[Document], k: int = 3) -> list[Document]:
    """混合检索: 向量搜索 + 关键词搜索"""
    # 向量搜索
    vector_results = retriever.invoke(question)

    # 关键词搜索（在所有文档中搜索）
    keyword_results = keyword_search(question, all_docs, k=k)

    # 合并去重
    seen = set()
    merged = []
    for doc in vector_results + keyword_results:
        content_hash = hash(doc.page_content)
        if content_hash not in seen:
            seen.add(content_hash)
            merged.append(doc)

    return merged[:k]


# 测试
question = "uvicorn怎么启动"
print(f"   问题: {question}")

vector_only = retriever.invoke(question)
print(f"   纯向量搜索:")
for doc in vector_only[:2]:
    print(f"     [{doc.metadata.get('topic')}] {doc.page_content[:60]}...")

hybrid_results = hybrid_search(question, split_docs)
print(f"   混合搜索:")
for doc in hybrid_results[:2]:
    print(f"     [{doc.metadata.get('topic')}] {doc.page_content[:60]}...")


# ============================================================
# 总结
# ============================================================

print("\n\n" + "=" * 50)
print("进阶 RAG 技巧总结:")
print("=" * 50)
print("""
1. 多查询检索 (Multi-Query)
   - 把一个问题扩展成多个查询，覆盖更多角度
   - 适合: 用户问题比较宽泛时

2. 上下文压缩 (Contextual Compression)
   - 用 LLM 过滤检索结果中的无关内容
   - 适合: chunk 较大、噪音较多时

3. 查询重写 (Query Rewriting)
   - 把模糊/口语化的问题改写成精确查询
   - 适合: 面向普通用户的产品

4. 对话式 RAG (Conversational RAG)
   - 结合对话历史理解追问
   - 适合: 多轮对话场景

5. 重排序 (Re-ranking)
   - 粗筛 + 精排，两阶段检索
   - 适合: 对检索精度要求高的场景

6. 混合检索 (Hybrid Search)
   - 向量搜索 + 关键词搜索
   - 适合: 既有语义查询又有精确查询的场景

实际项目中，这些技巧可以组合使用:
  查询重写 → 多查询检索 → 重排序 → 上下文压缩 → LLM 生成

选择哪些技巧取决于:
  - 数据特点 (文档类型、长度、质量)
  - 用户特点 (专业用户 vs 普通用户)
  - 性能要求 (每多一步 LLM 调用就多一份延迟和成本)
""")
