from langgraph.graph import StateGraph, START, END

from src.schemas.state import ComplaintState

from src.nodes.nodes import (
    load_order_node,
    classify_node,
    retrieve_policy_node,
    retrieve_historical_node,
    draft_response_node,
    compliance_node,
    router_node,
    revise_node,
    escalate_node,
    send_response_node,
)

# ==========================================================
# Create Graph Builder
# ==========================================================

builder = StateGraph(ComplaintState)

# ==========================================================
# Register Nodes
# ==========================================================

builder.add_node("load_order", load_order_node)

builder.add_node("classify", classify_node)

builder.add_node("retrieve_policy", retrieve_policy_node)

builder.add_node("retrieve_historical", retrieve_historical_node)

builder.add_node("draft_response", draft_response_node)

builder.add_node("compliance", compliance_node)

builder.add_node("revise", revise_node)

builder.add_node("escalate", escalate_node)

builder.add_node("send", send_response_node)

# ==========================================================
# Main Flow
# ==========================================================

builder.add_edge(START, "load_order")

builder.add_edge("load_order", "classify")

builder.add_edge("classify", "retrieve_policy")

builder.add_edge("retrieve_policy", "retrieve_historical")

builder.add_edge("retrieve_historical", "draft_response")

builder.add_edge("draft_response", "compliance")

# ==========================================================
# Conditional Routing
# ==========================================================

builder.add_conditional_edges(
    "compliance",
    router_node,
    {
        "send": "send",
        "revise": "revise",
        "escalate": "escalate",
    },
)

# ==========================================================
# Revision Loop
# ==========================================================

builder.add_edge("revise", "draft_response")

# ==========================================================
# Exit Nodes
# ==========================================================

builder.add_edge("send", END)

builder.add_edge("escalate", END)

# ==========================================================
# Compile Graph
# ==========================================================

def build_graph():
    return builder.compile()


graph = build_graph()