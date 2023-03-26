from profile import Profile
from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.profile.address_model import Address
from models.profile.address_schema import CreateAddressDto, AddressDisplayDto, RequestMyAddressDto


from sqlalchemy.orm import selectinload

async def create_address(db: AsyncSession, current_user: User, request: Optional[CreateAddressDto] = None):
    
    new_address = Address(
        user_id=current_user.id,
        address=request.address,
        detailed_address=request.detailed_address,
        receiver_name=request.receiver_name,
        phone=request.phone,
        is_default=request.is_default
    )
    db.add(new_address)
    await db.commit()
    await db.refresh(new_address)
    
    return new_address

async def update_address(db: AsyncSession, current_user: User, request: Optional[CreateAddressDto] = None):
    address = await db.execute(
        select(Address)
        .options(selectinload(Address.user))
        .where(Address.user_id == current_user.id)
        .where(Address.id == request.id)
    )
    address = address.scalar_one_or_none()

    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")

    
    for key, value in request:
        if value is not None:
            setattr(address, key, value)
    
    await db.commit()
    await db.refresh(address)
    
    return address


async def my_address(db: AsyncSession, current_user: User, request: Optional[RequestMyAddressDto]):
    
    address = await db.execute(
        select(Address)
        .options(selectinload(Address.user))
        .where(Address.user_id == current_user.id)
        .where(Address.id == request.id)
    )
    
    address = address.scalar_one_or_none()

    if address is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address

async def my_address_list(db: AsyncSession, current_user: User):
    
    address = await db.execute(
        select(Address)
        .options(selectinload(Address.user))
        .where(Address.user_id == current_user.id)
    )
    
    address_list = address.scalars()
    
    if address_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    
    else:
        addresses = [address for address in address_list]
    
    return addresses