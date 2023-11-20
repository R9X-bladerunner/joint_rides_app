import datetime
import time
from collections.abc import AsyncGenerator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select, and_, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core import config, security
from app.core.session import async_session
from app.models import User, Vehicle, Ride, Booking
from app.schemas.requests import RideCreateRequest
from app.schemas.responses import UserPublicResponse

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="auth/access-token")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[security.JWT_ALGORITHM]
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )
    # JWT guarantees payload will be unchanged (and thus valid), no errors here
    token_data = security.JWTTokenPayload(**payload)

    if token_data.refresh:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, cannot use refresh token",
        )
    now = int(time.time())
    if now < token_data.issued_at or now > token_data.expires_at:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials, token expired or not yet valid",
        )

    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


async def check_valid_vehicle(
    ride_create: RideCreateRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> RideCreateRequest:
    if ride_create.vehicle_id is not None:
        query = select(Vehicle).where(
            and_(
                Vehicle.id == ride_create.vehicle_id,
                Vehicle.owner_id == current_user.id,
            )
        )
        vehicle = await session.scalar(query)
        if vehicle is None:
            raise HTTPException(
                status_code=400,
                detail=f"User vehicle with id <{ride_create.vehicle_id}> not found",
            )

    return ride_create


async def get_valid_ride(ride_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Ride).where(Ride.id == ride_id)
    ride = await session.scalar(query)
    if ride is None:
        raise HTTPException(
            status_code=400, detail=f"Ride with id <{ride_id}> not found"
        )
    return ride


async def get_valid_ride_for_booking(
    ride: Ride = Depends(get_valid_ride),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if ride.driver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot book own ride")

    if datetime.datetime.now(tz=datetime.timezone.utc) > ride.departure_at:
        raise HTTPException(
            status_code=400, detail=f"Ride with id <{ride.id}> has expired"
        )

    query = select(Booking).where(
        and_(Booking.passenger_id == current_user.id, Booking.ride_id == ride.id)
    )
    existing_user_booking = await session.scalar(query)
    if existing_user_booking is not None:
        raise HTTPException(
            status_code=400,
            detail=f"booking from the current user already exists: booking_id: {existing_user_booking.id}",
        )
    return ride


async def get_current_user_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    query = select(Ride).where(Ride.id == ride_id, Ride.driver_id == current_user.id)
    ride = await session.scalar(query)
    if ride is None:
        raise HTTPException(
            status_code=400, detail=f"Not found current user ride with id: {ride_id}"
        )

    return ride


async def get_ride_approved_seats(
    ride: Ride = Depends(get_valid_ride), session: AsyncSession = Depends(get_session)
):
    query = select(func.sum(Booking.seats)).where(
        and_(Booking.ride_id == ride.id, Booking.approve == True)
    )
    approved_seats = await session.scalar(query)

    return 0 if approved_seats is None else approved_seats


async def get_ride_free_seats(
    ride: Ride = Depends(get_valid_ride),
    approved_seats: int = Depends(get_ride_approved_seats),
):
    return ride.seats - approved_seats


async def check_booking_exist(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    query = select(Booking).where(
        and_(Booking.id == booking_id, Booking.passenger_id == current_user.id)
    )
    booking = await session.scalar(query)
    if booking is None:
        raise HTTPException(
            status_code=400, detail=f"User booking with id: {booking_id} not found"
        )
    return booking


async def get_ride_booking(
    booking_id: int,
    ride: Ride = Depends(get_current_user_ride),
    session: AsyncSession = Depends(get_session),
) -> Booking:
    query = select(Booking).where(Booking.ride_id == ride.id)
    booking = await session.scalar(query)
    if Booking is None:
        raise HTTPException(
            status_code=400, detail=f"Ride booking with id: {booking_id} not found"
        )

    return booking


async def get_user_info(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    query = (
        select(User)
        .options(
            joinedload(User.rides, Ride.bookings)
        )
        .where(
            and_(
                User.id == user_id,
                Ride.departure_at > datetime.datetime.now(tz=datetime.timezone.utc)
            )
        )
    )
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=400, detail=f"Not found related user with id {user_id}"
        )

    return UserPublicResponse(**vars(user))
