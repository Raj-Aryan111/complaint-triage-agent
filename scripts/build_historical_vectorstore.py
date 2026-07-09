import pandas as pd

from langchain_core.documents import Document

from src.rag.vectorstore import VectorStoreManager


CSV_PATH = "data/precedents/historical_resolution_dataset.csv"

df = pd.read_csv(CSV_PATH)

documents = []

for _, row in df.iterrows():

    text = f"""
Complaint:
{row['complaint_text']}

Category:
{row['category']}

Resolution:
{row['resolution_summary']}

Action Taken:
{row['action_taken']}

Policy Applied:
{row['policy_sections_applied']}
"""

    documents.append(
        Document(
            page_content=text
        )
    )


manager = VectorStoreManager()

manager.add_documents(
    collection_name="historical_cases",
    documents=documents,
)

print("=" * 60)
print(f"Indexed {len(documents)} historical cases.")
print("=" * 60)