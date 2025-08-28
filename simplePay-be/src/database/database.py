from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import DATABASE_URL

# Crea engine
engine = create_engine(DATABASE_URL)

# Crea session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency per FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()