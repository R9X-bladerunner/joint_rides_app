from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User, Ride, Booking
from app.schemas.requests import RideCreateRequest
from app.schemas.responses import (
    RideResponse,
    RideCreateResponse,
    RideDetailedResponse,
    BookingResponse,
)

router = APIRouter()


@router.post("/rides", response_model=RideCreateResponse)
async def create_ride(
    ride_data: RideCreateRequest = Depends(deps.check_valid_vehicle),
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Create a new ride with driver's role for the current user"""
    ride = Ride(**ride_data.model_dump(exclude_unset=True), driver_id=current_user.id)
    session.add(ride)
    await session.commit()
    return ride


@router.get("/rides/me", response_model=list[RideResponse])
async def read_current_user_rides(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read  the current user's rides"""
    await session.refresh(current_user, ["rides"])
    return current_user.rides


@router.get("/rides/search")
async def search_rides(
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session)
):
    pass


@router.get("/rides/{ride_id}", response_model=RideDetailedResponse)
async def read_ride_info(
    ride: Ride = Depends(deps.get_valid_ride),
    free_seats: int = Depends(deps.get_ride_free_seats),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read ride's information"""
    await session.refresh(ride, ["driver", "vehicle", "bookings"])
    return RideDetailedResponse(**vars(ride), free_seats=free_seats)


@router.get("/rides/me/{ride_id}/bookings", response_model=list[BookingResponse])
async def read_current_user_ride_bookings(
    ride: Ride = Depends(deps.get_current_user_ride),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read incoming ride booking's of the current user"""
    await session.refresh(ride, ["bookings"])
    return ride.bookings


@router.post(
    "rides/me/{ride_id}/bookings/{booking_id}/approve", response_model=BookingResponse
)
async def approve_ride_booking(
    booking: Booking = Depends(deps.get_ride_booking),
    session: AsyncSession = Depends(deps.get_session),
):
    """Approve incoming ride booking's of the current user"""
    booking.approve = True
    await session.commit()
    return booking



# @router.patch("/rides/{ride_id}")
# async def update_ride(
#         ride: Ride = Depends(deps.get_user_ride),
#
#         current_user: User = Depends(deps.get_current_user)
# ):
#     pass
#
#
# @router.delete("/rides/{ride_id}")
# async def delete_ride(
#         ride_id: int,
#         current_user: User = Depends(deps.get_current_user)
# ):
#     pass
