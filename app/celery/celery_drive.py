from app.api.repositories.products_repo import * 
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.product_schemas import * 
from log_config.logger_config import logger
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.api.security.jwt_auth import verify_token
from app.api.repositories.products_repo import DriveRepository
import numpy as np 
from app.models.prediction import DetectModels
from datetime import datetime
from app.api.schemas.product_schemas import *
import asyncio
from app.api.modules.tables import Drive
from app.api.services.drive_services import DriveServices
from io import BytesIO
from PIL import Image
from .setting_celery import celery

prediction = DetectModels(detect_car_plates_model_path = "app/models/best.pt")
@celery.task
def drive_in_detection(image: bytes): 
    image = np.array(Image.open(BytesIO(image)))
    plates_list = prediction.detection(image = image)
    if plates_list is not None: 
        unique_plates = list(dict.fromkeys(plates_list))
        for plate in unique_plates:
            logger.info(f"Detected plate: {plate}")
            if asyncio.run(DriveServices.validation_drive_in(plate = plate)): 
                data = DriveIn(drive_in = datetime.now(),
                                plate = plate,
                                payment = False)
                
                drive = asyncio.run(DriveServices.create_celery(data = data))
            else: 
                logger.info("Access denid - verify in drive failed")


@celery.task
def drive_out_detection(image: bytes): 
    image = np.array(Image.open(BytesIO(image)))
    plates_list = prediction.detection(image = image)

    if plates_list is not None: 
        unique_plates = list(dict.fromkeys(plates_list))
        for plate in unique_plates:

            if asyncio.run(DriveServices.validation_drive_out(plate = plate)): 
                data = DriveUpdate(drive_out = datetime.now())

                id_data = asyncio.run(DriveServices.get_drives_by_plate_celery(plate = plate))[-1].id

                drive =asyncio.run(
                        DriveServices.update_drive_celery(
                            data=data,
                            drive_id=id_data
                        )
                       )
        
        