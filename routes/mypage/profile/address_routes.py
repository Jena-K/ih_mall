from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.profile.address_model import Address
from models.profile.address_schema import AddressDisplayDto, CreateAddressDto, RequestMyAddressDto
from models.profile.base_schema import AddressBaseDto
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
@router.get("/my_address", response_model=AddressDisplayDto)
async def update_address(request: RequestMyAddressDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    address = await address_repository.my_address(db, current_user, request)
    print(type(address))
    return address

# 내 주소지 조회(리스트)
@router.get("/my_address_list", response_model=List[AddressDisplayDto])
async def update_address(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    addresses = await address_repository.my_address_list(db, current_user)
    
    return addresses