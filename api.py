from fastapi import (
    Depends,
    FastAPI,
)

from sqlalchemy.orm import Session

from src.graph.workflow import graph

from src.db.database import get_db

from src.db.crud import (
    create_complaint,
    approve_complaint,
    escalate_complaint,
)

from src.schemas.api import (
    ComplaintRequest,
    ComplaintResponse,
    AgentActionRequest,
    AgentActionResponse,
)

from src.schemas.agent_api import (
    AgentComplaintResponse,
    CustomerInfo,
    OrderInfo,
    ClassificationInfo,
    RecommendationInfo,
    ComplianceInfo,
)

# ==========================================================
# FastAPI App
# ==========================================================

app = FastAPI(
    title="NovaMart Complaint Triage Agent",
    version="2.0.0",
    description="AI-powered Customer Complaint Resolution using LangGraph",
)

# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def home():

    return {
        "message": "NovaMart Complaint Triage Agent API is running."
    }


# ==========================================================
# Shared LangGraph Runner
# ==========================================================

def run_graph(request: ComplaintRequest):

    initial_state = {

        # --------------------------------------------------
        # User Input
        # --------------------------------------------------

        "order_id": request.order_id,
        "complaint_text": request.complaint_text,

        # --------------------------------------------------
        # Database Context
        # --------------------------------------------------

        "order_context": {},

        # --------------------------------------------------
        # Classification
        # --------------------------------------------------

        "category": None,
        "severity": None,
        "sentiment": None,

        # --------------------------------------------------
        # RAG
        # --------------------------------------------------

        "retrieved_policy": [],
        "retrieved_precedents": [],

        # --------------------------------------------------
        # Generation
        # --------------------------------------------------

        "draft_response": None,
        "proposed_action": {},

        # --------------------------------------------------
        # Compliance
        # --------------------------------------------------

        "compliance_result": {},

        # --------------------------------------------------
        # Workflow
        # --------------------------------------------------

        "revision_count": 0,
        "final_decision": None,
        "escalation_reason": None,

        # --------------------------------------------------
        # Execution Trace
        # --------------------------------------------------

        "execution_trace": [],
    }

    return graph.invoke(initial_state)


# ==========================================================
# Customer Endpoint
# ==========================================================

@app.post(
    "/complaint",
    response_model=ComplaintResponse,
)
def process_customer_complaint(
    request: ComplaintRequest,
):

    result = run_graph(request)

    action = result["proposed_action"]

    customer_message = (
        "We're sorry for the inconvenience.\n\n"
        f"{action['resolution_summary']}.\n\n"
        "Thank you for shopping with NovaMart."
    )

    return ComplaintResponse(

        action=action["action"],

        customer_message=customer_message,

        resolution_summary=action["resolution_summary"],

        refund_amount=action["refund_amount"],

        replacement=action["replacement"],

        compensation=action["compensation"],

        confidence=action["confidence"],

        final_decision=result["final_decision"],

        execution_trace=result["execution_trace"],

    )


# ==========================================================
# Agent Complaint Endpoint
# ==========================================================

@app.post(
    "/agent/complaint",
    response_model=AgentComplaintResponse,
)
def process_agent_complaint(

    request: ComplaintRequest,

    db: Session = Depends(get_db),

):

    result = run_graph(request)

    order = result["order_context"]

    action = result["proposed_action"]

    # ------------------------------------------------------
    # Save Complaint
    # ------------------------------------------------------

    complaint = create_complaint(

        db=db,

        order_id=request.order_id,

        complaint_text=request.complaint_text,

        category=result["category"],

        severity=result["severity"],

        sentiment=result["sentiment"],

        ai_action=action["action"],

        confidence=action["confidence"],

    )

    # ------------------------------------------------------
    # Policy Summary
    # ------------------------------------------------------

    policy_summary = []

    for chunk in result["retrieved_policy"]:

        for line in chunk.split("\n"):

            line = line.strip()

            if "Section" in line:

                policy_summary.append(line)

    policy_summary = list(dict.fromkeys(policy_summary))

    # ------------------------------------------------------
    # Historical Summary
    # ------------------------------------------------------

    historical_summary = []

    for case in result["retrieved_precedents"]:

        resolution = ""

        action_taken = ""

        lines = case.split("\n")

        for i, line in enumerate(lines):

            if line.strip() == "Resolution:":

                if i + 1 < len(lines):

                    resolution = lines[i + 1].strip()

            if line.strip() == "Action Taken:":

                if i + 1 < len(lines):

                    action_taken = lines[i + 1].strip()

        historical_summary.append(
            f"{resolution} | {action_taken}"
        )
        
        # ------------------------------------------------------
    # Build Response
    # ------------------------------------------------------

    return AgentComplaintResponse(

        complaint_id=complaint.complaint_id,

        customer=CustomerInfo(

            customer_id=order["customer_id"],
            name=order["customer_name"],
            email=order["customer_email"],
            phone=order["customer_phone"],
            tier=order["customer_tier"],

        ),

        order=OrderInfo(

            order_id=order["order_id"],
            product=order["product_name"],
            brand=order["brand"],
            category=order["product_category"],
            order_value=order["order_value"],
            delivery_status=order["delivery_status"],
            payment_status=order["payment_status"],

        ),

        complaint=result["complaint_text"],

        classification=ClassificationInfo(

            category=result["category"],
            severity=result["severity"],
            sentiment=result["sentiment"],

        ),

        recommendation=RecommendationInfo(

            action=action["action"],
            resolution_summary=action["resolution_summary"],
            refund_amount=action["refund_amount"],
            replacement=action["replacement"],
            compensation=action["compensation"],
            confidence=action["confidence"],
            reasoning=action["reasoning"],

        ),

        compliance=ComplianceInfo(

            passed=result["compliance_result"]["passed"],
            reason=result["compliance_result"]["reason"],

        ),

        policy_summary=policy_summary,

        historical_summary=historical_summary,

        execution_trace=result["execution_trace"],

    )


# ==========================================================
# Approve Complaint
# ==========================================================

@app.post(
    "/agent/approve",
    response_model=AgentActionResponse,
)
def approve_case(

    request: AgentActionRequest,

    db: Session = Depends(get_db),

):

    complaint = approve_complaint(

        db=db,

        complaint_id=request.complaint_id,

    )

    if complaint is None:

        return AgentActionResponse(

            complaint_id=request.complaint_id,

            status="Not Found",

            message="Complaint not found.",

        )

    return AgentActionResponse(

        complaint_id=complaint.complaint_id,

        status=complaint.status,

        message="Complaint approved successfully.",

    )


# ==========================================================
# Escalate Complaint
# ==========================================================

@app.post(
    "/agent/escalate",
    response_model=AgentActionResponse,
)
def escalate_case(

    request: AgentActionRequest,

    db: Session = Depends(get_db),

):

    complaint = escalate_complaint(

        db=db,

        complaint_id=request.complaint_id,

    )

    if complaint is None:

        return AgentActionResponse(

            complaint_id=request.complaint_id,

            status="Not Found",

            message="Complaint not found.",

        )

    return AgentActionResponse(

        complaint_id=complaint.complaint_id,

        status=complaint.status,

        message="Complaint escalated successfully.",

    )    