from fastapi import FastAPI, APIRouter, status, HTTPException, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.user_schemas import * 
from app.api.services.user_services import UserServices
from log_config.logger_config import logger
from pydantic import EmailStr
from app.api.utils.auth_wrapper import wrapper_auth_user

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/create/", response_model= UserResponse)
async def create_user(data: UserCreate):
    logger.info("Create user in database")
    return await UserServices.user_create(data)

@user_router.post("/login/", response_model = str)
async def login_user(data: UserLogin):
    logger.info(f"Login user :{data}")
    return await UserServices.login(data)

@user_router.post("/refresh")
async def refresh_token(refresh_token: str):
    logger.info(f"Refresh access token")
    return UserServices.refresh_token(refresh_token)



@user_router.get("/by-id/{id}", response_model= UserResponse)
@wrapper_auth_user
async def get_user_by_id(id: int,
                         authorization: str = Header(...)):
    
    logger.info(f"Getting user with id: {id}")
    data = UserGetById(id=id)
    return await UserServices.user_get_by_id(data)

@user_router.get("/by-email", response_model= UserResponse)
@wrapper_auth_user
async def get_user_by_email(email: EmailStr = Query(...),
                            authorization: str = Header(...)):
    
    logger.info(f"Getting user with email: {email}")
    data = UserGetByEmail(email=email)
    return await UserServices.user_get_by_email(data)


@user_router.post("/update", response_model= UserResponse)
@wrapper_auth_user
async def user_update(data: UserUpdate,
                            authorization: str = Header(...)):
    
    logger.info(f"Update user with email: {data.email}")
    return await UserServices.user_update(data)