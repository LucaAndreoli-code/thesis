from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL del database - modifica con i tuoi dati
DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/postgres"

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