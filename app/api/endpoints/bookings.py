from fastapi import APIRouter, Depends

from app.api import deps
from app.models import User

router = APIRouter()


@router.post("/bookings")
async def book_ride(
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.get("/bookings")
async def read_bookings(
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.delete("/bookings/{booking_id}")
async def cancel_the_booking(
        booking_id,
        current_user: User = Depends(deps.get_current_user)
):
    pass



