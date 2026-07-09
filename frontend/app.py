import requests
import streamlit as st

# ==========================================================
# Configuration
# ==========================================================

API_URL = "http://127.0.0.1:8000/complaint"

st.set_page_config(
    page_title="NovaMart AI Complaint Triage Agent",
    page_icon="🤖",
    layout="wide",
)

# ==========================================================
# Header
# ==========================================================

st.title("🤖 NovaMart AI Complaint Triage Agent")

st.caption(
    "AI-powered customer complaint resolution using LangGraph, RAG, and LLMs."
)

st.divider()

# ==========================================================
# Input Section
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    order_id = st.text_input(
        "Order ID",
        placeholder="OD562837684",
    )

with col2:

    complaint_text = st.text_input(
        "Customer Complaint",
        placeholder="My product arrived damaged.",
    )

analyze = st.button(
    "Analyze Complaint",
    use_container_width=True,
)

# ==========================================================
# Process Complaint
# ==========================================================

if analyze:

    if not order_id or not complaint_text:

        st.error("Please enter both Order ID and Complaint.")

        st.stop()

    with st.spinner("Analyzing Complaint..."):

        response = requests.post(
            API_URL,
            json={
                "order_id": order_id,
                "complaint_text": complaint_text,
            },
        )

    if response.status_code != 200:

        st.error("Backend Error")

        st.code(response.text)

        st.stop()

    result = response.json()

    st.divider()

    st.success("Complaint Processed Successfully")

    # ======================================================
    # Decision
    # ======================================================

    st.subheader("Decision")

    st.success(result["action"])

    # ======================================================
    # Metrics
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Confidence",
            f"{result['confidence']*100:.1f}%",
        )

    with c2:

        st.metric(
            "Refund",
            f"₹{result['refund_amount']}",
        )

    with c3:

        st.metric(
            "Replacement",
            "Yes" if result["replacement"] else "No",
        )

    with c4:

        st.metric(
            "Decision",
            result["final_decision"].capitalize(),
        )

    # ======================================================
    # Resolution
    # ======================================================

    st.subheader("Resolution Summary")

    st.info(result["resolution_summary"])

    # ======================================================
    # Compensation
    # ======================================================

    st.subheader("Compensation")

    st.write(result["compensation"])

    # ======================================================
    # Workflow
    # ======================================================

    st.subheader("Execution Trace")

    for step in result["execution_trace"]:

        st.write(f"✅ {step}")