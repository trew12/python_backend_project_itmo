from datetime import date
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import SalesData, SaleRecord
from app.crud import get_sales_by_date, save_sales_data
from app.kafka_producer import send_forecast_request
from app.settings import settings


router = APIRouter()


@router.get("/sales_by_date", response_model=List[SaleRecord])
def sales_by_date(date: date = Query(...), db: Session = Depends(get_db)):
    return get_sales_by_date(date, db)


@router.post("/submit_sales")
def submit_sales(data: SalesData, db: Session = Depends(get_db)):
    save_sales_data(data, db)
    send_forecast_request(data, topic=settings.kafka_topic)
    return {"status": "data received"}
