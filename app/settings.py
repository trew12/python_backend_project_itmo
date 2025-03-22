from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@db:5432/salesdb"
    kafka_topic: str = "forecast_requests"
    kafka_server: str = "kafka:9092"


settings = Settings()
