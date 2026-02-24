from datetime import datetime
import os
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import dotenv

import rag_demo.app_config as cfg

dotenv.load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def check_md5(md5: str):
    try:
        with open(cfg.MD5_FILE, "r") as f:
            md5_strs = f.readlines()
            for md5_str in md5_strs:
                if md5_str.strip() == md5:
                    return True
        return False
    except Exception as e:
        print(f"Error checking md5: {e}")
        return False


def get_md5(text: str, encoding="utf-8"):
    text_bytes = text.encode(encoding=encoding)

    md5_obj = hashlib.md5()
    md5_obj.update(text_bytes)
    return md5_obj.hexdigest()


def save_md5(md5: str):
    try:
        md5_dir = os.path.dirname(cfg.MD5_FILE)
        if not os.path.exists(md5_dir):
            os.makedirs(md5_dir)
        with open(cfg.MD5_FILE, "a") as f:
            f.write(md5 + "\n")
    except Exception as e:
        print(f"Error saving md5: {e}")


class KnowledgeBaseService(object):
    def __init__(self) -> None:
        os.makedirs(cfg.persist_directory, exist_ok=True)
        self.chroma = Chroma(
            collection_name=cfg.collection_name,
            persist_directory=cfg.persist_directory,
            embedding_function=DashScopeEmbeddings(
                model="text-embedding-v4", dashscope_api_key=DASHSCOPE_API_KEY
            ),
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=cfg.chunk_size,
            chunk_overlap=cfg.chunk_overlap,
            separators=cfg.separators,
            length_function=len,
        )

    def upload_by_str(self, data: str, filename):
        md5_hex = get_md5(data)

        if check_md5(md5_hex):
            return "Already processed"

        if len(data) > cfg.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]
        metadata = {
            "source": filename,
            "creat_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "Tian",
        }
        self.chroma.add_texts(
            knowledge_chunks, metadatas=[metadata for _ in knowledge_chunks]
        )

        save_md5(md5_hex)

        return "Loaded in chroma"


if __name__ == "__main__":
    service = KnowledgeBaseService()
    r = service.upload_by_str("Good old time", "test")
    print(r)
