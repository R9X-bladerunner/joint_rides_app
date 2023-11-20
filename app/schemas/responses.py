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
    type: VehicleType
    seats: int


class UserResponse(BaseResponse):
    id: int
    first_name: str
    last_name: str
    rating: float | None = None


class UserPublicResponse(UserResponse):
    pass


class UserPrivateResponse(UserResponse):
    email: EmailStr
    birthday: date | None = None


class RideResponse(BaseResponse):
    id: int
    created_at: datetime
    departure: str
    arrival: str
    departure_at: datetime
    arrival_at: datetime
    seats: int
    price: int
    with_approval: bool
    comment: str | None = None


class RideCreateResponse(RideResponse):
    pass


class RideDetailedResponse(RideResponse):
    driver: UserPublicResponse
    vehicle: VehicleResponse | None = None
    free_seats: int


class BookingResponse(BaseResponse):
    id: int
    ride_id: int
    filled_at: datetime
    approve: bool
    approved_at: datetime | None = None
    seats: int


class BookingCreateResponse(BookingResponse):
    pass


class BookingDetailedResponse(BookingResponse):
    ride: RideResponse
