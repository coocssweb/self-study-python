你可以先自己做 15~20 个问题：

# 人物类
- 云天明和程心是什么关系？
- 章北海最核心的决策是什么？
- 叶文洁为什么与三体文明接触？

# 组织/设定类
- 面壁计划是什么？
- 智子封锁指的是什么？
- 黑暗森林理论的核心观点是什么？

# 事件类
- 红岸基地在故事中起了什么作用？
- 威慑纪元是如何开始的？
- 水滴事件造成了什么影响？
- 这类题比“文学评论型问题”更适合评估第一版系统。

# Agent
- 帮我总结云天明 + 给出相关情节 + 判断他的性格变化


# 目录结构
```python
rag-project/
├── main.py
├── loader.py
├── splitter.py
├── embedding.py
├── vector_store.py
├── retriever.py
├── llm.py
└── utils.py
└── docs
```


# 虚拟代码
```python
query = input("请输入问题：")
docs = load_docs()
chunks = split(docs)
vectors = embed(chunks)
top_k = search(query, vectors)
prompt = build_prompt(query, top_k)
answer = call_llm(prompt)
print(answer)
```