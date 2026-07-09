from pydantic import BaseModel


class ComplaintRequest(BaseModel):
    order_id: str
    complaint_text: str


class ComplaintResponse(BaseModel):
    action: str
    customer_message: str
    resolution_summary: str
    refund_amount: float
    replacement: bool
    compensation: str
    confidence: float
    final_decision: str
    execution_trace: list[str]
    


# ==========================================================
# Agent Actions
# ==========================================================

class AgentActionRequest(BaseModel):
    complaint_id: int


class AgentActionResponse(BaseModel):
    complaint_id: int
    status: str
    message: str    
    