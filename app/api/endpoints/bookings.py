from datetime import datetime, timezone

from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User, Ride, Booking
from app.schemas.responses import BookingCreateResponse, BookingDetailedResponse

router = APIRouter()


@router.post("/bookings", response_model=BookingCreateResponse)
async def book_ride(
    requested_seats: int,
    ride: Ride = Depends(deps.get_valid_ride_for_booking),
    approved_seats: int = Depends(deps.get_ride_approved_seats),
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Book the ride"""
    free_seats = ride.seats - approved_seats

    if requested_seats > free_seats:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough free seats: requested_seats: {requested_seats} free seats: {free_seats}",
        )

    if ride.with_approval:
        booking = Booking(
            passenger_id=current_user.id, approved=False, seats=requested_seats
        )
    else:
        booking = Booking(
            passenger_id=current_user.id,
            approved=True,
            approved_at=datetime.now(tz=timezone.utc),
            seats=requested_seats,
        )
    await session.refresh(ride, ["bookings"])
    ride.bookings.append(booking)
    await session.commit()
    return booking


@router.get("/bookings", response_model=list[BookingDetailedResponse])
async def read_current_user_bookings(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Read the current user's bookings"""
    await session.refresh(current_user, ["bookings"])
    return current_user.bookings


@router.delete("/bookings/{booking_id}", status_code=204)
async def cancel_the_booking(
    booking: Booking = Depends(deps.check_booking_exist),
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Cancel the current user's active booking"""
    await session.delete(booking)
    await session.commit()
