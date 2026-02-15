from langchain_chroma import Chroma
import app_config as cfg
from langchain_community.embeddings import DashScopeEmbeddings
import os
import dotenv

dotenv.load_dotenv()

DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


class VectorStoreService(object):
    def __init__(self, embedding) -> None:
        self.embedding = embedding
        self.vectore_store = Chroma(
            collection_name=cfg.collection_name,
            embedding_function=self.embedding,
            persist_directory=cfg.persist_directory,
        )

    def get_retrirver(self):
        return self.vectore_store.as_retriever(
            search_kwargs={"k": cfg.similarity_threshold}
        )


if __name__ == "__main__":
    retriever = VectorStoreService(
        DashScopeEmbeddings(
            model="text-embedding-v4", dashscope_api_key=DASHSCOPE_API_KEY
        )
    ).get_retrirver()
    print(retriever.invoke("什么是三原色？"))
