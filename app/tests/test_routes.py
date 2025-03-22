import datetime
from app.database import Sale


def test_submit_sales(client, monkeypatch):
    sales_data = {
        "user_id": 1,
        "sales": [
            {"date": str(datetime.date.today()), "amount": 100},
            {"date": str(datetime.date.today()), "amount": 200}
        ]
    }

    monkeypatch.setattr("app.routes.send_forecast_request", lambda *args, **kwargs: None)

    response = client.post("/submit_sales", json=sales_data)
    assert response.status_code == 200
    assert response.json() == {"status": "data received"}


def test_sales_by_date(client, override_get_db):
    today = datetime.date.today()
    db = override_get_db
    db.add(Sale(user_id=1, date=today, amount=100))
    db.commit()

    response = client.get(f"/sales_by_date?date={today}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["user_id"] == 1
    assert data[0]["amount"] == 100
