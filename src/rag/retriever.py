from langchain_core.documents import Document
from src.rag.vectorstore import VectorStoreManager

manager = VectorStoreManager()


class PolicyRetriever:
    """
    Loads Chroma collections once and reuses them.
    """

    def __init__(self):

        self.collections = {
            "policies": manager.load_collection("policies"),
            "historical_cases": manager.load_collection("historical_cases"),
            "compliance": manager.load_collection("compliance"),
            "escalation": manager.load_collection("escalation"),
        }

    def search(
        self,
        collection_name: str,
        query: str,
        k: int = 3,
    ) -> list[Document]:

        return self.collections[
            collection_name
        ].similarity_search(
            query=query,
            k=k,
        )