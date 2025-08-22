from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.models import RegionDataORM
from utils.database.crud.db_operations import db_catcher
from utils.database.crud.common_info_region import CommonInfoRegionCRUD

class RegionDataCRUD:
    @staticmethod
    @db_catcher("Creating region aggregated data")
    async def create_region_aggregated_date(session: AsyncSession, region_data: dict):
        new_region = RegionDataORM(
            region=region_data['region'],
            avg_business_value=region_data['business_value'],
            avg_liquidation_value=region_data['liquidation_value'],
            avg_creditors_return=region_data['creditors_return'],
            avg_working_capital_needs=region_data['working_capital_needs'],
            avg_profit_before_tax=region_data['profit_before_tax']
        )
        session.add(new_region)
        await session.flush()
        await session.refresh(new_region)
        return new_region

    @staticmethod
    @db_catcher("Truncating region_data table")
    async def truncate_region_data(session: AsyncSession):
        await session.execute(text('TRUNCATE TABLE region_data RESTART IDENTITY CASCADE'))

    @staticmethod
    async def calculate_region_aggregate_data(session: AsyncSession, df: pd.DataFrame):
        await RegionDataCRUD.truncate_region_data(session)
        region_agg = df.groupby('region').agg({
            'business_value': 'mean',
            'liquidation_value': 'mean',
            'creditors_return': 'mean',
            'working_capital_needs': 'mean',
            'profit_before_tax': 'mean'
        }).reset_index()

        for _, row in region_agg.iterrows():
            await RegionDataCRUD.create_region_aggregated_date(session, row.to_dict())

        await session.commit()

        await CommonInfoRegionCRUD.calculate_common_region_info(session, region_agg)


