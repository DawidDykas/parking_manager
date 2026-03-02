from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

# ------------------------
# Base User (DRY)
# ------------------------
class BaseUser(BaseModel):
    username: str = Field(
        ...,
        description="Login name chosen by the user",
        min_length=3,
        max_length=50,
        example="alice_wonder"
    )
    email: EmailStr = Field(
        ...,
        description="Email address of the user (must be unique)",
        example="alice@example.com"
    )

# ------------------------
# Create / Update / Delete / Get Models
# ------------------------
class UserCreate(BaseUser):
    password: str = Field(
        ...,
        description="Password for user account (at least 6 characters)",
        min_length=6,
        max_length=100,
        example="SuperSecure123!"
    )
    registration_date: None | datetime = Field(
        default_factory=datetime.utcnow,
        description="Date and time when the user registered (auto-set to now)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "alice_wonder",
                "email": "alice@example.com",
                "password": "SuperSecure123!",
                "registration_date": "2026-02-11T15:30:00"
            }
        }
    )

class UserUpdate(BaseModel):
    id: int = Field(..., description="Identifier of the user to modify", example=42)
    username: None | str = Field(None, min_length=3, max_length=50, example="alice_new")
    email: None | EmailStr = Field(None, example="alice.new@example.com")
    password: None | str = Field(None, min_length=6, max_length=100, example="NewPass456!")

# class UserDelete(BaseModel):
#     id: int = Field(..., description="ID of the user to remove", example=42)

class UserGetById(BaseModel):
    id: int = Field(..., description="ID of the user to retrieve", example=42)

class UserGetByEmail(BaseModel):
    email: EmailStr = Field(..., description="Email of the user to retrieve", example="alice@example.com")

# ------------------------
# Response Models
# ------------------------
class UserResponse(BaseUser):
    id: int = Field(..., description="Unique identifier assigned to the user", example=42)
    registration_date: datetime = Field(..., description="Timestamp when the user registered")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "username": "alice_wonder",
                "email": "alice@example.com",
                "registration_date": "2026-02-11T15:30:00"
            }
        }
    )

class UserListResponse(BaseModel):
    total: int = Field(..., description="Total number of users available", example=250)
    skip: int = Field(..., description="Number of users skipped in this result", example=0)
    limit: int = Field(..., description="Maximum number of users returned", example=50)
    users: list[UserResponse] = Field(..., description="Array of user records")

# ------------------------
# Auth Models
# ------------------------
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="Email used to log in", example="alice@example.com")
    password: str = Field(..., description="User password for login", min_length=6, example="SuperSecure123!")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT token granting access")
    token_type: str = Field(default="bearer", description="Type of the token")
    expires_in: int = Field(..., description="Validity period of the token in seconds", example=3600)

class UserLogout(BaseModel):
    token: str = Field(..., description="JWT token to be invalidated on logout")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Short description of the error", example="Authentication failed")
    detail: None | str = Field(None, description="Optional detailed explanation of the error", example="Email or password is incorrect")