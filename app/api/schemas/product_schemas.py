# models/product_models.py
from pydantic import BaseModel, Field, ConfigDict
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
    payment: bool = Field(
        False, 
        description="Payment",
        example= True
    )

class DriveUpdate():
    plate: None | str = Field(
        None,
        description="Plate of car ",
        example="2026-02-11T17:30:00"
    )

    drive_in: None | datetime = Field(
        None,
        description="Date and time when the car income",
        example="2026-02-11T17:30:00"
    )

    drive_out: None | datetime = Field(
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
    start_date: None | datetime = None
    end_date: None | datetime = None



class DriveResponse(BaseModel):
    id: int = Field(..., description="Unique identifier assigned to the drive", example=42)
    drive_in: datetime = Field(..., description="Timestamp when the drive in registered")
    drive_out: datetime = Field(..., description="Timestamp when the drive out in registered")
    payment: bool = Field(..., description="Payment status")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "plate": "alice_wonder1234",
                "drive_in": "2026-02-11T15:30:00",
                "drive_out": "2026-02-11T15:30:00",
                "payment": "False",
            }
        }
    )

