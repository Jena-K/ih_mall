from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.creator.creator_schema import CreateCreatorDto, CreateResponseCreatorDto, GetCreatorDto, UpdateCreatorDto
from models.product.product_image_schema import CreateProductImageDto, ResponseCreateProductImageDto
from sqlalchemy.ext.asyncio import AsyncSession
from repositories import creator_repository, like_repository
from auth.users import current_active_user

router = APIRouter(prefix="/creator", tags=["creator"])

# Create Profile Image
@router.post("/image", response_model=str)
async def create_profile_image(
    image: CreateProductImageDto = Depends(),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    profile_image = await creator_repository.create_creator_image(db, current_user, image)
    return profile_image

# Creator Registration
@router.post("/", response_model=CreateResponseCreatorDto)
async def create_creator(request: CreateCreatorDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    creator = await creator_repository.create_creator(db, current_user, request)
    return creator

# Creator Update
@router.patch("/", response_model=CreateResponseCreatorDto)
async def update_creator(request: UpdateCreatorDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    creator = await creator_repository.update_creator(db, current_user, request)
    return creator

# 작가정보 조회
@router.get("/my_info", response_model=CreateResponseCreatorDto)
async def my_info(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    creator = await creator_repository.creator_info(db, current_user)
    return creator

# 작가정보 조회 (Single)
@router.get("/", response_model=CreateResponseCreatorDto)
async def get_creator(request: GetCreatorDto, db: Session = Depends(get_async_session)):
    creator = await creator_repository.get_creator(db, request)
    return creator

# 작가정보 조회 (List)
@router.get("/creator_all", response_model=List[CreateResponseCreatorDto])
async def get_creators(db: Session = Depends(get_async_session)):
    creators = await creator_repository.get_creators(db)
    return creators