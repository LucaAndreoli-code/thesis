# routes/auth.py - Routes per autenticazione
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from src.database.database import get_db
from src.models import User
from src.models.user import pwd_context

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Modelli Pydantic
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Routes
@router.post("/login")
async def login(user_data: UserLogin,  db=Depends(get_db)):
    # Verifica username e password e ritorna token per login
    user = User(
        email=user_data.email,
    )
    user.verify_password(user_data.password, db)

    return {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
    }


@router.post("/register", response_model=dict)
async def register(user_data: UserRegister, db=Depends(get_db)):
    hashed_password = pwd_context.hash(user_data.password)
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )
    user.create_user(db)

    return {
        "email": user.email,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
    }
