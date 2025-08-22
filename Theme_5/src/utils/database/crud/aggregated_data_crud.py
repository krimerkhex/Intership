from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.crud.db_operations import db_catcher


class DataCRUD:
    @staticmethod
    @db_catcher("Creating data aggregate")
    async def create_data_aggregate(session: AsyncSession, data: dict, orm_class):
        new_data = orm_class(**data)
        session.add(new_data)
        await session.flush()
        await session.refresh(new_data)
        return new_data

    @staticmethod
    @db_catcher("Truncating data table")
    async def truncate_data_table(session: AsyncSession, table_name: str):
        await session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))

    @staticmethod
    async def calculate_data_aggregate(session: AsyncSession, df: pd.DataFrame, group_by: str, orm_class):
        await DataCRUD.truncate_data_table(session, orm_class.__tablename__)

        agg_data = df.groupby(group_by).agg({
            'business_value': 'mean',
            'liquidation_value': 'mean',
            'creditors_return': 'mean',
            'working_capital_needs': 'mean',
            'profit_before_tax': 'mean'
        }).reset_index()

        for _, row in agg_data.iterrows():
            await DataCRUD.create_data_aggregate(session, row.to_dict(), orm_class)
        await session.commit()

        return agg_data
