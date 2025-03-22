import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.crud import save_sales_data, get_sales_by_date
from app.models import SalesData, DailySale
from app.database import Base


engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)


def test_save_and_get_sales():
    db = TestingSessionLocal()
    sales_data = SalesData(
        user_id=1,
        sales=[
            DailySale(date=datetime.date.today(), amount=100),
            DailySale(date=datetime.date.today(), amount=200),
        ]
    )

    save_sales_data(sales_data, db)
    result = get_sales_by_date(datetime.date.today(), db)

    assert len(result) == 2
    assert result[0].amount == 100
    assert result[1].amount == 200
