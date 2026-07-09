from src.db.database import Base, engine
import src.db.models

Base.metadata.create_all(bind=engine)

print("Database created successfully!")