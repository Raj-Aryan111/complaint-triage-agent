from pydantic import BaseModel
from typing import List


class CustomerInfo(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: str
    tier: str


class OrderInfo(BaseModel):
    order_id: str
    product: str
    brand: str
    category: str
    order_value: float
    delivery_status: str
    payment_status: str


class ClassificationInfo(BaseModel):
    category: str
    severity: str
    sentiment: str


class RecommendationInfo(BaseModel):
    action: str
    resolution_summary: str
    refund_amount: float
    replacement: bool
    compensation: str
    confidence: float
    reasoning: str


class ComplianceInfo(BaseModel):
    passed: bool
    reason: str


class AgentComplaintResponse(BaseModel):

    complaint_id: int

    customer: CustomerInfo

    order: OrderInfo

    complaint: str

    classification: ClassificationInfo

    recommendation: RecommendationInfo

    compliance: ComplianceInfo

    policy_summary: List[str]

    historical_summary: List[str]

    execution_trace: List[str]