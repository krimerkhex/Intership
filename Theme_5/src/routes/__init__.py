from fastapi import APIRouter

from data_loading.csv_upload import data_loading_router
api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(
    router=data_loading_router,
)