from typing import Any, Dict, List, Optional, TypedDict


class ComplaintState(TypedDict):
    """
    Shared state that flows through every LangGraph node.
    Every node reads from this state and updates it.
    """

    # =====================================================
    # User Input
    # =====================================================

    order_id: str
    complaint_text: str

    # =====================================================
    # Database Context
    # =====================================================

    order_context: Dict[str, Any]

    # =====================================================
    # Classification Output
    # =====================================================

    category: Optional[str]
    severity: Optional[str]
    sentiment: Optional[str]

    # =====================================================
    # RAG Output
    # =====================================================

    retrieved_policy: List[str]
    retrieved_precedents: List[str]

    # =====================================================
    # Response Generation
    # =====================================================

    draft_response: Optional[str]

    proposed_action: Dict[str, Any]

    # Example:
    #
    # {
    #     "action": "refund",
    #     "refund_amount": 500,
    #     "replacement": False
    # }

    # =====================================================
    # Compliance
    # =====================================================

    compliance_result: Dict[str, Any]

    # Example:
    #
    # {
    #     "passed": True,
    #     "violations": [],
    #     "confidence": 0.94
    # }

    # =====================================================
    # Workflow
    # =====================================================

    revision_count: int

    final_decision: Optional[str]

    escalation_reason: Optional[str]

    # =====================================================
    # Execution Trace
    # =====================================================

    execution_trace: List[str]