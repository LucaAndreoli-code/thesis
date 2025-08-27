from fastapi import APIRouter

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/")
async def get_current_user() -> dict:
    # Dummy implementation for example purposes
    return {"user_id": "123", "username": "johndoe"}