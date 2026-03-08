from fastapi import FastAPI, routing, APIRouter, Body, UploadFile, File, Depends
from typing import List, Dict, Any
from ultralytics import data
from app.api.schemas.product_schemas import * 
from log_config.logger_config import logger
from app.api.services.drive_services import DriveServices
from app.api.utils.auth_wrapper import get_current_user
import numpy as np 
from io import BytesIO
from PIL import Image
from app.celery.celery_drive import drive_in_detection, drive_out_detection
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.modules.database import get_db


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

#################################################################


@drive_router.get("/getDriveById/{drive_id}")
async def get_drive_by_id(
    drive_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    drive = await DriveServices.get_drive_by_id(session=session, drive_id=drive_id)
    return drive



@drive_router.delete("/deleteDrive/{drive_id}")
async def delete_drive(
    drive_id: int,
    session: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    status = await DriveServices.delete_drive(session=session, drive_id=drive_id)
    return {"message": "Drive deleted successfully"} if status else {"message": "Drive not found"}

@drive_router.put("/updateDrive/{drive_id}")
async def update_drive(
    drive_id: int, 
    data: DriveUpdate,
    session: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> DriveResponse:
    drive = await DriveServices.update_drive(
        drive_id=drive_id, 
        session=session,
        data=data
    )
    return drive


@drive_router.get("/getDrivesByPlate/{plate}")
async def get_drives_by_plate(
    plate: str, 
    session: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> List[DriveResponse]:
    drives = await DriveServices.get_drives_by_plate(session=session, plate=plate)
    return drives

@drive_router.get("/getDrivesByDateRange/")
async def get_drives_by_date_range(
    start_date: datetime, 
    end_date: datetime, 
    session: AsyncSession = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    drives = await DriveServices.get_drives_by_date_range(
        session=session, 
        start_date=start_date, 
        end_date=end_date
    )
    return drives