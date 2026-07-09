from pydantic import BaseModel, Field


class ProposedAction(BaseModel):
    """
    Structured decision produced by the LLM.
    """

    action: str = Field(
        description="Replacement, Refund, Reject, Escalate, Partial Refund, etc."
    )

    resolution_summary: str = Field(
        description="Short internal summary of the proposed resolution."
    )

    refund_amount: float = Field(
        default=0.0
    )

    replacement: bool = Field(
        default=False
    )

    compensation: str = Field(
        default=""
    )

    needs_escalation: bool = Field(
        default=False
    )

    reasoning: str = Field(
        description="Reason why this action was chosen."
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )