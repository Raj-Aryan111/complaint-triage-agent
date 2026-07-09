from src.rag.vectorstore import VectorStoreManager

manager = VectorStoreManager()

collection = manager.create_collection(
    "policies"
)

print(collection)