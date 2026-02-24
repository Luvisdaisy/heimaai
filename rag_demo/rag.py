from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableWithMessageHistory,
    RunnableLambda,
)
from langchain_core.runnables.config import RunnableConfig
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_history
from pydantic import SecretStr
import rag_demo.app_config as cfg
import os
import dotenv

dotenv.load_dotenv()
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


def print_prompt(prompt):
    print("=======prompt=======")
    print(prompt)
    print("=======prompt end=======")
    return prompt


class RagService(object):
    def __init__(self) -> None:
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(
                model=cfg.embedding_model, dashscope_api_key=DASHSCOPE_API_KEY
            )
        ).get_retriever()

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你是人工智能助手，以简洁的方式解答问题，参考资料:{context}",
                ),
                ("system", "我提供过去的对话记录，如下所示:"),
                MessagesPlaceholder("history"),
                ("human", "请回答问题:{input}"),
            ]
        )

        self.chat_model = ChatTongyi(
            model=cfg.chat_model,
            api_key=DASHSCOPE_API_KEY,
        )

        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service

        def format_document(documents):
            if not documents:
                return "没有找到相关资料"
            for document in documents:
                document.page_content = (
                    f"来源:{document.metadata['source']}\n内容:{document.page_content}"
                )
            return "\n\n".join([doc.page_content for doc in documents])

        def format_for_retriever(value):
            return value["input"]

        def format_for_prompt(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value

        chain = (
            {
                "input": RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever)
                | retriever
                | format_document,
            }
            | RunnableLambda(format_for_prompt)
            | self.prompt_template
            | print_prompt
            | self.chat_model
            | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain


if __name__ == "__main__":
    session_config: RunnableConfig = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    rag_service = RagService()
    response = rag_service.chain.invoke(
        {"input": "我的身高170cm，求尺码推荐"}, config=session_config
    )
    print("=======response=======")
    print(response)
    print("=======response end=======")
