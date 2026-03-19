# RAG 学习 (检索增强生成)

RAG = Retrieval-Augmented Generation，核心思路：

1. 把文档切成小块
2. 用 Embedding 模型把文本变成向量
3. 存到向量数据库
4. 用户提问时，先检索相关片段
5. 把检索到的内容拼进 prompt，让 LLM 基于这些内容回答

类比前端：RAG 就像 Elasticsearch + React 的组合。
向量数据库负责"搜"，LLM 负责"答"，你负责把它们串起来。

## 为什么需要 RAG？

LLM 有两个硬伤：
- 知识截止日期：训练数据有时效性，不知道最新的事
- 不了解你的私有数据：公司文档、项目代码、个人笔记

RAG 就是让 LLM "开卷考试"，把相关资料塞给它，而不是指望它什么都记住。

## 环境准备

```bash
# 一行装完所有依赖
pip install langchain langchain-openai langchain-community chromadb langchain-huggingface sentence-transformers langchain-chroma langchain-text-splitters
```

注意：不需要安装 `unstructured`（它在 Windows 上容易构建失败）。
我们的课程只读 `.py` 和 `.md` 文件，用 Python 内置的文件读取就够了。
`unstructured` 是用来加载 PDF、Word 等复杂格式的，后续有需要再装。

## 关于 Embedding 模型的选择

本课程提供两种 Embedding 方案：

1. **本地模型 (推荐学习用)**：`sentence-transformers/all-MiniLM-L6-v2`
   - 免费，无需 API Key
   - 首次运行会自动下载模型 (~80MB)
   - 速度快，适合开发调试

2. **DeepSeek Embedding API**：如果本地模型下载困难
   - 需要消耗 API 额度（很便宜）
   - 无需下载模型文件

课程代码默认用本地模型，每个文件里都有注释说明如何切换。

## 文件列表

```
01_embedding.py      — Embedding 向量化基础：文本如何变成向量
02_text_split.py     — 文档切片策略：怎么把长文档切成合适的小块
03_vector_store.py   — 向量数据库：存储、检索、相似度搜索
04_rag_chain.py      — 完整 RAG Chain：检索 + 生成，跑通核心流程
05_advanced_rag.py   — 进阶技巧：多查询、重排序、上下文压缩
06_rag_project.py    — 实战项目：对着本仓库的代码文档做问答
```

## 前置知识

建议先学完 `langchain/` 目录下的内容，特别是：
- `03_chain.py` — Chain 的管道语法
- `04_output.py` — OutputParser 结构化输出

## 运行

```bash
python rag/01_embedding.py
```
