from typing import Annotated

from fastapi import APIRouter, UploadFile, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from utils.database.crud.company_data_crud import CompanyDataCRUD
from utils.database.connecting import db_connector

data_loading_router = APIRouter()

@data_loading_router.post("/upload-csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        file: UploadFile
):
    try:
        logger.debug(file.filename)
        if not file.filename.endswith(".csv"):
            raise ValueError("File must be csv.")
        count = await CompanyDataCRUD.upload_file_data(session, file)
        return {"Info": count}
    except Exception as e:  # noqa
        logger.exception(e)
        logger.error(f"Error during CSV upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
