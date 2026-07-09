from src.rag.retriever import PolicyRetriever

retriever = PolicyRetriever()

results = retriever.search(
    collection_name="historical_cases",
    query="Customer received damaged product and requested replacement.",
    k=3,
)

print(f"\nRetrieved {len(results)} historical cases.\n")

for i, doc in enumerate(results, start=1):

    print("=" * 90)
    print(f"Historical Case {i}")
    print("=" * 90)

    print(doc.page_content)
    print()