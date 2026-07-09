from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
)
from langchain_core.documents import Document


class DocumentLoader:
    """
    Loads policy documents from PDF and DOCX files.
    """

    def load_pdf(self, file_path: str) -> list[Document]:
        loader = PyPDFLoader(file_path)
        return loader.load()

    def load_docx(self, file_path: str) -> list[Document]:
        loader = Docx2txtLoader(file_path)
        return loader.load()

    def load_all_documents(self, data_dir: str) -> list[Document]:
        """
        Loads every PDF and DOCX inside a directory.
        """

        documents = []

        data_path = Path(data_dir)

        for file in data_path.iterdir():

            if file.suffix.lower() == ".pdf":
                documents.extend(
                    self.load_pdf(str(file))
                )

            elif file.suffix.lower() == ".docx":
                documents.extend(
                    self.load_docx(str(file))
                )

        return documents