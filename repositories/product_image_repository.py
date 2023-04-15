from profile import Profile
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator
from models.product.product_image_model import ProductImage
from sqlalchemy.orm import selectinload
from models.product.product_image_schema import CreateProductImageDto, UpdateProductImageDto

async def create_product_image(db: AsyncSession, current_user: User, request: Optional[CreateProductImageDto] = None):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()
    

    product_images = await db.execute(
        select(ProductImage)
        .options(selectinload(ProductImage.creator))
        .where(ProductImage.creator_id == creator.id)
    )

    product_images = product_images.scalars()
    product_images = [product_image for product_image in product_images]
    

    new_product_image = ProductImage(
        
    )
    db.add(new_product_image)
    await db.commit()
    await db.refresh(new_product_image)
    
    return new_product_image

# Update product_image
async def update_product_image(db: AsyncSession, current_user: User, request: Optional[UpdateProductImageDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")


    product_image = await db.execute(
        select(ProductImage)
        .options(selectinload(ProductImage.creator))
        .where(ProductImage.creator_id == creator.id)
        .where(ProductImage.id == request.id)
    )
    product_image = product_image.scalar_one_or_none()

    if product_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product image not found")

    for key, value in request:
        if value is not None:
            setattr(product_image, key, value)
    
    await db.commit()
    await db.refresh(product_image)
    
    return product_image

# Get product_image (Single)
async def get_product_image(db: AsyncSession, request: Optional[UpdateProductImageDto]):

    product_image = await db.execute(
        select(ProductImage)
        .where(ProductImage.id == request.id)
    )

    product_image = product_image.scalar_one_or_none()


    if product_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product_image not found")
    return product_image


# Get product_image (List)
async def get_product_images(db: AsyncSession):
    
    product_images = await db.execute(
        select(ProductImage)
    )
    ]
    product_images = product_images.scalars()
    
    if product_images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product_image list not found")
    
    else:
        product_images = [product_image for product_image in product_images]
    
    return product_images