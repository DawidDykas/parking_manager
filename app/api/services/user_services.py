from app.api.repositories.user_repo import * 
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.user_schemas import * 
from log_config.logger_config import logger
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.api.security.security import hash_password, verify_password
from app.api.security.jwt_auth import create_access_token, verify_token




class UserServices: 
    async def user_create(data: UserCreate, session: AsyncSession) -> UserResponse:
        data.password = hash_password(data.password)
        logger.info("Create user in database")
        try:
            user = await UserRepository.create(
                session=session,
                data=data
            )
            return user

        except IntegrityError as e:
            logger.warning(f"Email already exists: {data.email}")

            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    async def user_update(data: UserUpdate, session: AsyncSession) -> UserResponse:
        try:
            updated_user = await UserRepository.update(session, data)
            logger.info(f"User updated successfully: {data.id}")
            return updated_user

        except HTTPException as e:
            logger.error(f"Error updating user {data.id}: {e.detail}")
            raise  


    async def user_get_by_id(data: UserGetById, session: AsyncSession) -> UserResponse:
        logger.info(f"Fetching user with id={data.id}")
        
        user = await UserRepository.get_by_id(session=session, data=data)
        
        if not user:
            logger.warning(f"User with id={data.id} not found")
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        logger.info(f"User fetched successfully: {user.id}")
        return user


    async def user_get_by_email(data: UserGetByEmail, session: AsyncSession) -> UserResponse:
        logger.info(f"Fetching user with email={data.email}")
        
        user = await UserRepository.get_by_email(session=session, data = data)
        
        if not user:
            logger.warning(f"User with email={data.email} not found")
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        logger.info(f"User fetched successfully: {data.email}")
        return user

    async def login(data: UserLogin, session: AsyncSession)  -> str:
        logger.info(f"Logging user with email: {data.email}")
        user = await UserRepository.get_by_email(session = session,
                                        data = data)
        
        
        if not user or not verify_password(data.password, user.password):
            logger.warning(f"Failed login attempt for email: {data.email}")
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })
        return token


    async def refresh_token(refresh_token: str, session: AsyncSession) -> str:
        payload = verify_token(refresh_token)
        data = UserGetById(id = payload["id"])
        user = await UserRepository.get_by_id(session=session, data = data)
        new_access_token = create_access_token({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role
        })
        return new_access_token