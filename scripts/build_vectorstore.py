from pathlib import Path

from src.rag.loader import DocumentLoader
from src.rag.chunker import DocumentChunker
from src.rag.vectorstore import VectorStoreManager


loader = DocumentLoader()
chunker = DocumentChunker()
vectorstore = VectorStoreManager()


DOCUMENTS = {
    "policies": "NovaMart_Complaint_Resolution_Policy_Manual.pdf",
    "compliance": "NovaMart_Compliance_Rulebook.docx",
    "escalation": "NovaMart_Escalation_Handbook.docx",
}


DATA_PATH = Path("data/policies")


for collection_name, filename in DOCUMENTS.items():

    print("=" * 70)
    print(f"Building collection: {collection_name}")
    print("=" * 70)

    file_path = DATA_PATH / filename

    if file_path.suffix.lower() == ".pdf":
        documents = loader.load_pdf(str(file_path))
    else:
        documents = loader.load_docx(str(file_path))

    chunks = chunker.split_documents(documents)

    # Remove useless cover/admin chunks
    filtered_chunks = []

    for chunk in chunks:

        text = chunk.page_content.lower()

        if (
            "internal use only" in text
            and "version" in text
            and len(text) < 700
        ):
            continue

        filtered_chunks.append(chunk)

    print(f"Original Chunks : {len(chunks)}")
    print(f"Filtered Chunks : {len(filtered_chunks)}")

    vectorstore.add_documents(
        collection_name=collection_name,
        documents=filtered_chunks,
    )

    print(f"Collection '{collection_name}' created.\n")


print("=" * 70)
print("Vector Database Created Successfully!")
print("=" * 70)