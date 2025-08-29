from fastapi import APIRouter
from src.controller.v1.auth import router as auth_router
from src.controller.v1.transaction import router as transaction_router
from src.controller.v1.wallet import router as wallet_router

router = APIRouter(prefix='/api/v1')

router.include_router(auth_router)
router.include_router(transaction_router)
router.include_router(wallet_router)