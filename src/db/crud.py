from sqlalchemy.orm import Session

from src.db.models import (
    Complaint,
    HistoricalResolution,
    Order,
    RunLog,
)


# ==========================================================
# Orders
# ==========================================================

def get_order_by_id(
    db: Session,
    order_id: str,
):

    return (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )


# ==========================================================
# Historical Resolutions
# ==========================================================

def get_all_historical_resolutions(
    db: Session,
):

    return db.query(HistoricalResolution).all()


# ==========================================================
# Complaints
# ==========================================================

def create_complaint(
    db: Session,
    order_id: str,
    complaint_text: str,
    category: str,
    severity: str,
    sentiment: str,
    ai_action: str,
    confidence: float,
):

    complaint = Complaint(
        order_id=order_id,
        complaint_text=complaint_text,
        category=category,
        severity=severity,
        sentiment=sentiment,
        ai_action=ai_action,
        confidence=confidence,
        status="Pending",
    )

    db.add(complaint)

    db.commit()

    db.refresh(complaint)

    return complaint


def get_complaint(
    db: Session,
    complaint_id: int,
):

    return (
        db.query(Complaint)
        .filter(
            Complaint.complaint_id == complaint_id
        )
        .first()
    )


def approve_complaint(
    db: Session,
    complaint_id: int,
):

    complaint = get_complaint(
        db,
        complaint_id,
    )

    if complaint is None:
        return None

    complaint.status = "Resolved"

    db.commit()

    db.refresh(complaint)

    return complaint


def escalate_complaint(
    db: Session,
    complaint_id: int,
):

    complaint = get_complaint(
        db,
        complaint_id,
    )

    if complaint is None:
        return None

    complaint.status = "Escalated"

    db.commit()

    db.refresh(complaint)

    return complaint


def get_all_complaints(
    db: Session,
):

    return (
        db.query(Complaint)
        .order_by(
            Complaint.created_at.desc()
        )
        .all()
    )


# ==========================================================
# Run Logs
# ==========================================================

def save_run_log(
    db: Session,
    order_id: str,
    state_json: str,
    execution_time_ms: float,
    status: str,
):

    run = RunLog(
        order_id=order_id,
        state_json=state_json,
        execution_time_ms=execution_time_ms,
        status=status,
    )

    db.add(run)

    db.commit()

    db.refresh(run)

    return run


def get_run_history(
    db: Session,
):

    return (
        db.query(RunLog)
        .order_by(
            RunLog.created_at.desc()
        )
        .all()
    )