MD5_FILE = "data/md5.txt"

# chroma
collection_name = "rag"
persist_directory = "./chroma_db"
top_k = 3

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", " ", "", ".", "!", "?", "。", "，", "？"]
max_split_char_number = 1000

# model
embedding_model = "text-embedding-v4"
chat_model = "qwen-turbo"

session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}
