from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.profile.address_schema import AddressDisplayDto, AddressListDisplayDto, CreateAddressDto, RequestMyAddressDto
from repositories import address_repository
from auth.users import current_active_user

router = APIRouter(prefix="/address", tags=["address"])

# Address Registration
@router.post("/", response_model=AddressDisplayDto)
async def create_address(request: CreateAddressDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    address = await address_repository.create_address(db, current_user, request)
    return address

# Address Update
@router.patch("/update", response_model=AddressDisplayDto)
async def update_address(request: CreateAddressDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    address = await address_repository.update_address(db, current_user, request)
    return address

# 내 주소지 조회(1개)
@router.get("/", response_model=AddressDisplayDto)
async def update_address(request: RequestMyAddressDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    address = await address_repository.my_address(db, current_user, request)
    return address

# User Query (One)
# @router.get("/{id}", response_model=AddressDisplayDto)
# def get_address(
#     id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
# ):
#     return address_repository.get_address(db, id, current_user)
