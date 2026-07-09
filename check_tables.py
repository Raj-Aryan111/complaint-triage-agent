from sqlalchemy import inspect

from src.db.database import engine

inspector = inspect(engine)

print(inspector.get_table_names())