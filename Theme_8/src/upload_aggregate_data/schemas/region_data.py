from pydantic import BaseModel
from typing import Optional


class RegionDataUpdate(BaseModel):
    avg_business_value: Optional[float]
    avg_liquidation_value: Optional[float]
    avg_creditors_return: Optional[float]
    avg_working_capital_needs: Optional[float]
    avg_profit_before_tax: Optional[float]
