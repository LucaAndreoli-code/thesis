# main.py
from fastapi import FastAPI
from sqlalchemy import text
from src.database.database import engine
from src.database.migration_manager import setup_database
from src.controller.router import router

# Setup database all'avvio
print("Starting ...")
setup_database()

# App FastAPI
app = FastAPI(title="Simple Pay", version="1.0.0", docs_url="/docs")

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Simple Pay API"}

@app.get("/health")
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy"}
    except:
        return {"status": "error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)