from src.db.crud import get_order_by_id
from src.db.database import SessionLocal

db = SessionLocal()

order = get_order_by_id(
    db,
    "OD562837684"
)

print(order)

db.close()