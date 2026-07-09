from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from src.config.settings import settings


class VectorStoreManager:
    """
    Singleton manager for all Chroma collections.
    """

    def __init__(self):

        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )

        self.collections = {}

    def load_collection(
        self,
        collection_name: str,
    ):

        if collection_name not in self.collections:

            self.collections[collection_name] = Chroma(
                collection_name=collection_name,
                embedding_function=self.embedding_model,
                persist_directory=settings.CHROMA_DB_PATH,
            )

        return self.collections[collection_name]

    def create_collection(
        self,
        collection_name: str,
    ):

        return self.load_collection(
            collection_name
        )

    def add_documents(
        self,
        collection_name: str,
        documents,
    ):

        collection = self.load_collection(
            collection_name
        )

        collection.add_documents(
            documents
        )

        return collection