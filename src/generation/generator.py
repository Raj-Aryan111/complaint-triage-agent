import json

from src.llm import get_llm
from src.schemas.proposed_action import ProposedAction


class ResponseGenerator:
    """
    Generates a structured resolution using company policy
    and historical precedents.
    """

    def __init__(self):

        self.llm = get_llm()

    def generate(
        self,
        complaint_text: str,
        order_context: dict,
        policies: list[str],
        precedents: list[str],
    ) -> ProposedAction:

        system_prompt = """
You are NovaMart's AI Complaint Resolution Agent.

Your job is to determine the correct resolution according to company policy.

You MUST use the supplied policies and historical resolutions.

Return ONLY valid JSON.

Required JSON format:

{
    "action": "",
    "resolution_summary": "",
    "refund_amount": 0,
    "replacement": false,
    "compensation": "",
    "needs_escalation": false,
    "reasoning": "",
    "confidence": 0.95
}
"""

        user_prompt = f"""
Complaint

{complaint_text}

Order Details

{json.dumps(order_context, indent=2)}

Relevant Policies

{chr(10).join(policies)}

Historical Cases

{chr(10).join(precedents)}
"""

        response = self.llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            json_output=True,
        )

        data = json.loads(response)

        return ProposedAction(**data)