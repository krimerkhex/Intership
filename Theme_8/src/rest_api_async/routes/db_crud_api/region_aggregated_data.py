from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from upload_aggregate_data.database.crud.region_aggregate_data_crud import RegionDataCRUD
from upload_aggregate_data.database.connecting import db_connector

region_aggregated_router = APIRouter()


@region_aggregated_router.get("/region/")
async def aggregate_region_data(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        skip: int = Query(0, ge=0, description="Количество записей, которые нужно пропустить"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей на странице"),
):
    try:
        aggregated_data = await RegionDataCRUD.get_region_data(session, skip, limit)
        return {"data": aggregated_data}
    except Exception as e:
        logger.exception(f"Error aggregating data by region: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while aggregating data by region."
        )
