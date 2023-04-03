from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.option_schema import CreateOptionDto, ResponseCreateOptionDto, UpdateOptionDto
from repositories import option_repository
from auth.users import current_active_user

router = APIRouter(prefix="/option", tags=["option"])

# Create Option
@router.post("/", response_model=ResponseCreateOptionDto)
async def create_option(request: CreateOptionDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    option = await option_repository.create_option(db, current_user, request)
    return option

# Update option
@router.patch("/update", response_model=ResponseCreateOptionDto)
async def create_category(request: UpdateOptionDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    option = await option_repository.update_option(db, current_user, request)
    return option

# Get option
@router.get("/", response_model=ResponseCreateOptionDto)
async def update_address(request: UpdateOptionDto, db: Session = Depends(get_async_session)):
    option = await option_repository.get_option(db, request)
    return option

# # Get option List
@router.get("/option_all", response_model=List[ResponseCreateOptionDto])
async def update_address(db: Session = Depends(get_async_session)):
    options = await option_repository.get_options(db)
    return options