from src.rag.retriever import PolicyRetriever

retriever = PolicyRetriever()

results = retriever.search(
    collection_name="policies",
    query="Customer received a damaged product and wants a replacement.",
    k=3,
)

print("\nRetrieved Chunks:", len(results))

for i, doc in enumerate(results, start=1):

    print("\n")
    print("=" * 80)
    print(f"Chunk {i}")
    print("=" * 80)

    print(doc.page_content[:1000])