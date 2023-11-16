from fastapi import APIRouter

from app.api.endpoints import auth, users, rides, bookings,  vehicles, messages

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(rides.router, tags=["rides"])
api_router.include_router(bookings.router, tags=["bookings"])
api_router.include_router(vehicles.router, tags=["vehicles"])
api_router.include_router(messages.router, tags=["messages"])









