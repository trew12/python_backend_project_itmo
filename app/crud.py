from datetime import date
from sqlalchemy.orm import Session

from app.models import SalesData
from app.database import Sale


def save_sales_data(data: SalesData,  db: Session):
    for item in data.sales:
        db_sale = Sale(user_id=data.user_id, date=item.date, amount=item.amount)
        db.add(db_sale)
    db.commit()
    db.close()


def get_sales_by_date(query_date: date,  db: Session):
    sales = db.query(Sale).filter(Sale.date == query_date).all()
    return sales
