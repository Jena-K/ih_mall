
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database import User, get_async_session
from models.product.product_image_schema import CreateProductImageDto, ResponseCreateProductImageDto
from models.profile.profile_schema import (
    RegisterProfileDto,
    ResponseRegisterProfileDto,
    UpdateProfileDto,
    ProfileDisplayDto,
)
from repositories import profile_repository
from auth.users import current_active_user

router = APIRouter(prefix="/profile", tags=["profile"])

# Create Profile Image
@router.post("/image", response_model=str)
async def create_profile_image(
    image: CreateProductImageDto = Depends(),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    profile_image = await profile_repository.create_profile_image(db, current_user, image)
    return profile_image


# User Registration
@router.post("/", response_model=ResponseRegisterProfileDto)
async def register_new_profile(request: RegisterProfileDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    profile = await profile_repository.create_profile(db, current_user, request)
    return profile


# User Update
@router.patch("/", response_model=ResponseRegisterProfileDto)
async def update_profile(request: UpdateProfileDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    profile = await profile_repository.update_profile(db, current_user, request)
    return profile

# 내 프로필 조회
@router.get("/", response_model=ProfileDisplayDto)
async def query_profile(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    profile = await profile_repository.my_profile(db, current_user)
    return profile