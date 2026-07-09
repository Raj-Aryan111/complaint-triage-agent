import json

from src.classification.schema import ClassificationResult
from src.llm import get_llm


class ComplaintClassifier:
    """
    Handles complaint classification using an LLM.

    Returns a validated ClassificationResult object.
    """

    def __init__(self):

        self.llm = get_llm()

    def classify(
        self,
        complaint_text: str,
        order_context: dict,
    ) -> ClassificationResult:

        prompt = f"""
You are an expert customer support complaint classifier.

Classify the following e-commerce customer complaint.

Return ONLY valid JSON.

-----------------------------------------
Allowed Categories
-----------------------------------------
- Late Delivery
- Damaged Product
- Wrong Product
- Missing Product
- Billing Dispute
- Refund Request
- Payment Failure
- Warranty Claim
- Other

-----------------------------------------
Allowed Severity
-----------------------------------------
- Low
- Medium
- High

-----------------------------------------
Allowed Sentiment
-----------------------------------------
- Neutral
- Frustrated
- Angry

-----------------------------------------
Complaint
-----------------------------------------

{complaint_text}

-----------------------------------------
Order Context
-----------------------------------------

{json.dumps(order_context, indent=2)}

-----------------------------------------
Return ONLY this JSON
-----------------------------------------

{{
    "category": "...",
    "severity": "...",
    "sentiment": "..."
}}

Do not return markdown.

Do not explain.

Return JSON only.
"""

        last_exception = None

        for attempt in range(2):

            try:

                response = self.llm.generate(
                    prompt=prompt,
                    system_prompt=(
                        "You are an expert complaint "
                        "classification assistant."
                    ),
                    json_output=True,
                )

                result = ClassificationResult.model_validate_json(
                    response
                )

                return result

            except Exception as e:

                last_exception = e

                print(
                    f"Classification attempt {attempt + 1} failed."
                )
                print(e)
        raise RuntimeError(
            "Classification failed after 2 attempts."
        ) from last_exception