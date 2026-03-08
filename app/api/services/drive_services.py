from app.api.modules.tables import Drive
from app.api.repositories.products_repo import DriveRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.product_schemas import * 
from log_config.logger_config import logger
from app.api.security.jwt_auth import verify_token
from app.api.repositories.products_repo import DriveRepository
import numpy as np 
from app.models.prediction import DetectModels
from datetime import datetime
from log_config.logger_config import logger
from app.api.services.utils import with_session

prediction = DetectModels(detect_car_plates_model_path = "app/models/best.pt")

class DriveServices: 
    @with_session
    async def update_drive_celery(session: AsyncSession, 
                           drive_id: int, 
                           data: DriveUpdate) -> None | Drive:
        
        logger.info(f"Updating drive with id: {drive_id}")

        drive = await DriveRepository.update_drive(drive_id = drive_id,
                                                   session = session,
                                                   data=data)
        if not drive:
            logger.warning(f"Drive with id: {drive_id} not found")
            return None
        else:
            logger.info(f"Drive with id: {drive_id} updated successfully")
            return drive

    @with_session    
    async def create_celery(session: AsyncSession, 
                     data: DriveIn) -> None | Drive:
        return await DriveRepository.create(session, data)
    

    @with_session    
    async def get_drives_by_plate_celery(session: AsyncSession, 
                                  plate: str) -> list[Drive]:

        logger.info(f"Getting drives with plate: {plate}")
        return await DriveRepository.get_by_plate(session=session, 
                                                 data=DriveGetByPlate(plate=plate))
    

    @staticmethod
    @with_session
    async def validation_drive_in(session: AsyncSession, 
                                  plate: str) -> bool:

        drives = await DriveRepository.get_by_plate(
            session=session,
            data=DriveGetByPlate(plate=plate)
        )

        if not drives:
            return True

        last_drive = drives[-1]

        # DRIVE OUT
        if not last_drive.drive_out:
            logger.warning(f"Car with plate {plate} has not driven out")
            return False

        return True 
    

    @staticmethod
    @with_session
    async def validation_drive_out(session: AsyncSession, 
                                   plate: str) -> bool: 

        drives = await DriveRepository.get_by_plate(
            session=session,
            data=DriveGetByPlate(plate=plate)
        )

        if not drives:
            logger.warning(f"No drive history for plate {plate}")
            return False 
        
        last_drive = drives[-1]

        if last_drive.drive_out:
            logger.warning(f"Car with plate {plate} has already driven out")
            return False

        # PAYMENT
        if not last_drive.payment:
            logger.warning(f"Car with plate {plate} has not paid for last parking")
            return False
        
        logger.info("Authorization drive out complete access permision") 
        return True 


# ################################################

    async def create(session: AsyncSession, 
                     data: DriveIn) -> None | Drive:
        return await DriveRepository.create(session, data)


    async def get_drive_by_id(session: AsyncSession, 
                              drive_id: int) -> Drive | None:
        logger.info(f"Getting drive with id: {drive_id}")
        return await DriveRepository.get_by_id(session=session, drive_id = drive_id)
    
    async def delete_drive(session: AsyncSession, 
                           drive_id: int) -> bool:
        logger.info(f"Deleting drive with id: {drive_id}")
        status = await DriveRepository.delete_drive(session=session, 
                                                    drive_id = drive_id)
        if not status:
            logger.warning(f"Drive with id: {drive_id} not found")
            return False
        else:
            logger.info(f"Drive with id: {drive_id} deleted successfully")
            return True

    async def get_drives_by_date_range(session: AsyncSession,
                                      start_date: datetime, 
                                      end_date: datetime) -> list[Drive]:

        logger.info(f"Getting drives with date range: {start_date} - {end_date}")
        return await DriveRepository.get_by_date_range(session=session, 
                                                        date_range=DateRange(start_date=start_date, end_date=end_date))
        
    async def get_drives_by_plate(session: AsyncSession, 
                                  plate: str) -> list[Drive]:

        logger.info(f"Getting drives with plate: {plate}")
        return await DriveRepository.get_by_plate(session=session, 
                                                 data=DriveGetByPlate(plate=plate))
    
    async def get_drives_by_date_range(session: AsyncSession,
                                      start_date: datetime, 
                                      end_date: datetime) -> list[Drive]:

        logger.info(f"Getting drives with date range: {start_date} - {end_date}")
        return await DriveRepository.get_by_date_range(session=session, 
                                                        date_range=DateRange(start_date=start_date, end_date=end_date))
    


    async def update_drive(session: AsyncSession, 
                           drive_id: int , 
                           data: DriveUpdate) -> None | Drive:
        
        logger.info(f"Updating drive with id: {drive_id}")

        drive = await DriveRepository.update_drive(drive_id = drive_id,
                                                   session = session,
                                                   data=data)
        if not drive:
            logger.warning(f"Drive with id: {drive_id} not found")
            return None
        else:
            logger.info(f"Drive with id: {drive_id} updated successfully")
            return drive
