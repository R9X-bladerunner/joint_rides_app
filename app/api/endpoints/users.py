from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core.security import get_password_hash
from app.models import User
from app.schemas.requests import (
    UserCreateRequest,
    UserUpdatePasswordRequest,
    UserUpdateInfoRequest,
)
from app.schemas.responses import UserPrivateResponse, UserPublicResponse

router = APIRouter()


@router.get("/me", response_model=UserPrivateResponse)
async def read_current_user(
    current_user: User = Depends(deps.get_current_user),
):
    """Get current user"""
    return current_user


@router.patch("/me", response_model=UserPrivateResponse)
async def update_current_user_info(
    user_info: UserUpdateInfoRequest,
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Update current user info"""
    for attr, value in user_info.model_dump(exclude_unset=True).items():
        setattr(current_user, attr, value)
    await session.commit()
    return current_user


@router.delete("/me", status_code=204)
async def delete_current_user(
    current_user: User = Depends(deps.get_current_user),
    session: AsyncSession = Depends(deps.get_session),
):
    """Delete current user"""
    await session.execute(delete(User).where(User.id == current_user.id))
    await session.commit()


@router.post("/reset-password", response_model=UserPrivateResponse)
async def reset_current_user_password(
    user_update_password: UserUpdatePasswordRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user),
):
    """Update current user password"""
    current_user.hashed_password = get_password_hash(user_update_password.password)
    session.add(current_user)
    await session.commit()
    return current_user


@router.post("/register", response_model=UserPrivateResponse)
async def register_new_user(
    new_user: UserCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
):
    """Create new user"""
    result = await session.execute(select(User).where(User.email == new_user.email))
    if result.scalars().first() is not None:
        raise HTTPException(status_code=400, detail="Cannot use this email address")
    user = User(
        **new_user.model_dump(exclude_unset=True, exclude={"password"}),
        hashed_password=get_password_hash(new_user.password)
    )
    session.add(user)
    await session.commit()
    return user


@router.get("/{user_id}", response_model=UserPublicResponse)
async def read_user_info(user: UserPublicResponse = Depends(deps.get_user_info)):
    """Read related user's information (for user having active ride or user having booking of current_user ride"""
    return user
