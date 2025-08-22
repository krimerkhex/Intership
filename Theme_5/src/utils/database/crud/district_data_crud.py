from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.models import DistrictDataORM
from utils.database.crud.db_operations import db_catcher
from utils.database.crud.common_info_district import CommonInfoDistrictCRUD


class DistrictDataCRUD:
    @staticmethod
    @db_catcher("Creating district aggregated data")
    async def create_district_aggregate_date(session: AsyncSession, district_data: dict):
        new_district = DistrictDataORM(
            district=district_data['district'],
            avg_business_value=district_data['business_value'],
            avg_liquidation_value=district_data['liquidation_value'],
            avg_creditors_return=district_data['creditors_return'],
            avg_working_capital_needs=district_data['working_capital_needs'],
            avg_profit_before_tax=district_data['profit_before_tax']
        )
        session.add(new_district)
        await session.flush()
        await session.refresh(new_district)
        return new_district

    @staticmethod
    @db_catcher("Truncating district_data table")
    async def truncate_district_data(session: AsyncSession):
        await session.execute(text('TRUNCATE TABLE district_data RESTART IDENTITY CASCADE'))

    @staticmethod
    async def calculate_district_aggregate_data(session: AsyncSession, df: pd.DataFrame):
        await DistrictDataCRUD.truncate_district_data(session)
        district_agg = df.groupby('district').agg({
            'business_value': 'mean',
            'liquidation_value': 'mean',
            'creditors_return': 'mean',
            'working_capital_needs': 'mean',
            'profit_before_tax': 'mean'
        }).reset_index()

        for _, row in district_agg.iterrows():
            await DistrictDataCRUD.create_district_aggregate_date(session, row.to_dict())
        await session.commit()

        await CommonInfoDistrictCRUD.calculate_common_district_info(session, district_agg)
