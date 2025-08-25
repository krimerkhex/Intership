from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.crud.common_info_industry import CommonInfoIndustryCRUD
from utils.database.crud.aggregated_data_crud import DataCRUD
from utils.database.models import IndustryDataORM


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
