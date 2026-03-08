from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


# ------------------------
# User Table
# ------------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="user", nullable=False)
    registration_date: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)



# ------------------------
# Product Table
# ------------------------
class Drive(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    plate: Mapped[str] = mapped_column(nullable=False)
    drive_in: Mapped[datetime] = mapped_column(nullable=False)
    drive_out: Mapped[None | datetime] = mapped_column(nullable=True)
    payment: Mapped[None | bool] = mapped_column(default=False, nullable=False)