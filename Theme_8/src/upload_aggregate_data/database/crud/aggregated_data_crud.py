from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd
from sqlalchemy.future import select

from upload_aggregate_data.schemas.region_data import RegionDataUpdate
from upload_aggregate_data.database.crud.db_operations import db_catcher


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

    @staticmethod
    async def get_data_aggregate_by_id(session: AsyncSession, record_id: int, orm_class) -> Any:
        record = await session.get(entity=orm_class, ident=record_id)
        if record is None:
            raise ValueError
        return record

    @staticmethod
    async def delete_data_aggregate(session: AsyncSession, record_id: int, orm_class):
        record = await DataCRUD.get_data_aggregate_by_id(session, record_id, orm_class)
        await session.delete(record)
        await session.commit()
        return record

    @staticmethod
    async def update_data_aggregate(session: AsyncSession, record_id: int, region_data: RegionDataUpdate, orm_class):
        record = await DataCRUD.get_data_aggregate_by_id(session, record_id, orm_class)
        if record:
            for key, value in region_data.model_dump(exclude_unset=True).items():
                setattr(record, key, value)
            await session.commit()
        return record

    @staticmethod
    async def get_data(session: AsyncSession, orm_class, skip: int = 0, limit: int = 100):
        stmt = select(orm_class).offset(skip).limit(limit)
        result = await session.scalars(statement=stmt)
        return result.all()
