from sqlalchemy import Column, Integer, String, JSON, Float, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CompanyDataORM(Base):
    __tablename__ = 'company_data'
    id = Column(Integer, primary_key=True)
    okved = Column(String(10), nullable=False)
    okved_decoding = Column(String(255), nullable=False)
    industry = Column(String(512), nullable=False)
    region = Column(String(255), nullable=False)
    district = Column(String(255), nullable=False)
    business_value = Column(Float, nullable=True)
    liquidation_value = Column(Float, nullable=True)
    creditors_return = Column(Float, nullable=True)
    working_capital_needs = Column(Float, nullable=True)
    profit_before_tax = Column(Float, nullable=True)
    tax_debt = Column(Float, nullable=True)
    enforcement_proceedings = Column(Float, nullable=True)
    guarantee_limit = Column(String(255), nullable=True)
    solvency_rank = Column(Float, nullable=True)
    company_age = Column(Float, nullable=True)
    bankruptcy_data = Column(JSON, nullable=False)


class DataORM:
    __abstract__ = True

    avg_business_value = Column(Float, default=0.0)
    avg_liquidation_value = Column(Float, default=0.0)
    avg_creditors_return = Column(Float, default=0.0)
    avg_working_capital_needs = Column(Float, default=0.0)
    avg_profit_before_tax = Column(Float, default=0.0)


class RegionDataORM(Base, DataORM):
    __tablename__ = 'region_data'

    id = Column(Integer, primary_key=True)
    region = Column(String(128), nullable=False)
    common_region_info = relationship("CommonInfoRegion", back_populates="common_info")


class DistrictDataORM(Base, DataORM):
    __tablename__ = 'district_data'

    id = Column(Integer, primary_key=True)
    district = Column(String(128), nullable=False)
    common_district_info = relationship("CommonInfoDistrict", back_populates="common_info")


class IndustryDataORM(Base, DataORM):
    __tablename__ = 'industry_data'

    id = Column(Integer, primary_key=True)
    industry = Column(String(128), nullable=False)
    common_industry_info = relationship("CommonInfoIndustry", back_populates="common_info")


class CommonInfo:
    __abstract__ = True
    total_companies = Column(Integer)
    companies_with_business_value = Column(Integer)
    profitable_companies = Column(Integer)
    debt_free_companies = Column(Integer)
    solvent_companies = Column(Integer)
    companies_with_asset_profitability = Column(Integer)


class CommonInfoRegion(Base, CommonInfo):
    __tablename__ = 'common_info_region'

    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('region_data.id'), unique=True)
    common_info = relationship("RegionDataORM", back_populates="common_region_info")


class CommonInfoDistrict(Base, CommonInfo):
    __tablename__ = 'common_info_district'

    id = Column(Integer, primary_key=True)
    district_id = Column(Integer, ForeignKey('district_data.id'), unique=True)
    common_info = relationship("DistrictDataORM", back_populates="common_district_info")


class CommonInfoIndustry(Base, CommonInfo):
    __tablename__ = 'common_info_industry'

    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer, ForeignKey('industry_data.id'), unique=True)
    common_info = relationship("IndustryDataORM", back_populates="common_industry_info")
