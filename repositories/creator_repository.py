from profile import Profile
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator
from sqlalchemy.orm import selectinload
from models.creator.creator_schema import CreateCreatorDto, GetCreatorDto, UpdateCreatorDto


async def create_creator(db: AsyncSession, current_user: User, request: Optional[CreateCreatorDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )
    existing_creator = creator.scalar_one_or_none()

    if existing_creator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator already exist")
    
    new_creator = Creator(
        user_id=current_user.id,
        nickname=request.nickname,
        phone=request.phone,
        businessNumber=request.businessNumber,
        businessName=request.businessName,
        representative=request.representative,
        representativeType=request.representativeType,
        businessRegistrationCertification=request.businessRegistrationCertification,
        address=request.address,
        sns=request.sns,
        is_certified=False
    )
    db.add(new_creator)
    await db.commit()
    await db.refresh(new_creator)
    
    return new_creator


# 작가 업데이트
async def update_creator(db: AsyncSession, current_user: User, request: Optional[UpdateCreatorDto] = None):
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )
    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")

    
    for key, value in request:
        if value is not None:
            setattr(creator, key, value)
    
    await db.commit()
    await db.refresh(creator)
    
    return creator

# 작가 정보조회
async def creator_info(db: AsyncSession, current_user: User):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )
    
    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")
    return creator

# Get Creator (Single)
async def get_creator(db: AsyncSession, request: Optional[GetCreatorDto]):

    creator = await db.execute(
        select(Creator)
        .where(Creator.id == request.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")
    return creator


# Get Product (List)
async def get_creators(db: AsyncSession):
    
    creators = await db.execute(
        select(Creator)
    )
    
    creators = creators.scalars()
    
    if creators is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator list not found")
    
    else:
        creators = [creator for creator in creators]
    
    return creators