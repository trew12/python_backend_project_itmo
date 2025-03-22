FROM python:3.10-slim
WORKDIR /worker
COPY worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY worker/ ./worker
