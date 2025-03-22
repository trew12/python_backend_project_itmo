from datetime import date
import json
from kafka import KafkaProducer

from app.settings import settings


producer = None


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)


def get_producer():
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=settings.kafka_server,
            value_serializer=lambda v: json.dumps(v, cls=DateTimeEncoder).encode('utf-8')
        )
    return producer


def send_forecast_request(data, topic):
    producer = get_producer()
    producer.send(topic, data.dict())

