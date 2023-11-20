from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User, Vehicle
from app.schemas.requests import VehicleCreateRequest
from app.schemas.responses import VehicleResponse

router = APIRouter()


@router.post("/vehicles", response_model=VehicleResponse)
async def create_vehicle(
    new_vehicle: VehicleCreateRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    vehicle = Vehicle(**new_vehicle.model_dump(), owner_id=current_user.id)
    session.add(vehicle)
    await session.commit()
    return vehicle


#
# @router.get("/vehicles")
# async def read_vehicles(
#         current_user: User = Depends(deps.get_current_user)
# ):
#     pass
#
#
# @router.patch("/vehicles/{vehicle_id}")
# async def update_vehicle(
#         vehicle_id: int,
#         current_user: User = Depends(deps.get_current_user)
# ):
#     pass
#
#
# @router.delete("/vehicles/{vehicle_id}")
# async def delete_vehicle(
#         vehicle_id: int,
#         current_user: User = Depends(deps.get_current_user)
# ):
#     pass
