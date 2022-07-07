from api.general_page import general_page_router
from fastapi import APIRouter

api_router = APIRouter(prefix="")
api_router.include_router(
    general_page_router, prefix="", tags=["general_page"]
)
