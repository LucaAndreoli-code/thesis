from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from migration_manager import setup_database
from src.controller.router import router

print("Starting ...")
setup_database()

app = FastAPI(title="Simple Pay", version="1.0.0", docs_url="/docs", openapi_url="/be/openapi.json")

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"msg": "Simple Pay API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)