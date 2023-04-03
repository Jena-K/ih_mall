from profile import Profile
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator
from models.product.option_model import Option
from sqlalchemy.orm import selectinload
from models.product.option_schema import CreateOptionDto, UpdateOptionDto

async def create_option(db: AsyncSession, current_user: User, request: Optional[CreateOptionDto] = None):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")
    
    new_option = Option(
        name=request.name,
        added_price=request.added_price,
        stock=request.stock,
        product_id=request.product_id
    )
    db.add(new_option)
    await db.commit()
    await db.refresh(new_option)
    
    return new_option

# Update Option
async def update_option(db: AsyncSession, current_user: User, request: Optional[UpdateOptionDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")


    option = await db.execute(
        select(Option)
        .where(Option.id == request.id)
    )
    option = option.scalar_one_or_none()

    if option is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Option not found")

    for key, value in request:
        if value is not None:
            setattr(option, key, value)
    
    await db.commit()
    await db.refresh(option)
    
    return option

# Get Option (Single)
async def get_option(db: AsyncSession, request: Optional[UpdateOptionDto]):

    option = await db.execute(
        select(Option)
        .where(Option.id == request.id)
    )

    option = option.scalar_one_or_none()


    if option is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Option not found")
    return option


# Get Options (List)
async def get_options(db: AsyncSession):
    
    options = await db.execute(
        select(Option)
    )
    
    options = options.scalars()
    
    if options is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Option list not found")
    
    else:
        options = [option for option in options]
    
    return options