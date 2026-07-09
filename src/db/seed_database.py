from pathlib import Path

import pandas as pd

from src.db.database import Base, SessionLocal, engine
from src.db.models import (
    Complaint,
    HistoricalResolution,
    Order,
)

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ORDERS_CSV = BASE_DIR / "data" / "orders" / "orders.csv"

HISTORICAL_CSV = (
    BASE_DIR
    / "data"
    / "precedents"
    / "historical_resolution_dataset.csv"
)


# ==========================================================
# Helper Functions
# ==========================================================

def clean_currency(value):
    """
    Converts

    ₹210.00
    ₹11,523.00
    ₹0

    into

    210.0
    11523.0
    0.0
    """

    if pd.isna(value):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value)

    value = value.replace("₹", "")
    value = value.replace(",", "")
    value = value.strip()

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


# ==========================================================
# Seed Database
# ==========================================================

def seed_database():

    print("=" * 60)
    print("Seeding Database...")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # Clear Existing Data
        # --------------------------------------------------

        db.query(Order).delete()

        db.query(HistoricalResolution).delete()

        db.query(Complaint).delete()

        db.commit()

        # --------------------------------------------------
        # Orders
        # --------------------------------------------------

        print("Loading Orders...")

        orders_df = pd.read_csv(ORDERS_CSV)

        order_objects = []

        for _, row in orders_df.iterrows():

            data = row.to_dict()

            data["unit_price"] = clean_currency(
                data["unit_price"]
            )

            data["order_value"] = clean_currency(
                data["order_value"]
            )

            order_objects.append(
                Order(**data)
            )

        db.bulk_save_objects(order_objects)

        db.commit()

        print(
            f"Inserted {len(order_objects)} orders."
        )

        # --------------------------------------------------
        # Historical Resolutions
        # --------------------------------------------------

        print("Loading Historical Resolutions...")

        historical_df = pd.read_csv(HISTORICAL_CSV)

        historical_objects = []

        for _, row in historical_df.iterrows():

            data = row.to_dict()

            data["refund_amount"] = clean_currency(
                data["refund_amount"]
            )

            historical_objects.append(
                HistoricalResolution(**data)
            )

        db.bulk_save_objects(
            historical_objects
        )

        db.commit()

        print(
            f"Inserted {len(historical_objects)} historical resolutions."
        )

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        print()

        print("=" * 60)
        print("Database seeded successfully!")
        print("=" * 60)

        print(
            f"Orders                     : {len(order_objects)}"
        )

        print(
            f"Historical Resolutions     : {len(historical_objects)}"
        )

        print(
            "Complaints                : 0"
        )

        print("=" * 60)

    except Exception as e:

        db.rollback()

        print()
        print("=" * 60)
        print("Database seeding failed!")
        print("=" * 60)

        raise e

    finally:

        db.close()


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    seed_database()