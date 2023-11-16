from fastapi import APIRouter, Depends

from app.api import deps
from app.models import User

router = APIRouter()


@router.post("/vehicles")
async def create_vehicle(
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.get("/vehicles")
async def read_vehicles(
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.patch("/vehicles/{vehicle_id}")
async def update_vehicle(
        vehicle_id: int,
        current_user: User = Depends(deps.get_current_user)
):
    pass


@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(
        vehicle_id: int,
        current_user: User = Depends(deps.get_current_user)
):
    pass
