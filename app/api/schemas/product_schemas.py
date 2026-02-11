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

class DriveOut(BaseDrive):
    drive_out: Optional[datetime] = Field(
        None,
        description="Date and time when the car left (can be None if not yet left)",
        example="2026-02-11T17:30:00"
    )

class ProductGetByPlate(BaseDrive):
    pass  # wszystko jest w BaseDrive, DRY


class DateRange(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProductGetByDate(BaseModel):
    date: DateRange = Field(
        ...,
        description="Date range to filter cars (start_date, end_date). Use None for open-ended range.",
        example=("2026-02-11T00:00:00", None)
    )