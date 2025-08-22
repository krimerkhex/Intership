from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.models import RegionDataORM
from utils.database.crud.db_operations import db_catcher
from utils.database.crud.common_info_industry import CommonInfoIndustryCRUD
from utils.database.crud.aggregated_data_crud import DataCRUD


class IndustryDataCRUD:
    @staticmethod
    async def create_district_aggregate_date(session: AsyncSession, data: dict):
        return await DataCRUD.create_data_aggregate(session, data, IndustryDataCRUD)

    @staticmethod
    async def truncate_district_data(session: AsyncSession):
        await DataCRUD.truncate_data_table(session, "industry_data")

    @staticmethod
    async def calculate_district_aggregate_data(session: AsyncSession, df: pd.DataFrame):
        industry_agg = await DataCRUD.calculate_data_aggregate(session, df, "industry", IndustryDataCRUD)
        await CommonInfoIndustryCRUD.calculate_common_industry_info(session, industry_agg)
