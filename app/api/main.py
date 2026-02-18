from app.api.modules.database import get_engine, get_sessionmaker, init_user_db
from fastapi import FastAPI
from app.api.routers.user_routers import user_router
import uvicorn
from app.api.modules.database import user_session, user_engine
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
@app.on_event("startup")
async def startup():
    try:
        logger.info("Starting application – initializing database...")
        await init_user_db(user_engine)
        logger.info("Database initialized successfully.")

        # Create first user
        first_user = UserCreate(
            username="admin",
            email="admin@example.com",
            password="SuperSecure123!"
        )

        try:
            user = await UserServices.user_create(first_user)
            logger.info(f"First user created: {user.email}")
        except Exception as e:
            logger.warning(f"First user not created (probably already exists): {e}")

    except Exception as e:
        logger.exception(f"Error during database initialization: {e}")

# =========================
# Shutdown event
# =========================
@app.on_event("shutdown")
async def shutdown():
    try:
        logger.info("Closing database connections...")
        await user_engine.dispose()
        logger.info("Database connections closed.")
    except Exception as e:
        logger.exception(f"Error during closing database connections: {e}")


        

# =========================
# Run server
# =========================
if __name__ == "__main__":
    logger.info("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run("app.api.main:app", host="127.0.0.1", port=8000, reload=True)