MD5_FILE = "data/md5.txt"

# chroma
collection_name = "rag"
persist_directory = "./chroma_db"
similarity_threshold = 1

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", ".", "!", "?", "。", "，", "？"]
max_split_char_number = 1000
