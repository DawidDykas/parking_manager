# models/product_models.py
from pydantic import BaseModel, Field
from typing import Optional, Tuple
from datetime import datetime

class BaseDrive(BaseModel):
    plate: str = Field(
        ...,
        description="License plate of the car",
        example="W290190"
    )

class DriveIn(BaseDrive):
    drive_in: datetime = Field(
        ...,
        description="Date and time when the car entered",
        example="2026-02-11T15:30:00"
    )

    plate: BaseDrive = Field( 
        ..., 
        description = "Plate of car",
        example = "W12345"
    )

    payment: bool = Field(
        False, 
        description="Payment",
        example= True
    )

class DriveUpdate(BaseDrive):
    plate: Optional[str] = Field(
        None,
        description="Plate of car ",
        example="2026-02-11T17:30:00"
    )

    drive_in: Optional[datetime] = Field(
        None,
        description="Date and time when the car income",
        example="2026-02-11T17:30:00"
    )

    drive_out: Optional[datetime] = Field(
        None,
        description="Date and time when the car left (can be None if not yet left)",
        example="2026-02-11T17:30:00"
    )

    payment: bool = Field(
        False, 
        description="Payment",
        example= True
    )

class DriveGetByPlate(BaseDrive):
    pass


class DateRange(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

