from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CompanyDataORM(Base):
    __tablename__ = 'company_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(512), nullable=True)
    inn = Column(String(10), nullable=True)
    bankruptcy_data = Column(JSON, nullable=False)
