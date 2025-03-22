from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_topic: str = "forecast_requests"
    kafka_server: str = "kafka:9092"
    kafka_group: str = 'forecast-group'


settings = Settings()
