
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.profile.cart_schema import CreateCartDto, DeleteCartDto, UpdateCartDTO, ResponseCartListDTO
from repositories import cart_repository
from auth.users import current_active_user

router = APIRouter(prefix="/cart", tags=["cart"])


# Add cart item
@router.post("/add", response_model=dict)
async def add_cart_item(request: CreateCartDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    cart = await cart_repository.add_cart(request, db, current_user)
    return cart


# Delete cart item
@router.post("/delete", response_model=dict)
async def del_cart_item(request: DeleteCartDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    cart = await cart_repository.delete_cart(request, db, current_user)
    return cart


@router.post("/update", response_model=dict)
async def del_cart_item(request: UpdateCartDTO, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    cart = await cart_repository.update_cart(request, db, current_user)
    return cart


@router.get("/get", response_model=list)
async def get_cart_item(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    cart = await cart_repository.get_cart(db, current_user)
    return cart
