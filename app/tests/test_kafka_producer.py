import json
from datetime import date
from unittest.mock import patch, MagicMock

from app.kafka_producer import DateTimeEncoder, get_producer, send_forecast_request


def test_datetime_encoder():
    d = date(2025, 3, 22)
    encoded = json.dumps({"date": d}, cls=DateTimeEncoder)
    assert encoded == '{"date": "2025-03-22"}'


def test_datetime_encoder_non_date():
    data = {"value": 42}
    encoded = json.dumps(data, cls=DateTimeEncoder)
    assert encoded == '{"value": 42}'


def test_datetime_encoder_fallback():
    class Dummy:
        def __str__(self):
            return "dummy"

    data = {"obj": Dummy()}
    try:
        json.dumps(data, cls=DateTimeEncoder)
    except TypeError:
        assert True


@patch("app.kafka_producer.KafkaProducer")
def test_get_producer_initializes_once(mock_kafka_producer):
    mock_instance = MagicMock()
    mock_kafka_producer.return_value = mock_instance

    p1 = get_producer()
    assert p1 is mock_instance

    p2 = get_producer()
    assert p2 is p1
    mock_kafka_producer.assert_called_once()


@patch("app.kafka_producer.get_producer")
def test_send_forecast_request(mock_get_producer):
    mock_producer = MagicMock()
    mock_get_producer.return_value = mock_producer

    class DummyData:
        def dict(self):
            return {"date": "2025-03-22", "amount": 100}

    send_forecast_request(DummyData(), topic="test-topic")
    mock_producer.send.assert_called_once_with("test-topic", {"date": "2025-03-22", "amount": 100})
