from src.rag.loader import DocumentLoader
from src.rag.chunker import DocumentChunker

loader = DocumentLoader()

documents = loader.load_all_documents(
    "data/policies"
)

chunker = DocumentChunker()

chunks = chunker.split_documents(documents)

print(f"\nOriginal Documents : {len(documents)}")

print(f"Generated Chunks   : {len(chunks)}")

print("\n")

print("=" * 100)

print(chunks[0].page_content)

print("\n")

print("=" * 100)

print(chunks[0].metadata)
for i in [0, 5, 20, 50, 100, 200]:

    print("\n")
    print("=" * 100)
    print(f"Chunk {i}")
    print("=" * 100)
    print(chunks[i].page_content[:700])