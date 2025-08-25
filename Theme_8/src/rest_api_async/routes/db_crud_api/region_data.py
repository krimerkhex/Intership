from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from upload_aggregate_data.database.crud.region_aggregate_data_crud import RegionDataCRUD
from upload_aggregate_data.database.connecting import db_connector

from upload_aggregate_data.schemas.region_data import RegionDataUpdate

region_data_router = APIRouter()


@region_data_router.delete("/region-data/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_region(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        region_id: int,
):
    success = await RegionDataCRUD.delete_region_data(session, region_id=region_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found."
        )
    return {"status": "success", "data": success}


@region_data_router.patch("/region-data/{region_id}")
async def update_region(
        region_id: int,
        region_data: RegionDataUpdate,
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
):
    updated_region = await RegionDataCRUD.update_region_data(session, region_id=region_id, region_data=region_data)
    if not updated_region:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found."
        )
    return {"status": "success", "data": updated_region}
