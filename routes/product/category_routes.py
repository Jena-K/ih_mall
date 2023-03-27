from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.category_schema import CreateCategoryDto, GetCategoryDto, ResponseCreateCategoryDto, UpdateCategoryDto
from repositories import category_repository
from auth.users import current_active_user

router = APIRouter(prefix="/category", tags=["category"])

# Category Registration
@router.post("/", response_model=ResponseCreateCategoryDto)
async def create_category(request: CreateCategoryDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    category = await category_repository.create_category(db, current_user, request)
    return category

# Category Update
@router.patch("/update", response_model=ResponseCreateCategoryDto)
async def create_category(request: UpdateCategoryDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    category = await category_repository.update_category(db, current_user, request)
    return category

# Get Category
@router.get("/", response_model=ResponseCreateCategoryDto)
async def update_address(request: GetCategoryDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    category = await category_repository.get_category(db, current_user, request)
    return category

# Get Category List
@router.get("/category_all", response_model=List[ResponseCreateCategoryDto])
async def update_address(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    categories = await category_repository.get_category_list(db, current_user)
    
    return categories