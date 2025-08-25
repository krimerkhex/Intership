from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from upload_aggregate_data.database.crud.industry_aggregate_data_crud import IndustryDataCRUD
from upload_aggregate_data.database.connecting import db_connector

industry_aggregated_router = APIRouter()


@industry_aggregated_router.get("/industry/")
async def aggregate_industry_data(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        skip: int = Query(0, ge=0, description="Количество записей, которые нужно пропустить"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей на странице"),
):
    try:
        aggregated_data = await IndustryDataCRUD.get_industry_data(session, skip, limit)
        return {"data": aggregated_data}
    except Exception as e:
        logger.exception(f"Error aggregating data by industry: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while aggregating data by industry."
        )
