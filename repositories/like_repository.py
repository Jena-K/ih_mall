from profile import Profile
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator
from models.product.like_model import ProductLike, CreatorLike
from models.product.like_schema import ToggleLikeDto
from models.product.material_model import Material
from models.product.option_model import Option
from models.product.product_model import Product
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.expression import delete


async def toggle_product_like(
    db: AsyncSession,
    current_user: User = Depends(current_active_user),
    request: Optional[ToggleLikeDto] = None,
) -> ProductLike:
    if not request or not request.product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    # Get the product to be liked or unliked
    product = (
        await db.execute(
            select(Product)
            .where(Product.id == request.product_id)
        )
    ).scalar()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Delete if there is an existing like, otherwise create a new one
    existing_like = (
        await db.execute(
            select(ProductLike)
            .where(ProductLike.product_id == product.id)
            .where(ProductLike.user_id == current_user.id)
        )
    ).scalar()

    if existing_like:
        await db.execute(
            delete(ProductLike)
            .where(ProductLike.product_id == product.id)
            .where(ProductLike.user_id == current_user.id)
        )
        await db.commit()
        return f"Like for {product.name} has been canceled"

    new_like = ProductLike(user_id=current_user.id, product_id=product.id)
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like)
    return f"Like for {product.name} has been registered"


async def toggle_creator_like(
    db: AsyncSession,
    current_user: User = Depends(current_active_user),
    request: Optional[ToggleLikeDto] = None,
) -> CreatorLike:
    if not request or not request.creator_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")

    # Get the creator to be liked or unliked
    creator = (
        await db.execute(select(Creator).where(Creator.id == request.creator_id))
    ).scalar()

    if not creator:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")

    # Delete if there is an existing like, otherwise create a new one
    existing_like = (
        await db.execute(
            select(CreatorLike)
            .where(CreatorLike.creator_id == creator.id)
            .where(CreatorLike.user_id == current_user.id)
        )
    ).scalar()

    if existing_like:
        await db.execute(
            delete(CreatorLike)
            .where(CreatorLike.creator_id == creator.id)
            .where(CreatorLike.user_id == current_user.id)
        )
        await db.commit()
        return f"Like for {creator.nickname} canceled"

    new_like = CreatorLike(user_id=current_user.id, creator_id=creator.id)
    db.add(new_like)
    await db.commit()
    await db.refresh(new_like)
    return f"Like for {creator.nickname} registered"
