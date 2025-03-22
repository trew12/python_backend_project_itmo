from datetime import date
from pydantic import BaseModel
from typing import List


class DailySale(BaseModel):
    date: date
    amount: float


class SalesData(BaseModel):
    user_id: int
    sales: List[DailySale]


class SaleRecord(BaseModel):
    id: int
    user_id: int
    date: date
    amount: float

    class Config:
        orm_mode = True
