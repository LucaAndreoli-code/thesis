import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.config.config import SECRET_KEY


class JWTService:

    @staticmethod
    def generate_token(user) -> str:
        try:
            payload = {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "exp": datetime.utcnow() + timedelta(hours=24),
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            return token
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Token generation error: {str(e)}")

    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")