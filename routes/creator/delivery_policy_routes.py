from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.creator.delivery_policy_schema import CreateDeliveryPolicyDto, CreateResponseDeliveryPolicyDto, GetDeliveryPolicyDto, UpdateDeliveryPolicyDto

from repositories import delivery_policy_repository
from auth.users import current_active_user

router = APIRouter(prefix="/delivery_policy", tags=["delivery_policy"])

# Delivery Policy Registration
@router.post("/", response_model=CreateResponseDeliveryPolicyDto)
async def create_delivery_policy(request: CreateDeliveryPolicyDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    delivery_policy = await delivery_policy_repository.create_delivery_policy(db, current_user, request)
    return delivery_policy

# Delivery Policy Update
@router.patch("/", response_model=CreateResponseDeliveryPolicyDto)
async def update_delivery_policy(request: UpdateDeliveryPolicyDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    delivery_policy = await delivery_policy_repository.update_delivery_policy(db, current_user, request)
    return delivery_policy

# 배송정보 조회 (Single)
@router.get("/", response_model=CreateResponseDeliveryPolicyDto)
async def get_delivery_policy(db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    delivery_policy = await delivery_policy_repository.get_delivery_policy(db, current_user)
    return delivery_policy