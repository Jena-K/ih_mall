from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator, DeliveryPolicy
from models.creator.delivery_policy_schema import CreateDeliveryPolicyDto, GetDeliveryPolicyDto, UpdateDeliveryPolicyDto
from sqlalchemy.orm import selectinload

async def create_delivery_policy(db: AsyncSession, current_user: User, request: Optional[CreateDeliveryPolicyDto] = None):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    new_bank_information= DeliveryPolicy(
        creator_id=creator.id,
        vendor = request.vendor,
        primary_fee = request.primary_fee,
        is_semi_registered = request.is_semi_registered,
        advanced_fee = request.advanced_fee,
        free_shipping_amt = request.free_shipping_amt,
        est_departure = request.est_departure,
        refund_policy = request.refund_policy
    )
    db.add(new_bank_information)
    await db.commit()
    await db.refresh(new_bank_information)
    
    return new_bank_information


async def update_delivery_policy(db: AsyncSession, current_user: User, request: Optional[UpdateDeliveryPolicyDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")


    delivery_policy = await db.execute(
        select(DeliveryPolicy)
        .options(selectinload(DeliveryPolicy.creator))
        .where(DeliveryPolicy.creator_id == creator.id)
    )
    delivery_policy = delivery_policy.scalar_one_or_none()

    if delivery_policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery policy not found")

    for key, value in request:
        if value is not None:
            setattr(delivery_policy, key, value)
    
    await db.commit()
    await db.refresh(delivery_policy)
    
    return delivery_policy

# Get Material (Single)
async def get_delivery_policy(db: AsyncSession, current_user: User):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    delivery_policy = await db.execute(
        select(DeliveryPolicy)
        .where(DeliveryPolicy.creator_id == creator.id)
    )

    delivery_policy = delivery_policy.scalar_one_or_none()


    if delivery_policy is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Delivery policy not found")
    return delivery_policy
