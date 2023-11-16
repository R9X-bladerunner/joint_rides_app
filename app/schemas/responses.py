from datetime import datetime, date

from pydantic import EmailStr

from app.models import VehicleType
from app.schemas.base import CustomModel


class BaseResponse(CustomModel):
    pass


class AccessTokenResponse(BaseResponse):
    token_type: str
    access_token: str
    expires_at: int
    issued_at: int
    refresh_token: str
    refresh_token_expires_at: int
    refresh_token_issued_at: int


class VehicleResponse(BaseResponse):
    id: int
    reg_plate: str | None
    make: str
    model: str
    color: str
    registration_date: date
    owner_id: int
    type: VehicleType
    seats_count: int


class UserResponse(BaseResponse):
    id: int
    name: str
    surname: str
    rating: float | None = None


class UserPublicResponse(UserResponse):
    pass


class UserPrivateResponse(UserResponse):
    email: EmailStr
    birthday: datetime | None = None
    vehicles: list[VehicleResponse]


class RideResponse(BaseResponse):
    id: int
    created_at: datetime
    departure: int
    arrival: str
    departure_at: datetime
    arrival_at: datetime
    passenger_seats: int
    price: int
    comment: str | None = None
    with_approval: bool
    driver: UserPublicResponse
    vehicle: VehicleResponse










