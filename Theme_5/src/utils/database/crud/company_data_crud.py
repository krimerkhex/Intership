from fastapi import File
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd
from loguru import logger

from utils.database.models import CompanyDataORM
from utils.database.crud.region_data_crud import RegionDataCRUD
from utils.database.crud.district_data_crud import DistrictDataCRUD
from utils.database.crud.industry_data_crud import IndustryDataCRUD

BANKRUPTCY_COLUMN = "возбуждено производство по делу о несостоятельности (банкротстве)"

NAME_MAPPER = {
    "оквэд": "okved",
    "расшифровка оквэд": "okved_decoding",
    "Отрасль": "industry",
    "Субъект": "region",
    "Округ": "district",
    "текущая стоимость бизнеса": "business_value",
    "ликвидационная стоимость бизнеса": "liquidation_value",
    "расчёт возвратности средств для кредиторов": "creditors_return",
    "потребность в оборотных средствах": "working_capital_needs",
    "прибыль до налогообложения": "profit_before_tax",
    "задолженность по налогам": "tax_debt",
    "исполнительное производство без учета налогов": "enforcement_proceedings",
    "Лимит поручительства": "guarantee_limit",
    "ранг платежеспособности": "solvency_rank",
    "возраст организации": "company_age",
    "возбуждено производство по делу о несостоятельности (банкротстве)": "bankruptcy_data"
}


def process_csv_row(data: dict) -> dict:
    """
    Separates row data into main_data and bankruptcy_data
    """
    bankruptcy_started = False
    main_data = {"bankruptcy_data": {}}

    for key, value in data.items():

        if "Unnamed" in key or NAME_MAPPER.get(key, None) is None:
            continue
        if key == BANKRUPTCY_COLUMN:
            bankruptcy_started = True

        if bankruptcy_started:
            main_data["bankruptcy_data"][key] = value
        else:
            main_data[key] = value
    return main_data


class CompanyDataCRUD:
    @staticmethod
    async def create_company_data(
            session: AsyncSession,
            company_data: dict
    ) -> CompanyDataORM:
        new_company = CompanyDataORM(
            **company_data
        )
        session.add(new_company)
        await session.refresh(new_company)
        return new_company

    @staticmethod
    async def truncate_company_data(
            session: AsyncSession,
    ):
        await session.execute(text('TRUNCATE TABLE company_data RESTART IDENTITY CASCADE'))

    @staticmethod
    async def upload_file_data(
            session: AsyncSession,
            csv_file: File
    ) -> dict:
        logger.info("Uploading file data to DB")
        await CompanyDataCRUD.truncate_company_data(session)
        df = pd.read_csv(csv_file.file)
        df.rename(columns=NAME_MAPPER)
        if BANKRUPTCY_COLUMN not in df.columns:
            raise ValueError(f"Column '{BANKRUPTCY_COLUMN}' not found")

        count = 0

        for _, row in df.iterrows():
            try:
                processed = process_csv_row(row.to_dict())
                await CompanyDataCRUD.create_company_data(session, processed)
                count += 1
            except SQLAlchemyError:
                pass
        await session.commit()

        await RegionDataCRUD.calculate_region_aggregate_data(session, df)
        await DistrictDataCRUD.calculate_district_aggregate_data(session, df)
        await IndustryDataCRUD.calculate_industry_aggregate_data(session, df)

        return {"Added": count, "Rejected": len(df) - count}
