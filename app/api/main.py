import time

from fastapi import FastAPI, Depends
from app.api.routers.user_routers import user_router
from log_config.logger_config import logger 
import asyncio
# =========================
# FastAPI app
# =========================
app = FastAPI()
app.include_router(user_router)

# =========================
# Startup event
# =========================
from contextlib import asynccontextmanager
from fastapi import FastAPI
from log_config.logger_config import logger
from app.api.modules.database import engine
from app.api.services.user_services import UserServices
from app.api.schemas.user_schemas import UserCreate
from app.api.routers.drive_routers import drive_router

app = FastAPI(title="Parking Manager API")
app.include_router(user_router)
app.include_router(drive_router)



# =========================
# Run server
# =========================

from app.api.run_all import run_all

if __name__ == "__main__":
    asyncio.run(run_all())