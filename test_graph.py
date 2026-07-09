from pprint import pprint

from src.graph.workflow import graph

initial_state = {
    # =====================================================
    # User Input
    # =====================================================

    "order_id": "OD562837684",

    "complaint_text": "My product arrived damaged.",

    # =====================================================
    # Database
    # =====================================================

    "order_context": {},

    # =====================================================
    # Classification
    # =====================================================

    "category": None,

    "severity": None,

    "sentiment": None,

    # =====================================================
    # Retrieval
    # =====================================================

    "retrieved_policy": [],

    "retrieved_precedents": [],

    # =====================================================
    # Generation
    # =====================================================

    "draft_response": None,

    "proposed_action": {},

    # =====================================================
    # Compliance
    # =====================================================

    "compliance_result": {},

    # =====================================================
    # Workflow
    # =====================================================

    "revision_count": 0,

    "final_decision": None,

    "escalation_reason": None,

    # =====================================================
    # Logging
    # =====================================================

    "execution_trace": [],
}

result = graph.invoke(initial_state)

print("\nExecution Trace\n")

for step in result["execution_trace"]:
    print(step)

print("\nFinal State\n")

print(result)