from datetime import datetime, date

from pydantic import EmailStr, Field

from app.models import VehicleType
from app.schemas.base import CustomModel


class BaseRequest(CustomModel):
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserUpdateInfoRequest(BaseRequest):
    name: str | None = None
    surname: str | None = None
    rating: float | None = None
    birthday: datetime | None = None


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    name: str
    surname: str
    rating: float | None = None
    birthday: datetime | None = None


class VehicleCreateRequest(BaseRequest):
    reg_plate: str | None = Field(
        default=None,
        pattern=r'^[АВЕКМНОРСТУХABEKMHOPCTYX]{1}\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}\d{2,3}$',
        examples=["A001AA77", "A001AA777"]
    )
    make: str
    model: str
    color: str
    registration_date: date
    owner_id: int
    type: VehicleType
    seats_count: int = Field(gt=0, le=5)


class RideCreateRequest(BaseRequest):
    departure: str
    arrival: str
    departure_at: datetime
    arrival_at: datetime
    passenger_seats: int = Field(gt=0, le=4)
    price: int = Field(gt=0)
    comment: str | None = None
    with_approval: bool = True
    driver_id: int
    vehicle_id: int | None = None
