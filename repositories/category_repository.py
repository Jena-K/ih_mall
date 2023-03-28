from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User
from auth.users import current_active_user
from models.product.category_model import Category
from models.product.category_schema import CreateCategoryDto, GetCategoryDto, UpdateCategoryDto

from sqlalchemy.orm import selectinload
async def create_category(db: AsyncSession, current_user: User, request: Optional[CreateCategoryDto] = None):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    new_category = Category(
        name=request.name,
        url=request.url
    )

    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category

# 카테고리 업데이트
async def update_category(db: AsyncSession, current_user: User, request: UpdateCategoryDto):

    if current_user.is_superuser is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unauthorized")

    category = await db.execute(
        select(Category)
        .where(Category.id == request.id)
    )
    category = category.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    
    await db.commit()
    await db.refresh(category)
    
    return category

# Get Single Cateogry
async def get_category(db: AsyncSession, request: GetCategoryDto):

    category = await db.execute(
        select(Category)
        .where(Category.id == request.id)
    )
    
    category = category.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

# Get Cateogry List
async def get_category_list(db: AsyncSession):
    
    category = await db.execute(
        select(Category)
    )
    
    category_list = category.scalars()
    
    if category_list is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    else:
        categories = [category for category in category_list]
    
    return categories