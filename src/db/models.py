from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from src.db.database import Base


# ==========================================================
# Orders Table
# ==========================================================

class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True, index=True)

    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)

    customer_tier = Column(String, nullable=False)

    order_date = Column(String)
    shipping_date = Column(String)
    expected_delivery_date = Column(String)
    actual_delivery_date = Column(String)

    delivery_status = Column(String)

    product_name = Column(String)
    product_category = Column(String)
    brand = Column(String)

    quantity = Column(Integer)

    unit_price = Column(Float)
    order_value = Column(Float)

    payment_method = Column(String)
    payment_status = Column(String)

    billing_address = Column(Text)
    shipping_address = Column(Text)

    courier_partner = Column(String)
    tracking_id = Column(String)

    return_history = Column(String)
    refund_history = Column(String)

    previous_orders = Column(Integer)

    warranty_expiry = Column(String)


# ==========================================================
# Historical Resolutions
# ==========================================================

class HistoricalResolution(Base):
    __tablename__ = "historical_resolutions"

    ticket_id = Column(String, primary_key=True, index=True)

    order_id = Column(String)
    customer_id = Column(String)

    complaint_text = Column(Text)

    category = Column(String)
    severity = Column(String)
    sentiment = Column(String)

    resolution_summary = Column(Text)

    action_taken = Column(String)

    refund_amount = Column(Float)

    replacement_given = Column(String)

    compensation_given = Column(String)

    policy_sections_applied = Column(String)

    agent_notes = Column(Text)

    resolution_time_hours = Column(Float)

    customer_satisfaction = Column(Integer)

    resolved_by = Column(String)

    resolution_status = Column(String)


# ==========================================================
# LangGraph Run Logs
# ==========================================================

class RunLog(Base):
    __tablename__ = "run_logs"

    run_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id = Column(
        String,
        nullable=False,
    )

    state_json = Column(
        Text,
        nullable=False,
    )

    execution_time_ms = Column(Float)

    status = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# ==========================================================
# Live Complaints
# ==========================================================

class Complaint(Base):
    __tablename__ = "complaints"

    complaint_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    order_id = Column(
        String,
        nullable=False,
    )

    complaint_text = Column(
        Text,
        nullable=False,
    )

    category = Column(String)

    severity = Column(String)

    sentiment = Column(String)

    ai_action = Column(String)

    confidence = Column(Float)

    status = Column(
        String,
        default="Pending",
    )

    assigned_to = Column(
        String,
        default="AI Agent",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )