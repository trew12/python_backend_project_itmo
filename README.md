# 📊 Sales Forecasting

## 📌 Бизнесовая задача
Сервис для расчета прогноза продаж на основе пользовательских данных. Для простоты консьюмер выдает в лог усреднение по продажам. 
---
- `sales-app` — FastAPI-сервер с REST API, принимает запросы, сохраняет данные в PostgreSQL и публикует события в Kafka.
- `sales-worker` — Kafka-консьюмер, обрабатывающий события.
- `sales-db` — PostgreSQL, основное хранилище данных.
- `kafka`, `zookeeper` — инфраструктура брокера сообщений.
- `prometheus`, `grafana` — мониторинг и визуализация метрик.
- Запускается одной командой `docker compose up`.

## 🚀 Как запустить

```bash
git clone https://github.com/trew12/python_backend_project_itmo.git
cd python_backend_project_itmo
docker compose up --build
```

После запуска:
- FastAPI доступен по адресу: ```http://localhost:8000```
- Grafana: ```http://localhost:3000```
- Prometheus: ```http://localhost:9090```
