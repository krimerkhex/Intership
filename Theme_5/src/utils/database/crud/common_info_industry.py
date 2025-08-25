from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.crud.common_info import CommonInfoCRUD
from utils.database.models import CommonInfoIndustry


class CommonInfoIndustryCRUD:

    @staticmethod
    async def create_common_industry_info(session: AsyncSession, data: dict):
        return await CommonInfoCRUD.create_common_info(session, data, CommonInfoIndustry)

    @staticmethod
    async def truncate_common_industry_info(session: AsyncSession):
        await CommonInfoCRUD.truncate_common_info_table(session, "common_info_industry")

    @staticmethod
    async def calculate_common_industry_info(session: AsyncSession, df: pd.DataFrame, industry_ids: dict):
        return await CommonInfoCRUD.calculate_common_info(session, df, 'industry', industry_ids, CommonInfoIndustry)
