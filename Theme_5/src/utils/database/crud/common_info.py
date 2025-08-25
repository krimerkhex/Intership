from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from utils.database.models import CommonInfoRegion
from utils.database.crud.db_operations import db_catcher


class CommonInfoCRUD:
    @staticmethod
    @db_catcher("Creating common info")
    async def create_common_info(session: AsyncSession, data: dict, orm_class):
        new_info = orm_class(
            **data
        )
        session.add(new_info)
        await session.flush()
        await session.refresh(new_info)
        return new_info

    @staticmethod
    @db_catcher("Truncating common_info_region table")
    async def truncate_common_info_table(session: AsyncSession, table_name: str):
        await session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))
        await session.commit()

    @staticmethod
    async def calculate_common_info(session: AsyncSession, df: pd.DataFrame, selection: str, records_ids: dict,
                                    orm_class):
        region_agg = df.groupby(selection).agg({
            'ID': 'count',
            'business_value': lambda x: (x > 0).sum(),
            'profit_before_tax': lambda x: (x > 0).sum(),
            'tax_debt': lambda x: (x == 0).sum(),
            'solvency_rank': lambda x: (x > 0).sum(),
            'working_capital_needs': lambda x: (x != 0).sum()
        }).rename(columns={
            'ID': 'total_companies',
            'business_value': 'companies_with_business_value',
            'profit_before_tax': 'profitable_companies',
            'tax_debt': 'debt_free_companies',
            'solvency_rank': 'solvent_companies',
            'working_capital_needs': 'companies_with_asset_profitability'
        })

        for index, row in region_agg.iterrows():
            temp = row.to_dict()
            temp[f"{selection}_id"] = records_ids[index]
            await CommonInfoCRUD.create_common_info(session, temp, orm_class)
        await session.commit()
