from fastapi import FastAPI, routing, APIRouter, Body, UploadFile, File
from ultralytics import data
from app.api.schemas.product_schemas import * 
from log_config.logger_config import logger
from app.api.services.drive_services import DriveServices
from app.api.utils.auth_wrapper import wrapper_auth_user
import numpy as np 
from io import BytesIO
from PIL import Image
from app.celery.celery_drive import drive_in_detection, drive_out_detection


drive_router = APIRouter(prefix="/drives", tags=["Drive"])

@drive_router.post("/driveIn/")
def drive_in(file: UploadFile = File(...)):
    contents = file.file.read()
    task = drive_in_detection.delay(image = contents)
    return {"task_id": task.id} 

@drive_router.post("/driveOut/")
def drive_out(file: UploadFile = File(...)):
    contents = file.file.read()
    task = drive_out_detection.delay(image = contents)
    return {"task_id": task.id}