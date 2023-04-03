from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.profile.profile_model import Profile
from models.profile.profile_schema import (
    RegisterProfileDto,
    UpdateProfileDto,
)
from sqlalchemy.orm import selectinload
async def create_profile(db: AsyncSession, current_user: User, request: Optional[RegisterProfileDto] = None):

    new_profile = Profile(
        email=current_user.email,
        user_id=current_user.id,
        provider=current_user.oauth_accounts[0].oauth_name,
        phone=request.phone,
        name=request.name
    )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return new_profile


async def update_profile(db: AsyncSession, current_user: User, request: Optional[UpdateProfileDto] = None):

    profile = await db.execute(
        select(Profile)
        .options(selectinload(Profile.user))
        .where(Profile.user_id == current_user.id)
    )
    profile = profile.scalar_one_or_none()

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    for key, value in request:
        if value is not None:
            setattr(profile, key, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile

async def my_profile(db: AsyncSession, current_user: User):
    
    profile = await db.execute(
        select(Profile)
        .options(selectinload(Profile.user))
        .where(Profile.user_id == current_user.id)
    )
    
    profile = profile.scalar_one_or_none()

    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile