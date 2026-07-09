import os

import requests
import streamlit as st

BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

API_URL = f"{BASE_URL}/agent/complaint"

APPROVE_URL = f"{BASE_URL}/agent/approve"

ESCALATE_URL = f"{BASE_URL}/agent/escalate"

st.set_page_config(
    page_title="NovaMart AI Agent Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 NovaMart AI Agent Dashboard")
st.caption("Internal AI-powered Customer Support Dashboard")

st.divider()

# ======================================================
# Input Form
# ======================================================

with st.form("complaint_form"):

    order_id = st.text_input(
        "Order ID",
        value="OD562837684",
    )

    complaint = st.text_area(
        "Customer Complaint",
        value="My product arrived damaged.",
        height=150,
    )

    submitted = st.form_submit_button(
        "Analyze Complaint",
        use_container_width=True,
    )

# ======================================================
# Call API
# ======================================================

if submitted:

    with st.spinner("Analyzing Complaint..."):

        response = requests.post(
            API_URL,
            json={
                "order_id": order_id,
                "complaint_text": complaint,
            },
        )

    if response.status_code != 200:

        st.error("Backend Error")
        st.code(response.text)
        st.stop()

    result = response.json()
    st.session_state["complaint_id"] = result["complaint_id"]

    customer = result["customer"]
    order = result["order"]
    classification = result["classification"]
    recommendation = result["recommendation"]
    compliance = result["compliance"]

    st.success("Complaint Analysis Completed")

    st.divider()

    # ==================================================
    # Customer + Order
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("👤 Customer Information")

        st.write(f"**Name:** {customer['name']}")
        st.write(f"**Customer ID:** {customer['customer_id']}")
        st.write(f"**Tier:** {customer['tier']}")
        st.write(f"**Email:** {customer['email']}")
        st.write(f"**Phone:** {customer['phone']}")

    with col2:

        st.subheader("📦 Order Information")

        st.write(f"**Order ID:** {order['order_id']}")
        st.write(f"**Product:** {order['product']}")
        st.write(f"**Brand:** {order['brand']}")
        st.write(f"**Category:** {order['category']}")
        st.write(f"**Order Value:** ₹{order['order_value']}")
        st.write(f"**Delivery:** {order['delivery_status']}")
        st.write(f"**Payment:** {order['payment_status']}")

    st.divider()

    # ==================================================
    # Complaint
    # ==================================================

    st.subheader("📝 Customer Complaint")

    st.info(result["complaint"])

    st.divider()

    # ==================================================
    # AI Recommendation
    # ==================================================

    st.subheader("🤖 AI Recommendation")

    st.success(recommendation["action"])

    st.progress(recommendation["confidence"])

    st.caption(
        f"AI Confidence : {recommendation['confidence']*100:.0f}%"
    )

    # ==================================================
    # KPI Cards
    # ==================================================

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Confidence",
            f"{recommendation['confidence']*100:.0f}%"
        )

    with m2:
        st.metric(
            "Refund",
            f"₹{recommendation['refund_amount']}"
        )

    with m3:
        st.metric(
            "Replacement",
            "YES" if recommendation["replacement"] else "NO"
        )

    with m4:
        st.metric(
            "Compensation",
            recommendation["compensation"]
        )

    # ==================================================
    # Resolution Summary
    # ==================================================

    st.divider()

    st.subheader("📄 Resolution Summary")

    st.info(
        recommendation["resolution_summary"]
    )

    # ==================================================
    # AI Reasoning
    # ==================================================

    st.subheader("🧠 AI Reasoning")

    st.write(
        recommendation["reasoning"]
    )

    # ==================================================
    # Complaint Analysis
    # ==================================================

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Category",
            classification["category"]
        )

    with c2:
        st.metric(
            "Severity",
            classification["severity"]
        )

    with c3:
        st.metric(
            "Sentiment",
            classification["sentiment"]
        )

    # ==================================================
    # Policy Applied
    # ==================================================

    st.divider()

    with st.expander("📜 Policy Applied"):

        for policy in result["policy_summary"]:
            st.write(f"• {policy}")

    # ==================================================
    # Historical Cases
    # ==================================================

    with st.expander("📚 Similar Historical Cases"):

        for i, case in enumerate(
            result["historical_summary"],
            start=1,
        ):

            st.markdown(f"**Case {i}**")

            st.write(case)

            if i != len(result["historical_summary"]):
                st.divider()

    # ==================================================
    # Workflow Execution
    # ==================================================

    with st.expander("⚙️ Workflow Execution"):

        for step in result["execution_trace"]:
            st.success(step)

    
    
        # ==================================================
    # Agent Actions
    # ==================================================

    st.divider()

    st.subheader("🛠 Agent Actions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Approve Resolution",
            use_container_width=True,
        ):

            response = requests.post(
                APPROVE_URL,
                json={
                    "complaint_id": st.session_state["complaint_id"]
                },
            )

            if response.status_code == 200:

                st.success(response.json()["message"])

            else:

                st.error("Approval failed.")

    with col2:

        if st.button(
            "🚨 Escalate Case",
            use_container_width=True,
        ):

            response = requests.post(
                ESCALATE_URL,
                json={
                    "complaint_id": st.session_state["complaint_id"]
                },
            )

            if response.status_code == 200:

                st.warning(response.json()["message"])

            else:

                st.error("Escalation failed.")        