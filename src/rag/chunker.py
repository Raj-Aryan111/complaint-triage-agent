from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentChunker:
    """
    Splits documents into overlapping chunks for RAG.
    """

    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def split_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:

        chunks = self.splitter.split_documents(
            documents
        )

        return chunks