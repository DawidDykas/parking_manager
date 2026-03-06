import time

from app.api.modules.database import engine, sessionmaker , init_db

from fastapi import FastAPI, Depends
from app.api.routers.user_routers import user_router
import uvicorn
from log_config.logger_config import logger 

# Create initial user
from app.api.schemas.user_schemas import UserCreate
from app.api.services.user_services import UserServices

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
# -------------------------
# Lifespan context manager
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        
        await init_db(engine=engine)
        async with sessionmaker() as session:
            async with session.begin():
                try:
                    first_user = UserCreate(
                        username="admin",
                        email="admin@example.com",
                        password="SuperSecure123!"
                    )
                    user = await UserServices.user_create(first_user, session)
                    logger.info(f"First user created: {user.email}")
                except Exception as e:
                    logger.warning(f"First user not created (probably already exists): {e}")
        yield  

    finally:
        try:
            logger.info("Closing database connections...")
            await engine.dispose()
            logger.info("Database connections closed.")
        except Exception as e:
            logger.exception(f"Error during closing database connections: {e}")

# Przypisanie lifespan do FastAPI
app.router.lifespan_context = lifespan
        

# =========================
# Run server
# =========================

from app.api.run_all import start_celery, start_fastapi

if __name__ == "__main__":
    logger.info("Starting Celery worker...")
    celery_process = start_celery()

    time.sleep(2)

    logger.info("Starting FastAPI...")
    fastapi_process = start_fastapi()

    try:
        celery_process.wait()
        fastapi_process.wait()
    except KeyboardInterrupt:
        logger.info("Stopping services...")
        celery_process.terminate()
        fastapi_process.terminate()
