from typing import Annotated, Optional

from fastapi import APIRouter, UploadFile, status, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from upload_aggregate_data.database.crud.company_data_crud import CompanyDataCRUD
from upload_aggregate_data.database.connecting import db_connector
from upload_aggregate_data.kafka.producer.producer import send_to_kafka

company_data_router = APIRouter()


@company_data_router.post("/upload-csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        file: UploadFile
):
    try:
        logger.debug(file.filename)
        if not file.filename.endswith(".csv"):
            raise ValueError("File must be csv.")
        data = await file.read()
        message = {"file": data.decode()}
        await send_to_kafka(message)
        return {"Info": "Message dropped to kafka"}

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )

    except Exception as e:  # noqa
        logger.exception(e)
        logger.error(f"Error during CSV upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@company_data_router.get("/company-data/")
async def read_company_data(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        skip: int = Query(0, ge=0, description="Количество записей, которые нужно пропустить"),
        limit: int = Query(100, ge=1, le=1000, description="Максимальное количество записей на странице"),
        region_name: Optional[str] = Query(None, description="Фильтрация по региону"),
):
    try:
        result = await CompanyDataCRUD.get_filtered_data(session, region_name, skip, limit)
        return result
    except Exception as e:
        logger.exception(f"Error fetching company data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while fetching company data."
        )
