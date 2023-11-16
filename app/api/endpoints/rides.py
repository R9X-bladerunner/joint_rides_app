from fastapi import APIRouter, Depends

from app.api import deps
from app.models import User

router = APIRouter()


@router.post("/rides")
async def create_ride(current_user: User = Depends(deps.get_current_user)):
    pass


@router.delete("/rides/{ride_id}")
async def delete_ride(
        ride_id: int,
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.patch("/rides/{ride_id}")
async def update_ride(
        ride_id: int,
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.post("rides/{ride_id}/bookings")
async def read_ride_bookings(
        ride_id: int,
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.post("rides/{ride_id}/bookings/{booking_id}/approve")
async def approve_booking(
        ride_id: int,
        booking_id: int,
        current_user: User = Depends(deps.get_current_user)
):
    pass

