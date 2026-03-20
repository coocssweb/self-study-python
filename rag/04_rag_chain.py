# ============================================================
# RAG 第四课 — 完整 RAG Chain
# ============================================================
# 运行: python rag/04_rag_chain.py
# ============================================================
# 前三课学了三个零件: Embedding、切片、向量数据库
# 这一课把它们组装起来，跑通完整的 RAG 流程:
#
#   用户提问 → 检索相关文档 → 拼入 prompt → LLM 生成回答
#
# 类比前端: 这就像把 API 层、数据层、UI 层串起来，
# 从"各个组件能跑"到"整个应用能跑"。
# ============================================================

import os
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 初始化 LLM
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-chat",
    temperature=0,  # RAG 场景用低温度，减少幻觉
)

# 初始化 Embedding 模型
embeddings = HuggingFaceEmbeddings(
    model_name="shibing624/text2vec-base-chinese",
)


# ============================================================
# 1. 准备知识库
# ============================================================

print("1. 准备知识库:")

# 模拟一份技术文档
knowledge_docs = [
    Document(
        page_content="""FastAPI 是一个现代的 Python Web 框架，基于 Starlette 和 Pydantic。
它的核心特点是：自动生成 API 文档（Swagger UI）、原生支持异步、类型注解驱动。
性能接近 Node.js 和 Go，是目前 Python 最快的 Web 框架之一。
安装方式: pip install fastapi uvicorn。
启动服务: uvicorn main:app --reload。""",
        metadata={"source": "fastapi_docs.md", "topic": "FastAPI基础"},
    ),
    Document(
        page_content="""FastAPI 的路由定义使用装饰器语法，和 Flask 类似但更强大。
GET 请求: @app.get("/items/{item_id}")
POST 请求: @app.post("/items/")
路径参数自动校验类型，查询参数用函数默认值定义。
请求体用 Pydantic BaseModel 定义，自动校验和序列化。
响应模型用 response_model 参数指定，自动过滤多余字段。""",
        metadata={"source": "fastapi_docs.md", "topic": "FastAPI路由"},
    ),
    Document(
        page_content="""FastAPI 的依赖注入系统非常强大，用 Depends() 实现。
常见用途: 数据库连接管理、用户认证、权限校验、共享逻辑。
示例: def get_db(): yield db_session，然后在路由函数参数里写 db: Session = Depends(get_db)。
依赖可以嵌套，FastAPI 会自动解析依赖树。
类比前端: 类似 React 的 Context + Provider，或者 Angular 的依赖注入。""",
        metadata={"source": "fastapi_docs.md", "topic": "FastAPI依赖注入"},
    ),
    Document(
        page_content="""FastAPI 原生支持异步编程，路由函数可以用 async def。
对于 I/O 密集型操作（数据库查询、HTTP 请求），异步能显著提升并发性能。
同步函数 FastAPI 会自动放到线程池执行，不会阻塞事件循环。
推荐: 有异步库就用 async def，没有就用普通 def，不要混用。
常用异步库: httpx(HTTP客户端)、asyncpg(PostgreSQL)、motor(MongoDB)。""",
        metadata={"source": "fastapi_docs.md", "topic": "FastAPI异步"},
    ),
    Document(
        page_content="""FastAPI 的中间件用于处理请求/响应的通用逻辑。
添加中间件: @app.middleware("http")。
常见中间件: CORS跨域、请求日志、响应时间统计、异常处理。
CORS 配置: from fastapi.middleware.cors import CORSMiddleware，然后 app.add_middleware(...)。
中间件执行顺序: 请求时从外到内，响应时从内到外（洋葱模型）。
类比前端: 和 Express/Koa 的中间件概念完全一样。""",
        metadata={"source": "fastapi_docs.md", "topic": "FastAPI中间件"},
    ),
    Document(
        page_content="""FastAPI 的错误处理使用 HTTPException。
抛出异常: raise HTTPException(status_code=404, detail="未找到")。
自定义异常处理器: @app.exception_handler(CustomError)。
校验错误会自动返回 422 状态码和详细的错误信息。
生产环境建议: 统一错误响应格式，区分业务错误和系统错误。""",
        metadata={"source": "fastapi_docs.md", "topic": "FastAPI错误处理"},
    ),
]

# 切片
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["。\n", "。", "\n", "，", " ", ""],
)

split_docs = splitter.split_documents(knowledge_docs)
print(f"   原始文档: {len(knowledge_docs)} 篇")
print(f"   切片后: {len(split_docs)} 个 chunk")

# 存入向量数据库
vector_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
)

# 创建 Retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
print("   ✓ 向量数据库和 Retriever 准备完成")


# ============================================================
# 2. 手动实现 RAG 流程 — 理解原理
# ============================================================

# print("\n2. 手动实现 RAG (理解原理):")

# question = "FastAPI怎么处理跨域问题？"

# # 第一步: 检索相关文档
# retrieved_docs = retriever.invoke(question)

# print(f"   问题: {question}")
# print(f"   检索到 {len(retrieved_docs)} 个相关片段:")
# for i, doc in enumerate(retrieved_docs):
#     print(f"     [{i + 1}] {doc.page_content[:50]}...")

# # 第二步: 把检索到的内容拼成上下文
# context = "\n\n".join(doc.page_content for doc in retrieved_docs)

# # 第三步: 构造 prompt
# prompt_text = f"""基于以下参考资料回答用户的问题。如果参考资料中没有相关信息，请说明你不确定。

# 参考资料:
# {context}

# 用户问题: {question}

# 回答:"""

# # 第四步: 调用 LLM
# response = llm.invoke(prompt_text)
# print(f"\n   回答: {response.content}")


# # ============================================================
# # 3. 用 LCEL 构建 RAG Chain — 优雅的方式
# # ============================================================

# print("\n" + "=" * 50)
# print("3. 用 LCEL 构建 RAG Chain:")

# 定义 prompt 模板
rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """你是一个技术文档助手。基于提供的参考资料回答问题。
规则:
- 只基于参考资料回答，不要编造信息
- 如果参考资料中没有相关内容，明确说"根据现有资料无法回答"
- 回答要简洁准确，适当引用原文"""),
    ("user", """参考资料:
{context}

问题: {question}"""),
])


def format_docs(docs: list[Document]) -> str:
    """把 Document 列表格式化成纯文本"""
    return "\n\n".join(
        f"[来源: {doc.metadata.get('topic', '未知')}]\n{doc.page_content}"
        for doc in docs
    )


# 构建 RAG Chain
# RunnablePassthrough 用于传递原始输入

print('+++++++++++++++++++++++++++++++++++++++++', retriever | format_docs)

rag_chain = (
    {
        "context": retriever | format_docs,  # 检索 → 格式化
        "question": RunnablePassthrough(),    # 原样传递问题
    }
    | rag_prompt    # 填充模板
    | llm           # 调用 LLM
    | StrOutputParser()  # 提取纯文本
)

# 使用 chain
question = "FastAPI的依赖注入怎么用？和前端框架有什么类似的？"
answer = rag_chain.invoke(question)


print(f"   问题: {question}")
print(f"   回答: {answer}")


# # ============================================================
# # 4. 多轮问答测试
# # ============================================================

# print("\n4. 多轮问答测试:")

# questions = [
#     "FastAPI怎么定义路由？",
#     "FastAPI支持异步吗？怎么用？",
#     "FastAPI怎么处理错误？",
#     "FastAPI和Django有什么区别？",  # 知识库里没有 Django 的信息
# ]

# for q in questions:
#     print(f"\n   Q: {q}")
#     answer = rag_chain.invoke(q)
#     print(f"   A: {answer}")
#     print(f"   {'─' * 40}")


# # ============================================================
# # 5. 带来源引用的 RAG Chain
# # ============================================================

# print("\n5. 带来源引用的 RAG Chain:")
# print("""
#    实际项目中，用户不仅想要答案，还想知道"你从哪看到的"。
#    我们可以把检索到的文档来源一起返回。
# """)

from langchain_core.runnables import RunnableLambda


def retrieve_with_sources(question: str) -> dict:
    """检索文档并返回格式化的上下文和来源"""
    docs = retriever.invoke(question)
    context = format_docs(docs)
    sources = list(set(
        doc.metadata.get("topic", "未知") for doc in docs
    ))
    return {
        "context": context,
        "question": question,
        "sources": sources,
    }


# 带来源的 chain
rag_with_sources_chain = (
    RunnableLambda(retrieve_with_sources)
    | RunnableLambda(lambda x: {
        "answer": (rag_prompt | llm | StrOutputParser()).invoke({
            "context": x["context"],
            "question": x["question"],
        }),
        "sources": x["sources"],
    })
)

result = rag_with_sources_chain.invoke("FastAPI的中间件是什么？")
print(f"   回答: {result['answer']}")
print(f"   参考来源: {', '.join(result['sources'])}")


# # ============================================================
# # 6. 流式输出的 RAG Chain
# # ============================================================

# print("\n6. 流式输出:")

# # 流式 chain（简化版，不带来源）
# stream_chain = (
#     {
#         "context": retriever | format_docs,
#         "question": RunnablePassthrough(),
#     }
#     | rag_prompt
#     | llm
#     | StrOutputParser()
# )

# print("   Q: FastAPI怎么启动服务？")
# print("   A: ", end="")
# for chunk in stream_chain.stream("FastAPI怎么启动服务？"):
#     print(chunk, end="", flush=True)
# print("\n")


# # ============================================================
# # 总结
# # ============================================================

# print("=" * 50)
# print("RAG Chain 要点:")
# print("=" * 50)
# print("""
# 1. RAG 完整流程:
#    用户提问 → Retriever 检索 → 格式化上下文 → 填充 Prompt → LLM 生成 → 输出

# 2. LCEL 构建 RAG Chain:
#    chain = (
#        {"context": retriever | format_docs, "question": RunnablePassthrough()}
#        | prompt | llm | parser
#    )

# 3. 关键设计决策:
#    - temperature=0: RAG 场景要准确，不要创意
#    - prompt 里明确说"只基于参考资料回答": 减少幻觉
#    - format_docs 带上来源信息: 方便追溯

# 4. RunnablePassthrough 的作用:
#    在 chain 的 dict 步骤里，原样传递某个输入值
#    类比前端: 就像 Redux 中间件里的 next(action)，不做处理直接传递

# 5. 实际项目中还需要考虑:
#    - 检索质量优化 (下一课讲)
#    - 对话历史管理 (结合 Memory)
#    - 错误处理和降级策略
#    - 成本控制 (减少不必要的 LLM 调用)
# """)
