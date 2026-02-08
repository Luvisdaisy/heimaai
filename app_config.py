MD5_FILE = "data/md5.txt"

# chroma
collection_name = "rag"
persist_directory = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", ".", "!", "?", "。", "，", "？"]
