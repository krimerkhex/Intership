from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.models import RegionDataORM
from utils.database.crud.aggregated_data_crud import DataCRUD
from utils.database.crud.common_info_region import CommonInfoRegionCRUD


class RegionDataCRUD:
    @staticmethod
    async def create_region_aggregated_date(session: AsyncSession, data: dict):
        return await DataCRUD.create_data_aggregate(session, data, RegionDataORM)

    @staticmethod
    async def truncate_region_data(session: AsyncSession):
        await DataCRUD.truncate_data_table(session, "region_data")

    @staticmethod
    async def calculate_region_aggregate_data(session: AsyncSession, df: pd.DataFrame):
        region_agg = await DataCRUD.calculate_data_aggregate(session, df, "region", RegionDataORM)
        await CommonInfoRegionCRUD.calculate_common_region_info(session, region_agg)
