from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.crud.common_info_district import CommonInfoDistrictCRUD
from utils.database.crud.aggregated_data_crud import DataCRUD
from utils.database.models import DistrictDataORM


class DistrictDataCRUD:
    @staticmethod
    async def create_district_aggregate_date(session: AsyncSession, data: dict):
        return await DataCRUD.create_data_aggregate(session, data, DistrictDataORM)

    @staticmethod
    async def truncate_district_data(session: AsyncSession):
        await DataCRUD.truncate_data_table(session, "district_data")

    @staticmethod
    async def calculate_district_aggregate_data(session: AsyncSession, df: pd.DataFrame):
        district_ids = await DataCRUD.calculate_data_aggregate(session, df, "district", DistrictDataORM)
        await CommonInfoDistrictCRUD.calculate_common_district_info(session, df, district_ids)
