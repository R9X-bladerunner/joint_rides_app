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

from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(128))
    first_name: Mapped[str]
    last_name: Mapped[str]
    birthday: Mapped[Optional[date]]
    rating: Mapped[Optional[float]]
    rides: Mapped[list["Ride"]] = relationship(back_populates="driver")
    vehicles: Mapped[list["Vehicle"]] = relationship()
    bookings: Mapped[list["Booking"]] = relationship()


class VehicleType(Enum):
    SEDAN = "sedan"
    COUPE = "coupe"
    HATCHBACK = "hatchback"
    SUV = "suv"
    VAN = "van"


class Vehicle(Base):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    reg_plate: Mapped[Optional[str]]
    make: Mapped[str]
    model: Mapped[str]
    color: Mapped[str]
    registration_date: Mapped[date]
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    type: Mapped[VehicleType]
    seats: Mapped[int]


class Booking(Base):
    __tablename__ = "booking"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ride_id: Mapped[int] = mapped_column(ForeignKey("ride.id", ondelete="CASCADE"))
    passenger_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    filled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), insert_default=func.now()
    )
    approved: Mapped[bool]
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    seats: Mapped[int]
    ride: Mapped["Ride"] = relationship(back_populates="bookings", lazy="joined")
    passenger: Mapped['User'] = relationship(lazy='joined')


class Ride(Base):
    __tablename__ = "ride"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    departure: Mapped[str] = mapped_column(index=True)
    arrival: Mapped[str] = mapped_column(index=True)
    departure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    arrival_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    seats: Mapped[int]
    price: Mapped[int]
    with_approval: Mapped[bool]
    comment: Mapped[Optional[str]]
    driver_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    driver: Mapped["User"] = relationship(back_populates="rides")
    vehicle_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("vehicle.id", ondelete="SET NULL")
    )
    vehicle: Mapped["Vehicle"] = relationship()
    bookings: Mapped[list["Booking"]] = relationship(back_populates="ride")


class Messages(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_onupdate=func.now()
    )
    ride_id: Mapped[str] = mapped_column(ForeignKey("ride.id", ondelete="CASCADE"))
    message_text: Mapped[str] = mapped_column(String(1000))
