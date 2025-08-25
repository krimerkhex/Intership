from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from upload_aggregate_data.database.crud.common_info import CommonInfoCRUD
from upload_aggregate_data.database.models import CommonInfoDistrict


class CommonInfoDistrictCRUD:

    @staticmethod
    async def create_common_district_info(session: AsyncSession, data: dict):
        return await CommonInfoCRUD.create_common_info(session, data, CommonInfoDistrict)

    @staticmethod
    async def truncate_common_district_info(session: AsyncSession):
        await CommonInfoCRUD.truncate_common_info_table(session, "common_info_district")

    @staticmethod
    async def calculate_common_district_info(session: AsyncSession, df: pd.DataFrame, district_ids: dict):
        return await CommonInfoCRUD.calculate_common_info(session, df, 'district', district_ids, CommonInfoDistrict)
