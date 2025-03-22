from fastapi import FastAPI

from app.routes import router
from app.metrics import setup_metrics


app = FastAPI(title="Sales Forecast Service")
setup_metrics(app)
app.include_router(router)
