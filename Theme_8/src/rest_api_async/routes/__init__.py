from fastapi import APIRouter

from .db_crud_api.company_data import company_data_router
from .db_crud_api.district_aggregated_data import district_aggregated_router
from .db_crud_api.region_data import region_data_router
from .db_crud_api.industry_aggregated_data import industry_aggregated_router
from .db_crud_api.district_aggregated_data import district_aggregated_router

api_router = APIRouter(
    prefix="/api",
)

aggregated_router = APIRouter(
    prefix="/aggregate"
)

api_router.include_router(
    router=company_data_router,
)
api_router.include_router(
    router=region_data_router,
)

aggregated_router.include_router(

    router=industry_aggregated_router,
)
aggregated_router.include_router(
    router=district_aggregated_router,
)
aggregated_router.include_router(
    router=district_aggregated_router,
)

api_router.include_router(
    router=aggregated_router,
)