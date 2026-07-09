from pydantic import BaseModel


class ClassificationResult(BaseModel):
    category: str
    severity: str
    sentiment: str