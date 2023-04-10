from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.profile.address_model import Address
from models.product.like_schema import ToggleLikeDto
from repositories import like_repository
from auth.users import current_active_user

router = APIRouter(prefix="/like", tags=["like"])

# Like Registration
@router.post("/product")
async def toggle_product_like(request: ToggleLikeDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    result = await like_repository.toggle_product_like(db, current_user, request)
    return result

# Like Registration
@router.post("/creator")
async def toggle_product_like(request: ToggleLikeDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    result = await like_repository.toggle_creator_like(db, current_user, request)
    return result