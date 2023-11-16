"""
SQL Alchemy models declaration.
https://docs.sqlalchemy.org/en/14/orm/declarative_styles.html#example-two-dataclasses-with-declarative-table
Dataclass style for powerful autocompletion support.

https://alembic.sqlalchemy.org/en/latest/tutorial.html
Note, it is used by alembic migrations logic, see `alembic/env.py`

Alembic shortcuts:
# create migration
alembic revision --autogenerate -m "migration_name"

# apply all migrations
alembic upgrade head
"""
from datetime import datetime, date
from enum import Enum
from typing import Optional

from sqlalchemy import String, ForeignKey, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(128))
    name: Mapped[str]
    surname: Mapped[str]
    birthday: Mapped[Optional[datetime]]
    rating: Mapped[Optional[float]]




class VehicleType(Enum):
    SEDAN = 'sedan'
    COUPE = 'coupe'
    HATCHBACK = 'hatchback'
    SUV = 'suv'
    VAN = 'van'


class Vehicle(Base):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    reg_plate: Mapped[Optional[str]]
    make: Mapped[str]
    model: Mapped[str]
    color: Mapped[str]
    registration_date: Mapped[date]
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    type: Mapped[VehicleType]
    seats_count: Mapped[int]


class Ride(Base):
    __tablename__ = "ride"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    departure: Mapped[str] = mapped_column(index=True)
    arrival: Mapped[str] = mapped_column(index=True)
    departure_at: Mapped[datetime]
    arrival_at: Mapped[datetime]
    passenger_seats: Mapped[int]
    price: Mapped[int]
    comment: Mapped[Optional[str]]
    with_approval: Mapped[bool]
    driver_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete='CASCADE'))
    vehicle_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vehicle.id", ondelete='SET NULL'))


class Booking(Base):
    __tablename__ = "booking"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ride_id: Mapped[str] = mapped_column(ForeignKey("ride.id", ondelete="CASCADE"))
    passenger_id: Mapped[str] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    filled_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    approve: Mapped[bool]
    approved_at: Mapped[datetime]


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    ride_id: Mapped[str] = mapped_column(ForeignKey("ride.id", ondelete="CASCADE"))
    message_text: Mapped[str] = mapped_column(String(1000))
