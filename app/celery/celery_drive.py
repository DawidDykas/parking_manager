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
from celery import Celery
from app.api.modules.tables import Drive
from app.api.services.drive_services import DriveServices
from io import BytesIO
from PIL import Image
#===================

# temp
from config.setting import celery_settings  


#====================

prediction = DetectModels(detect_car_plates_model_path = "app/models/best.pt")
celery = Celery("worker", broker = celery_settings.URL_BROKER) # temp 




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
                
                drive = asyncio.run(DriveServices.create(data = data))
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
                data = DriveUpdate(drive_in = None,
                                   drive_out = datetime.now(),
                                   plate = None,
                                   payment = None)
                drive = DriveRepository.update_drive(data = data)
    
        