import os

import requests
import streamlit as st

BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

API_URL = f"{BASE_URL}/complaint"

st.set_page_config(
    page_title="NovaMart Customer Support",
    page_icon="🛍️",
    layout="centered",
)

# ==========================================================
# Header
# ==========================================================

st.title("🛍️ NovaMart Customer Support")

st.write(
    "Need help with your order? Submit your complaint below and "
    "our AI-powered support system will review it instantly."
)

st.divider()

# ==========================================================
# Complaint Form
# ==========================================================

with st.form("customer_form"):

    order_id = st.text_input(
        "Order ID",
        placeholder="OD562837684",
    )

    complaint = st.text_area(
        "Describe your issue",
        height=180,
        placeholder="Example: My product arrived damaged and I would like a replacement.",
    )

    submit = st.form_submit_button(
        "Submit Complaint",
        use_container_width=True,
    )

# ==========================================================
# Process Complaint
# ==========================================================

if submit:

    if not order_id or not complaint:

        st.error("Please fill in all fields.")

        st.stop()

    with st.spinner("Reviewing your complaint..."):

        response = requests.post(
            API_URL,
            json={
                "order_id": order_id,
                "complaint_text": complaint,
            },
        )

    if response.status_code != 200:

        st.error("Something went wrong. Please try again later.")

        st.stop()

    result = response.json()

    st.divider()

    st.success("Complaint Processed Successfully")

    st.subheader("Resolution")

    st.info(result["customer_message"])

    st.subheader("Status")

    if result["replacement"]:

        st.success("✅ Replacement Approved")

    elif result["refund_amount"] > 0:

        st.success(f"💰 Refund Approved (₹{result['refund_amount']})")

    else:

        st.success(result["action"])

    if result["compensation"]:

        st.subheader("Compensation")

        st.write(result["compensation"])

    st.divider()

    st.caption(
        "Reference: "
        + order_id
    )

    st.write(
        "If you have any additional questions, please contact NovaMart Customer Support."
    )