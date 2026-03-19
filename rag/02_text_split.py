# ============================================================
# RAG 第二课 — 文档切片策略
# ============================================================
# 运行: python rag/02_text_split.py
# ============================================================
# 核心问题: 文档太长，塞不进 LLM 的上下文窗口怎么办？
#
# LLM 有 token 上限（DeepSeek 是 64K），一本书几十万字根本塞不下。
# 就算塞得下，信息太多 LLM 也会"走神"（Lost in the Middle 问题）。
#
# 解决方案: 把长文档切成小块（chunk），只检索最相关的几块塞进去。
#
# 类比前端: 就像虚拟列表（Virtual List），
# 数据有 10 万条，但你只渲染可视区域的几十条。
# RAG 也一样，文档有几万段，但只取最相关的几段给 LLM。
# ============================================================


# ============================================================
# 1. 为什么不能直接按固定长度切？
# ============================================================

print("1. 为什么切片策略很重要？")
print("""
   假设有这段文本:
   "Python的装饰器是一种语法糖。它可以在不修改原函数代码的情况下，
    给函数添加额外功能。常见的用法包括日志记录、权限验证、缓存等。"

   如果按固定 20 字切:
     chunk1: "Python的装饰器是一种语法糖。它可以在不"  ← 句子被截断了!
     chunk2: "修改原函数代码的情况下，给函数添加额外功"  ← 上下文丢失!
     chunk3: "能。常见的用法包括日志记录、权限验证、缓存等。"

   问题: 搜索"装饰器有什么用"时，chunk1 匹配到了，但它不包含答案。
   答案在 chunk3 里，但 chunk3 没提到"装饰器"，搜不到。

   所以切片策略直接影响 RAG 的检索质量。
""")


# ============================================================
# 2. CharacterTextSplitter — 最基础的切片器
# ============================================================

print("2. CharacterTextSplitter (按字符切):")

from langchain_text_splitters import CharacterTextSplitter

text = """Python是一种广泛使用的高级编程语言。它由Guido van Rossum于1991年创建。Python强调代码的可读性，语法简洁优雅。

Python支持多种编程范式，包括面向对象、函数式和过程式编程。它拥有丰富的标准库和活跃的社区。

Python在数据科学、人工智能、Web开发等领域都有广泛应用。特别是在AI领域，PyTorch和TensorFlow等框架都基于Python。"""

# separator: 按什么字符切（默认换行符）
# chunk_size: 每块最大字符数
# chunk_overlap: 相邻块之间的重叠字符数
splitter = CharacterTextSplitter(
    separator="\n\n",    # 按段落分割
    chunk_size=100,      # 每块最多 100 字符
    chunk_overlap=20,    # 相邻块重叠 20 字符
)

chunks = splitter.split_text(text)

for i, chunk in enumerate(chunks):
    print(f"   chunk {i} ({len(chunk)}字符): {chunk[:60]}...")
    print()


# ============================================================
# 3. RecursiveCharacterTextSplitter — 最常用的切片器 (推荐)
# ============================================================

print("\n3. RecursiveCharacterTextSplitter (递归切片，推荐):")
print("""
   "递归"的意思: 它会按优先级依次尝试多种分隔符:
   ["\n\n", "\n", " ", ""]
   先尝试按段落切 → 段落太长就按行切 → 行太长就按空格切 → 最后按字符切

   这样能最大程度保持语义完整性。
   类比: 就像 CSS 的 word-break，优先在合适的位置断行。
""")

from langchain_text_splitters import RecursiveCharacterTextSplitter

# 准备一段更长的文本
long_text = """# Python 装饰器详解

## 什么是装饰器

装饰器是Python中一种强大的语法特性。它本质上是一个函数，接收一个函数作为参数，返回一个新函数。装饰器可以在不修改原函数代码的情况下，给函数添加额外的功能。

## 基本语法

使用@符号来应用装饰器。当你写@decorator时，Python会自动把下面的函数传给decorator函数处理。这是一种语法糖，让代码更简洁。

## 常见用途

装饰器在实际开发中有很多用途：
1. 日志记录：自动记录函数的调用时间、参数和返回值
2. 权限验证：在函数执行前检查用户是否有权限
3. 缓存：缓存函数的返回值，避免重复计算
4. 计时：统计函数的执行时间
5. 重试：在函数失败时自动重试

## 带参数的装饰器

有时候装饰器本身也需要参数。这时需要再嵌套一层函数。虽然看起来复杂，但理解了闭包的概念就很清晰了。

## 类装饰器

除了函数装饰器，Python还支持类装饰器。类装饰器通过实现__call__方法来实现。它的优势是可以维护状态。"""

recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,       # 每块最多 150 字符
    chunk_overlap=30,     # 重叠 30 字符
    separators=["\n\n", "\n", "。", "，", " ", ""],  # 中文友好的分隔符
)

chunks = recursive_splitter.split_text(long_text)

print(f"   原文长度: {len(long_text)} 字符")
print(f"   切成 {len(chunks)} 块:\n")

for i, chunk in enumerate(chunks):
    print(f"   --- chunk {i} ({len(chunk)}字符) ---")
    print(f"   {chunk}")
    print()


# ============================================================
# 4. chunk_overlap 重叠的作用
# ============================================================

print("4. chunk_overlap 重叠的作用:")
print("""
   假设原文: "装饰器可以添加日志功能。日志功能对调试很有帮助。"

   不重叠 (overlap=0):
     chunk1: "装饰器可以添加日志功能。"
     chunk2: "日志功能对调试很有帮助。"
     → 搜索"装饰器的日志功能对调试有帮助吗"时，两个 chunk 各匹配一半

   有重叠 (overlap=10):
     chunk1: "装饰器可以添加日志功能。日志功能"
     chunk2: "日志功能。日志功能对调试很有帮助。"
     → chunk2 包含了完整的上下文，检索效果更好

   重叠就像前端的 Intersection Observer 里的 rootMargin，
   给每个 chunk 留一点"缓冲区"，避免信息在边界处丢失。

   经验值:
   - chunk_size: 500~1000 字符 (中文) 或 200~500 tokens
   - chunk_overlap: chunk_size 的 10%~20%
""")

# 对比有无重叠的效果
sample = "AAAA。BBBB。CCCC。DDDD。EEEE。FFFF。GGGG。HHHH。"

no_overlap = RecursiveCharacterTextSplitter(
    chunk_size=20, chunk_overlap=0, separators=["。", ""]
).split_text(sample)

with_overlap = RecursiveCharacterTextSplitter(
    chunk_size=20, chunk_overlap=8, separators=["。", ""]
).split_text(sample)

print("   无重叠:")
for i, c in enumerate(no_overlap):
    print(f"     chunk {i}: {c}")

print("   有重叠 (overlap=8):")
for i, c in enumerate(with_overlap):
    print(f"     chunk {i}: {c}")


# ============================================================
# 5. 用 Document 对象切片 — 保留元数据
# ============================================================

print("\n5. Document 对象 — 带元数据的切片:")
print("""
   实际项目中，你不只是切文本，还要知道每块来自哪个文件、哪一页。
   LangChain 用 Document 对象来封装: 内容 + 元数据。
   类比前端: 就像 React 组件的 props，Document = { content, metadata }。
""")

from langchain_core.documents import Document

# 模拟从文件加载的文档
documents = [
    Document(
        page_content="LangChain是一个用于构建LLM应用的框架。它提供了Chain、Agent、Memory等核心抽象。",
        metadata={"source": "langchain_guide.md", "chapter": 1},
    ),
    Document(
        page_content="RAG通过检索外部知识来增强LLM的回答能力。核心流程是：文档切片、向量化、存储、检索、生成。",
        metadata={"source": "rag_tutorial.md", "chapter": 3},
    ),
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=50,
    chunk_overlap=10,
    separators=["。", "，", " ", ""],
)

# split_documents 会保留并继承原文档的 metadata
split_docs = splitter.split_documents(documents)

for doc in split_docs:
    print(f"   来源: {doc.metadata['source']} | 章节: {doc.metadata['chapter']}")
    print(f"   内容: {doc.page_content}")
    print()


# ============================================================
# 6. 针对代码的切片 — Language 分割器
# ============================================================

print("6. 代码切片 (按语言语法切):")

from langchain_text_splitters import Language

# RecursiveCharacterTextSplitter 内置了对各种编程语言的支持
python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=200,
    chunk_overlap=30,
)

python_code = '''
def hello(name: str) -> str:
    """打招呼函数"""
    return f"你好, {name}!"

class Calculator:
    """简单计算器"""

    def __init__(self):
        self.history = []

    def add(self, a: float, b: float) -> float:
        """加法"""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: float, b: float) -> float:
        """减法"""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
'''

code_chunks = python_splitter.split_text(python_code)

print(f"   代码切成 {len(code_chunks)} 块:")
for i, chunk in enumerate(code_chunks):
    print(f"\n   --- chunk {i} ---")
    print(f"   {chunk}")

print("""
   支持的语言: Python, JavaScript, TypeScript, Go, Java, C++, Markdown 等
   它会按函数/类的边界来切，而不是粗暴地按字符数切。
""")


# ============================================================
# 7. 切片策略选择指南
# ============================================================

print("\n" + "=" * 50)
print("切片策略选择指南:")
print("=" * 50)
print("""
1. 通用文本 → RecursiveCharacterTextSplitter (首选)
   - chunk_size: 500~1000
   - chunk_overlap: 50~100
   - 中文记得加中文分隔符: ["。", "，", "\\n"]

2. 代码 → RecursiveCharacterTextSplitter.from_language()
   - 按函数/类边界切割
   - chunk_size 可以大一些: 1000~2000

3. Markdown → MarkdownHeaderTextSplitter
   - 按标题层级切割
   - 自动把标题作为 metadata

4. chunk_size 怎么定？
   - 太小: 上下文不完整，检索到了也没用
   - 太大: 噪音太多，LLM 容易"走神"
   - 经验: 一个 chunk 应该包含一个完整的知识点

5. 实际项目中的建议:
   - 先用默认参数跑通
   - 然后根据检索效果调参
   - 没有万能参数，要根据你的数据特点来调
""")
