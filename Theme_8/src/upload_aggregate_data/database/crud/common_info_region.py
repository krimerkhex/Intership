from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from upload_aggregate_data.database.crud.common_info import CommonInfoCRUD
from upload_aggregate_data.database.models import CommonInfoRegion


class CommonInfoRegionCRUD:

    @staticmethod
    async def create_common_region_info(session: AsyncSession, data: dict):
        return await CommonInfoCRUD.create_common_info(session, data, CommonInfoRegion)

    @staticmethod
    async def truncate_common_region_info(session: AsyncSession):
        await CommonInfoCRUD.truncate_common_info_table(session, "common_info_region")

    @staticmethod
    async def calculate_common_region_info(session: AsyncSession, df: pd.DataFrame, region_ids: dict):
        return await CommonInfoCRUD.calculate_common_info(session, df, 'region', region_ids, CommonInfoRegion)
