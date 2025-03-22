import pytest
from kafka.errors import NoBrokersAvailable

from worker.consumer import fake_forecast, get_consumer, consume_events


def test_fake_forecast_with_sales():
    sales_data = [{'amount': 100.0}, {'amount': 200.0}, {'amount': 300.0}]
    result = fake_forecast(sales_data)
    assert result == 200.0


def test_fake_forecast_with_empty_list():
    assert fake_forecast([]) == 0.0


def test_get_consumer(mock_settings, mocker):
    mock_kafka_consumer = mocker.patch('worker.consumer.KafkaConsumer')
    consumer_instance = mocker.MagicMock()
    mock_kafka_consumer.return_value = consumer_instance

    consumer = get_consumer()
    assert consumer == consumer_instance
    mock_kafka_consumer.assert_called_once()


def test_get_consumer_retries_on_failure(mocker):
    mock_kafka_consumer = mocker.patch('worker.consumer.KafkaConsumer')
    mock_kafka_consumer.side_effect = [NoBrokersAvailable, NoBrokersAvailable, mocker.MagicMock()]

    mock_sleep = mocker.patch('time.sleep')

    consumer = get_consumer(retries=3, delay=0)
    assert consumer is not None
    assert mock_kafka_consumer.call_count == 3
    assert mock_sleep.call_count == 2


def test_get_consumer_raises_after_max_retries(mocker):
    mock_kafka_consumer = mocker.patch('worker.consumer.KafkaConsumer')
    mock_kafka_consumer.side_effect = NoBrokersAvailable

    mocker.patch('time.sleep')

    with pytest.raises(RuntimeError, match="Kafka is not available after multiple retries."):
        get_consumer(retries=3, delay=0)

    assert mock_kafka_consumer.call_count == 3


def test_consume_events(mocker):
    mock_logger = mocker.patch('worker.consumer.logger')
    mock_get_consumer = mocker.patch('worker.consumer.get_consumer')

    mock_message = mocker.MagicMock()
    mock_message.value = {
        'user_id': 123,
        'sales': [{'amount': 100}, {'amount': 200}]
    }

    mock_get_consumer.return_value = [mock_message]

    consume_events()

    mock_logger.info.assert_any_call("[Consumer] Listening for forecast requests...")
    mock_logger.info.assert_any_call("[User 123] Forecast: 150.0")
