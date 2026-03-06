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

    @staticmethod
    @with_session
    async def create(session: AsyncSession, 
                     data: DriveIn) -> None | Drive:
        return await DriveRepository.create(session, data)
    



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

