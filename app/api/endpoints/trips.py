from fastapi import APIRouter, Depends

from app.api import deps
from app.models import User

router = APIRouter()


@router.post("/trips")
def create_trip(current_user: User = Depends(deps.get_current_user)):
    pass


@router.get("/trips/search")
def search_trips():
    pass


@router.post("/trips/{id}/booking")
def book_trip(trip_id: int):
    pass


@router.get("/bookings")
def get_bookings():
    pass


@router.delete("/bookings/{id}")
def delete_booking(booking_id: int):
    pass
