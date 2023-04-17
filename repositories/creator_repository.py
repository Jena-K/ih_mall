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
from models.product.product_image_schema import CreateProductImageDto
from repositories.utils import upload_image_to_s3

async def create_creator_image(
    db: AsyncSession,
    current_user: User,
    request: CreateProductImageDto
):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")
    
    # 처리 불가 이미지 반송
    image_extension = request.image.filename.split(".")[-1]
    if image_extension not in ["png", "jpg"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image extention is not allowed")
    
    image_url = upload_image_to_s3(request)

    return image_url


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
    if request.picture_url:
        new_creator.picture_url = request.picture_url

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
    
    if request.picture_url:
        creator.picture_url = request.picture_url
    
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