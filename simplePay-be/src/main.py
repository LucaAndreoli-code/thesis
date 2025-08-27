from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller.v1.user import user_router

app = FastAPI(
    title="two factor API",
    description="API for two factor authentication",
    version="0.0.1",
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

@app.get("/")
def root():
    return {"message": "Hello coder!"}