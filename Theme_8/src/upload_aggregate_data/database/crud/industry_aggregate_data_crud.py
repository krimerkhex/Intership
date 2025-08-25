from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from upload_aggregate_data.database.crud.common_info_industry import CommonInfoIndustryCRUD
from upload_aggregate_data.database.crud.aggregated_data_crud import DataCRUD
from upload_aggregate_data.database.models import IndustryDataORM


class IndustryDataCRUD:
    @staticmethod
    async def create_industry_aggregate_date(session: AsyncSession, data: dict):
        return await DataCRUD.create_data_aggregate(session, data, IndustryDataORM)

    @staticmethod
    async def truncate_industry_data(session: AsyncSession):
        await DataCRUD.truncate_data_table(session, "industry_data")

    @staticmethod
    async def calculate_industry_aggregate_data(session: AsyncSession, df: pd.DataFrame):
        industry_ids = await DataCRUD.calculate_data_aggregate(session, df, "industry", IndustryDataORM)
        await CommonInfoIndustryCRUD.calculate_common_industry_info(session, df, industry_ids)

    @staticmethod
    async def get_industry_data(session: AsyncSession, skip: int, limit: int):
        return await DataCRUD.get_data(session, IndustryDataORM, skip, limit)

    @staticmethod
    async def get_industry_data_by_id(session: AsyncSession, industry_id: int):
        return await DataCRUD.get_data_aggregate_by_id(session, industry_id, IndustryDataORM)
