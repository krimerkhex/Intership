from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.crud.common_info import CommonInfoCRUD


class CommonInfoDistrictCRUD:

    @staticmethod
    async def create_common_district_info(session: AsyncSession, data: dict):
        return await CommonInfoCRUD.create_common_info(session, data, CommonInfoDistrictCRUD)

    @staticmethod
    async def truncate_common_district_info(session: AsyncSession):
        await CommonInfoCRUD.truncate_common_info_table(session, "common_info_district")

    @staticmethod
    async def calculate_common_district_info(session: AsyncSession, df: pd.DataFrame):
        return await CommonInfoCRUD.calculate_common_info(session, df, 'district', CommonInfoDistrictCRUD)
