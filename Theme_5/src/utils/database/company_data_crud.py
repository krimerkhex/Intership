from fastapi import File
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd
from loguru import logger

from utils.database.models import CompanyDataORM


class CompanyDataCRUD:
    BANKRUPTCY_COLUMN = "возбуждено производство по делу о несостоятельности (банкротстве)"

    @staticmethod
    async def create_company_data(
            session: AsyncSession,
            company_data: dict
    ) -> CompanyDataORM:
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

        except SQLAlchemyError:
            await session.rollback()
            raise

        await session.refresh(new_company)
        return new_company

    @staticmethod
    async def truncate_company_data(
            session: AsyncSession,
    ):
        logger.info("Truncating account_number record's")
        await session.execute('TRUNCATE TABLE company_data RESTART IDENTITY CASCADE')
        await session.commit()
        logger.info("Truncating account_number record's")

    @staticmethod
    async def upload_file_data(
            session: AsyncSession,
            csv_file: File
    ) -> dict:
        logger.info("Uploading file data to DB")
        await CompanyDataCRUD.truncate_company_data(session)
        df = pd.read_csv(csv_file.file)
        if CompanyDataCRUD.BANKRUPTCY_COLUMN not in df.columns:
            raise ValueError(f"Column '{CompanyDataCRUD.BANKRUPTCY_COLUMN}' not found")

        count = 0

        for _, row in df.iterrows():
            try:
                await CompanyDataCRUD.create_company_data(session, row.to_dict())
                count += 1
            except SQLAlchemyError:
                pass

        return {"Added": count, "Rejected": len(df) - count}
