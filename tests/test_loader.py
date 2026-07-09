from src.rag.loader import DocumentLoader

loader = DocumentLoader()

docs = loader.load_all_documents(
    "data/policies"
)

print(f"\nLoaded {len(docs)} documents/pages.\n")

print("=" * 80)

print(docs[0].page_content[:1000])

print("\n")

print(docs[0].metadata)