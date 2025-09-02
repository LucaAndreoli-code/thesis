from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from migration_manager import setup_database
from src.controller.router import router

print("Starting ...")
setup_database()

app = FastAPI(title="Simple Pay", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)