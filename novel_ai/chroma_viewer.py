import chromadb

client = chromadb.PersistentClient(path="./chroma_data")

# 先看看有哪些 collection
print(client.list_collections())

# 然后指定 collection 名称来查
collection = client.get_collection("langchain")
print(collection.count())
print(collection.get())