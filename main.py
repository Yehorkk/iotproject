from fastapi import FastAPI

from database import init_db
from auth import router as auth_router
from sensor_routes import router as sensor_router

init_db()

app = FastAPI(title="IoT Energy Monitoring")

app.include_router(auth_router)
app.include_router(sensor_router)
