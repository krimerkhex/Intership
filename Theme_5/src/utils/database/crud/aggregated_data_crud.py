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
        return new_data.id

    @staticmethod
    @db_catcher("Truncating data table")
    async def truncate_data_table(session: AsyncSession, table_name: str):
        await session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))

    @staticmethod
    async def calculate_data_aggregate(session: AsyncSession, df: pd.DataFrame, selection: str, orm_class):
        await DataCRUD.truncate_data_table(session, orm_class.__tablename__)
        agg_data = df.groupby(selection).agg({
            'business_value': 'mean',
            'liquidation_value': 'mean',
            'creditors_return': 'mean',
            'working_capital_needs': 'mean',
            'profit_before_tax': 'mean'
        })
        agg_data = agg_data.rename(columns={
            'business_value': 'avg_business_value',
            'liquidation_value': 'avg_liquidation_value',
            'creditors_return': 'avg_creditors_return',
            'working_capital_needs': 'avg_working_capital_needs',
            'profit_before_tax': 'avg_profit_before_tax',
        })
        ids = {}
        for index, row in agg_data.iterrows():
            temp = row.to_dict()
            temp[selection] = index
            ids[index] = await DataCRUD.create_data_aggregate(session, temp, orm_class)
        await session.commit()

        return ids
