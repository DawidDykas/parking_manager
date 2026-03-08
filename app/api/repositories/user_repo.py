from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.api.modules.tables import User
from app.api.schemas.user_schemas import *


class UserRepository:
    # ------------------------
    # CREATE
    # ------------------------
    async def create(
        session: AsyncSession,
        data: UserCreate
    ) -> User:

        user = User(
            username=data.username,
            email=data.email,
            password=data.password,
            role=data.role,
            registration_date=data.registration_date
        )
        session.add(user)
        await session.flush() # Do walidacji id bez tego wywali

        return user

    # ------------------------
    # GET
    # ------------------------
    async def get_by_id(
        session: AsyncSession,
        data: UserGetById
    ) -> None | User:

        result = await session.execute(
            select(User).where(User.id == data.id) 
        )
        return result.scalar_one_or_none()


    async def get_by_email(
        session: AsyncSession,
        data: UserGetByEmail
    ) -> None | User:

        result = await session.execute(
            select(User).where(User.email == data.email)
        )
        return result.scalar_one_or_none()

    # ------------------------
    # UPDATE 
    # ------------------------
    async def update(
        session: AsyncSession,
        data: UserUpdate
    ) -> None | User:

        user = await UserRepository.get_by_id(session, data)

        if not user:
            return None

        update_data = data.model_dump(exclude_unset=True)
        update_data.pop("id", None)

        for field, value in update_data.items():
            setattr(user, field, value)

        return user
