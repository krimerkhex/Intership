import copy
from typing import Hashable

from fastapi import File
from pandas import Series
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd
from loguru import logger

from utils.database.models import CompanyDataORM

BANKRUPTCY_COLUMN = "возбуждено производство по делу о несостоятельности (банкротстве)"


async def swipe_time(index: Hashable, row: Series) -> dict:
    """
    This function need's because i misunderstanding of data format in task.
    """
    result = {"company_name": index[0], "inn": str(index[1]), BANKRUPTCY_COLUMN: [*row.values, *index[2:]]}

    return result


class CompanyDataCRUD:
    @staticmethod
    async def create_company_data(
            session: AsyncSession,
            company_data: dict
    ) -> CompanyDataORM:
        logger.debug(company_data)
        logger.info("Creating an account_number record")
        main_data = {k: v for k, v in company_data.items()
                     if not k.startswith("возбуждено производство")}
        bankruptcy_data = {k: v for k, v in company_data.items()
                           if k.startswith("возбуждено производство")}

        new_company = CompanyDataORM(
            **main_data,
            bankruptcy_data=bankruptcy_data
        )
        session.add(new_company)

        try:
            await session.flush()

        except SQLAlchemyError as e:
            logger.error(e)
            await session.rollback()
            raise

        await session.refresh(new_company)
        return new_company

    @staticmethod
    async def truncate_company_data(
            session: AsyncSession,
    ):
        logger.info("Truncating account_number record's")
        await session.execute(text('TRUNCATE TABLE company_data RESTART IDENTITY CASCADE'))
        await session.commit()

    @staticmethod
    async def upload_file_data(
            session: AsyncSession,
            csv_file: File
    ) -> dict:
        logger.info("Uploading file data to DB")
        await CompanyDataCRUD.truncate_company_data(session)
        df = pd.read_csv(csv_file.file)
        if BANKRUPTCY_COLUMN not in df.columns:
            raise ValueError(f"Column '{BANKRUPTCY_COLUMN}' not found")

        count = 0

        for index, row in df.iterrows():
            try:
                await CompanyDataCRUD.create_company_data(session, await swipe_time(index, row))
                count += 1
            except SQLAlchemyError:
                pass
        await session.commit()

        return {"Added": count, "Rejected": len(df) - count}
