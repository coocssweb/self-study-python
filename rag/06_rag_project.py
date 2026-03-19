# ============================================================
# RAG 第六课 — 实战项目: 项目文档问答机器人
# ============================================================
# 运行: python rag/06_rag_project.py
# ============================================================
# 把前五课学的东西串起来，做一个真实可用的项目:
# 对着本仓库的代码和文档做问答。
#
# 功能:
# 1. 自动加载本仓库的 .py 和 .md 文件
# 2. 切片 + 向量化 + 存入 ChromaDB
# 3. 支持多轮对话问答
# 4. 带来源引用
# 5. 支持对话历史
#
# 这就是一个最小可用的 RAG 应用，
# 企业知识库问答、文档助手的核心逻辑都是这个。
# ============================================================

import os
import glob
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


# ============================================================
# 1. 文档加载器 — 读取本仓库的文件
# ============================================================

def load_repo_documents(repo_root: str) -> list[Document]:
    """
    加载仓库中的 .py 和 .md 文件，转成 Document 对象。
    跳过 .git、__pycache__、chroma_data 等目录。
    """
    documents = []
    skip_dirs = {".git", "__pycache__", "node_modules", "chroma_data", ".kiro"}

    # 加载 Python 文件
    for filepath in glob.glob(os.path.join(repo_root, "**", "*.py"), recursive=True):
        # 跳过不需要的目录
        if any(skip_dir in filepath for skip_dir in skip_dirs):
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                continue

            # 用相对路径作为来源标识
            rel_path = os.path.relpath(filepath, repo_root)
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": rel_path,
                    "file_type": "python",
                    "directory": os.path.dirname(rel_path),
                },
            ))
        except (UnicodeDecodeError, IOError):
            continue

    # 加载 Markdown 文件
    for filepath in glob.glob(os.path.join(repo_root, "**", "*.md"), recursive=True):
        if any(skip_dir in filepath for skip_dir in skip_dirs):
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.strip():
                continue

            rel_path = os.path.relpath(filepath, repo_root)
            documents.append(Document(
                page_content=content,
                metadata={
                    "source": rel_path,
                    "file_type": "markdown",
                    "directory": os.path.dirname(rel_path),
                },
            ))
        except (UnicodeDecodeError, IOError):
            continue

    return documents


# ============================================================
# 2. 智能切片 — 根据文件类型选择切片策略
# ============================================================

def split_documents(documents: list[Document]) -> list[Document]:
    """
    根据文件类型选择不同的切片策略:
    - Python 文件: 按代码结构切片
    - Markdown 文件: 按段落切片
    """
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=1000,
        chunk_overlap=100,
    )

    markdown_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["## ", "# ", "\n\n", "\n", "。", " ", ""],
    )

    all_chunks = []

    for doc in documents:
        if doc.metadata.get("file_type") == "python":
            chunks = python_splitter.split_documents([doc])
        else:
            chunks = markdown_splitter.split_documents([doc])
        all_chunks.extend(chunks)

    return all_chunks


# ============================================================
# 3. 构建 RAG 问答系统
# ============================================================

class RepoQA:
    """仓库文档问答系统"""

    def __init__(self, repo_root: str):
        self.repo_root = repo_root
        self.chat_history: list = []

        # 初始化 LLM
        self.llm = ChatOpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com",
            model="deepseek-chat",
            temperature=0,
        )

        # 初始化 Embedding
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
        )

        # 加载和处理文档
        self._build_index()

        # 初始化 prompt
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个代码仓库的文档助手。基于提供的代码和文档片段回答问题。

规则:
- 只基于提供的参考资料回答
- 如果资料不足以回答，明确说明
- 引用具体的文件路径帮助用户定位
- 代码相关的回答要准确，可以引用原始代码片段
- 用中文回答"""),
            ("user", """参考资料:
{context}

对话历史:
{history}

当前问题: {question}"""),
        ])

        # 查询改写 prompt（处理追问）
        self.rewrite_prompt = ChatPromptTemplate.from_messages([
            ("system", """根据对话历史，把用户的追问改写成一个独立的完整问题。
如果问题已经是独立的，直接返回原问题。只输出改写后的问题。"""),
            ("user", """对话历史:
{history}

当前问题: {question}

独立问题:"""),
        ])

    def _build_index(self):
        """加载文档、切片、构建向量索引"""
        print("   正在加载仓库文档...")
        documents = load_repo_documents(self.repo_root)
        print(f"   加载了 {len(documents)} 个文件")

        print("   正在切片...")
        chunks = split_documents(documents)
        print(f"   切成 {len(chunks)} 个片段")

        print("   正在构建向量索引...")
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
        )
        self.retriever = self.vector_store.as_retriever(
            search_type="mmr",  # 用 MMR 保证结果多样性
            search_kwargs={"k": 5, "fetch_k": 10},
        )
        print("   ✓ 索引构建完成\n")

    def _format_history(self) -> str:
        """格式化对话历史"""
        if not self.chat_history:
            return "(无历史对话)"

        # 只保留最近 3 轮
        recent = self.chat_history[-6:]
        lines = []
        for msg in recent:
            role = "用户" if isinstance(msg, HumanMessage) else "助手"
            # 截断过长的回答
            content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

    def _rewrite_query(self, question: str) -> str:
        """结合对话历史改写查询"""
        if not self.chat_history:
            return question

        history = self._format_history()
        rewritten = (
            self.rewrite_prompt | self.llm | StrOutputParser()
        ).invoke({
            "history": history,
            "question": question,
        })
        return rewritten.strip()

    def ask(self, question: str) -> str:
        """提问并获取回答"""
        # 改写查询（处理追问）
        search_query = self._rewrite_query(question)
        if search_query != question:
            print(f"   (查询改写: {search_query})")

        # 检索相关文档
        docs = self.retriever.invoke(search_query)

        # 格式化上下文，带文件来源
        context_parts = []
        sources = set()
        for doc in docs:
            source = doc.metadata.get("source", "未知")
            sources.add(source)
            context_parts.append(f"--- 文件: {source} ---\n{doc.page_content}")

        context = "\n\n".join(context_parts)
        history = self._format_history()

        # 生成回答
        answer = (
            self.qa_prompt | self.llm | StrOutputParser()
        ).invoke({
            "context": context,
            "history": history,
            "question": question,
        })

        # 追加来源信息
        source_info = "📎 参考文件: " + ", ".join(sorted(sources))
        full_answer = f"{answer}\n\n{source_info}"

        # 更新对话历史
        self.chat_history.append(HumanMessage(content=question))
        self.chat_history.append(AIMessage(content=answer))

        return full_answer

    def clear_history(self):
        """清空对话历史"""
        self.chat_history.clear()
        print("   ✓ 对话历史已清空")


# ============================================================
# 4. 运行问答系统
# ============================================================

def main():
    # 获取仓库根目录（当前脚本的上级目录）
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("=" * 50)
    print("  项目文档问答机器人")
    print("=" * 50)

    qa = RepoQA(repo_root)

    # 预设的演示问题
    demo_questions = [
        "这个项目包含哪些学习模块？",
        "LangChain 的 Chain 是怎么用的？给我看个例子",
        "tasks 目录下有哪些练习题？",
        "OutputParser 有几种？分别怎么用？",
        "项目里用的是什么 LLM？怎么配置的？",
    ]

    print("预设演示问题:")
    for i, q in enumerate(demo_questions, 1):
        print(f"  {i}. {q}")

    print("\n开始问答 (输入 quit 退出, clear 清空历史):\n")

    # 先跑一轮演示
    for q in demo_questions[:2]:
        print(f"Q: {q}")
        answer = qa.ask(q)
        print(f"A: {answer}\n")
        print("-" * 50)

    # 交互模式
    while True:
        try:
            user_input = input("\nQ: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("再见!")
            break
        if user_input.lower() == "clear":
            qa.clear_history()
            continue

        answer = qa.ask(user_input)
        print(f"A: {answer}")


if __name__ == "__main__":
    main()
