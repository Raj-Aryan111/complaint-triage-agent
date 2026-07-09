from sqlalchemy.orm import Session

from src.config.settings import settings
from src.classification.classifier import ComplaintClassifier
from src.generation.generator import ResponseGenerator
from src.db.crud import get_order_by_id
from src.db.database import SessionLocal
from src.rag.retriever import PolicyRetriever
from src.schemas.state import ComplaintState


# ==========================================================
# Shared Components
# ==========================================================

retriever = PolicyRetriever()


# ==========================================================
# Load Order Node
# ==========================================================

def load_order_node(state: ComplaintState) -> ComplaintState:

    db: Session = SessionLocal()

    try:

        order = get_order_by_id(
            db=db,
            order_id=state["order_id"],
        )

        if order is None:

            state["execution_trace"].append(
                f"Order {state['order_id']} not found."
            )

            state["final_decision"] = "escalate"
            state["escalation_reason"] = "Invalid Order ID"

            return state

        state["order_context"] = {
            column.name: getattr(order, column.name)
            for column in order.__table__.columns
        }

        state["execution_trace"].append(
            f"Loaded order {state['order_id']} from database."
        )

        return state

    finally:

        db.close()


# ==========================================================
# Classification Node
# ==========================================================

def classify_node(state: ComplaintState) -> ComplaintState:

    if settings.DEV_MODE:

        state["category"] = "Damaged Product"
        state["severity"] = "Medium"
        state["sentiment"] = "Frustrated"

        state["execution_trace"].append(
            "Development Mode: Mock classification used."
        )

        return state

    classifier = ComplaintClassifier()

    context = {
        "product_name": state["order_context"].get("product_name"),
        "product_category": state["order_context"].get("product_category"),
        "brand": state["order_context"].get("brand"),
        "delivery_status": state["order_context"].get("delivery_status"),
        "payment_status": state["order_context"].get("payment_status"),
        "customer_tier": state["order_context"].get("customer_tier"),
        "order_value": state["order_context"].get("order_value"),
    }

    result = classifier.classify(
        complaint_text=state["complaint_text"],
        order_context=context,
    )

    state["category"] = result.category
    state["severity"] = result.severity
    state["sentiment"] = result.sentiment

    state["execution_trace"].append(
        f"Complaint classified as "
        f"{result.category} | "
        f"{result.severity} | "
        f"{result.sentiment}"
    )

    return state


# ==========================================================
# Policy Retrieval Node
# ==========================================================

def retrieve_policy_node(state: ComplaintState) -> ComplaintState:

    query = (
        f"{state['category']}. "
        f"{state['complaint_text']}"
    )

    documents = retriever.search(
        collection_name="policies",
        query=query,
        k=settings.TOP_K_POLICY,
    )

    state["retrieved_policy"] = [
        document.page_content
        for document in documents
    ]

    state["execution_trace"].append(
        f"Retrieved {len(documents)} policy chunks."
    )

    return state


# ==========================================================
# Historical Retrieval Node
# ==========================================================

def retrieve_historical_node(state: ComplaintState) -> ComplaintState:

    query = (
        f"{state['category']}. "
        f"{state['complaint_text']}"
    )

    documents = retriever.search(
        collection_name="historical_cases",
        query=query,
        k=settings.TOP_K_PRECEDENTS,
    )

    state["retrieved_precedents"] = [
        document.page_content
        for document in documents
    ]

    state["execution_trace"].append(
        f"Retrieved {len(documents)} historical cases."
    )

    return state


# ==========================================================
# Draft Response Node
# ==========================================================

def draft_response_node(state: ComplaintState) -> ComplaintState:

    if settings.DEV_MODE:

        state["proposed_action"] = {
            "action": "Approve Replacement",
            "resolution_summary": "Replacement approved with ₹200 Coupon",
            "refund_amount": 0.0,
            "replacement": True,
            "compensation": "₹200 Coupon",
            "needs_escalation": False,
            "reasoning": "Development mode mock response.",
            "confidence": 0.95,
        }

        state["execution_trace"].append(
            "Development Mode: Mock draft generated."
        )

        return state

    generator = ResponseGenerator()

    result = generator.generate(
        complaint_text=state["complaint_text"],
        order_context=state["order_context"],
        policies=state["retrieved_policy"],
        precedents=state["retrieved_precedents"],
    )

    state["proposed_action"] = result.model_dump()

    state["execution_trace"].append(
        "Draft response generated."
    )

    return state


# ==========================================================
# Compliance Node
# ==========================================================

def compliance_node(state: ComplaintState) -> ComplaintState:

    action = state["proposed_action"]

    result = {
        "passed": True,
        "reason": "Passed all compliance checks.",
    }

    if action["confidence"] < settings.CONFIDENCE_THRESHOLD:

        result["passed"] = False
        result["reason"] = "Low confidence."

    if action["needs_escalation"]:

        result["passed"] = False
        result["reason"] = "LLM requested escalation."

    if action["refund_amount"] > 10000:

        result["passed"] = False
        result["reason"] = "Refund exceeds AI approval limit."

    state["compliance_result"] = result

    state["execution_trace"].append(
        f"Compliance: {result['reason']}"
    )

    return state


# ==========================================================
# Router Node
# ==========================================================

def router_node(state: ComplaintState) -> str:

    result = state["compliance_result"]

    if result["passed"]:
        return "send"

    if state["revision_count"] >= settings.MAX_REVISIONS:
        return "escalate"

    if result["reason"] == "Low confidence.":
        return "revise"

    return "escalate"


# ==========================================================
# Revision Node
# ==========================================================

def revise_node(state: ComplaintState) -> ComplaintState:

    state["revision_count"] += 1

    state["execution_trace"].append(
        "Revision Node Executed"
    )

    return state


# ==========================================================
# Escalation Node
# ==========================================================

def escalate_node(state: ComplaintState) -> ComplaintState:

    state["final_decision"] = "escalate"

    state["execution_trace"].append(
        "Escalation Node Executed"
    )

    return state


# ==========================================================
# Send Response Node
# ==========================================================

def send_response_node(state: ComplaintState) -> ComplaintState:

    state["final_decision"] = "send"

    state["execution_trace"].append(
        "Send Response Node Executed"
    )

    return state