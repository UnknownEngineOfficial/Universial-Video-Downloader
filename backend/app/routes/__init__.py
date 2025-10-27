from fastapi import APIRouter
from .info import router as info_router
from .download import router as download_router

api_router = APIRouter()

api_router.include_router(info_router, prefix="/info", tags=["info"])
api_router.include_router(download_router, prefix="/download", tags=["download"])