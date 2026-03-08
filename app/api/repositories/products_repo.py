from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.api.modules.tables import Drive
from app.api.schemas.product_schemas import DriveIn, DriveUpdate, DateRange, DriveResponse, DriveGetByPlate



class DriveRepository:
    async def create(session: AsyncSession, 
                     data: DriveIn) -> None | Drive:
        drive = Drive(
            plate=data.plate,
            drive_in=data.drive_in
        )
        session.add(drive)
        await session.flush()
        return drive
    

    async def get_by_plate(
        session: AsyncSession,
        data: DriveGetByPlate
    ) -> List[Drive]:

        result = await session.execute(
            select(Drive)
            .where(Drive.plate == data.plate)
            .order_by(Drive.drive_in.asc())
        )

        return result.scalars().all()


    async def get_by_date_range(
        session: AsyncSession,
        date_range: DateRange
    ) -> None | Drive:
    
        stmt = select(Drive)
        if date_range.start_date:
            stmt = stmt.where(Drive.drive_in >= date_range.start_date)
        if date_range.end_date:
            stmt = stmt.where(Drive.drive_in <= date_range.end_date)
        stmt = stmt.order_by(Drive.drive_in.desc())
        result = await session.execute(stmt)
        return result.scalars().all()



    async def update_drive(
        session: AsyncSession,
        drive_id: int,
        data: DriveUpdate
    ) -> Drive | None:


        result = await session.execute(
            select(Drive).where(Drive.id == drive_id)
        )
        drive = result.scalar_one_or_none()


        if not drive:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(drive, field, value)

        await session.flush()
        return drive

    


    async def get_by_id(session: AsyncSession, 
                        drive_id: int) -> Drive | None:
        result = await session.execute(
            select(Drive).where(Drive.id == drive_id)
        )
        return result.scalars().first()
    
    async def delete_drive(session: AsyncSession,
                           drive_id: int) -> None:
        drive = await DriveRepository.get_by_id(session, drive_id)
        if drive:
            await session.delete(drive)
            await session.flush()
            return True
        return False