from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.api.modules.tables import Drive
from app.api.schemas.product_schemas import DriveIn, DriveUpdate, DateRange



class DriveRepository:
    async def create(self, session: AsyncSession, 
                     data: DriveIn) -> Drive:
        drive = Drive(
            plate=data.plate,
            drive_in=data.drive_in
        )
        session.add(drive)
        await session.flush()
        return drive
    

    async def get_by_plate(self, session: AsyncSession, 
                           plate: str) -> Optional[Drive]:
        
        result = await session.execute(
            select(Drive).where(Drive.plate == plate)
        )
        return result.scalar_one_or_none()



    async def get_by_date_range(
        self,
        session: AsyncSession,
        date_range: DateRange
    ) -> List[Drive]:
    
        stmt = select(Drive)
        if date_range.start_date:
            stmt = stmt.where(Drive.drive_in >= date_range.start_date)
        if date_range.end_date:
            stmt = stmt.where(Drive.drive_in <= date_range.end_date)
        stmt = stmt.order_by(Drive.drive_in.desc())
        result = await session.execute(stmt)
        return result.scalars().all()



    async def update_drive(self, session: AsyncSession, 
                           data) -> Optional[Drive]:
        
        drive = await self.get_by_plate(session, data.plate)
        if not drive:
            return None

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(drive, field, value)

        await session.flush()
        return drive

    