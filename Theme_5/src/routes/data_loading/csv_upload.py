from fastapi import APIRouter, UploadFile, status, HTTPException, Depends
from loguru import logger

from utils.database.company_data_crud import CompanyDataCRUD
from utils.database.connecting import db_connector

data_loading_router = APIRouter()


@data_loading_router.post("/upload-csv", status_code=status.HTTP_201_CREATED)
async def upload_csv(
        session: Annotated[AsyncSession, Depends(db_connector.session_getter)],
        file: UploadFile
):
    try:
        if file.filename.endswith(".csv"):
            count = CompanyDataCRUD.upload_file_data(session, file)
            return {"Uploaded rows": count}
        else:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="File must be csv."
            )
    except Exception as e:  # noqa
        logger.error(f"Error during CSV upload: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
