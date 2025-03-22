import json
from kafka import KafkaConsumer, errors
import logging
import time

from worker.settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_consumer(retries=10, delay=5):
    for attempt in range(1, retries + 1):
        try:
            return KafkaConsumer(
                settings.kafka_topic,
                bootstrap_servers=settings.kafka_server,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                group_id=settings.kafka_group,
                enable_auto_commit=True
            )
        except errors.NoBrokersAvailable:
            logger.warning(f"[Attempt {attempt}] Kafka not available, retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("Kafka is not available after multiple retries.")


def fake_forecast(sales):
    if not sales:
        return 0.0
    return sum(s['amount'] for s in sales) / len(sales)


def consume_events():
    consumer = get_consumer()
    logger.info("[Consumer] Listening for forecast requests...")
    for msg in consumer:
        payload = msg.value
        user_id = payload.get('user_id')
        sales = payload.get('sales', [])
        forecast = fake_forecast(sales)
        logger.info(f"[User {user_id}] Forecast: {forecast}")


if __name__ == '__main__':  # pragma: no cover
    consume_events()
