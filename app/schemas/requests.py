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
    first_name: str | None = None
    last_name: str | None = None
    birthday: date | None = None


class UserCreateRequest(BaseRequest):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birthday: date | None = None


class VehicleCreateRequest(BaseRequest):
    reg_plate: str | None = Field(
        default=None,
        pattern=r"^[АВЕКМНОРСТУХABEKMHOPCTYX]{1}\d{3}[АВЕКМНОРСТУХABEKMHOPCTYX]{2}\d{2,3}$",
        examples=["A001AA77", "A001AA777"],
    )
    make: str
    model: str
    color: str
    registration_date: date
    type: VehicleType
    seats_count: int = Field(ge=1, le=5)


class RideCreateRequest(BaseRequest):
    departure: str
    arrival: str
    departure_at: datetime
    arrival_at: datetime
    seats: int = Field(ge=1, le=4)
    price: int = Field(ge=0)
    with_approval: bool = True
    comment: str | None = None
    vehicle_id: int | None = None
