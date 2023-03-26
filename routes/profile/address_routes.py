from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import get_db
from models.profile.address_schema import AddressDisplayDto, CreateAddressDto
from repositories import address_repository

router = APIRouter(prefix="/address", tags=["user"])

# User Registration
@router.post("/")
def create_address(request: CreateAddressDto, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return address_repository.create_address(db, request, current_user)


# User Query (One)
@router.get("/{id}", response_model=AddressDisplayDto)
def get_address(
    id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    return address_repository.get_address(db, id, current_user)
