from profile import Profile
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import User, get_user_db
from auth.users import current_active_user
from models.creator.creator_model import Creator
from models.product.material_model import Material
from models.product.option_model import Option
from models.product.product_model import Product
from sqlalchemy.orm import selectinload, joinedload
from models.product.product_schema import CreateProductDto, OptionDto, ProductImageDto, ResponseCreateProductDto, UpdateProductDto


async def create_product(db: AsyncSession, current_user: User, request: Optional[CreateProductDto] = None):
    
    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()
    
    try:
        products = await db.execute(
            select(Product)
            .options(selectinload(Product.creator))
            .where(Product.creator_id == creator.id)
        )
        products = products.scalars()
        products = [product for product in products]
    except:
        products = 0
    
    new_product = Product(
        category_id=request.category_id,
        creator_id=creator.id,
        name=request.name,
        description=request.description,
        price=request.price,
        discounted_price=request.discounted_price,
        stock=request.stock,
        ordering_number=len(products)+1,
        material_id=request.material_id,
        is_handmade=request.is_handmade,
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    try:
        new_product.material_id = request.material_id
        await db.commit()
    except:
        return new_product
    
    return new_product

# Update Product
async def update_product(db: AsyncSession, current_user: User, request: Optional[UpdateProductDto] = None):

    creator = await db.execute(
        select(Creator)
        .options(selectinload(Creator.user))
        .where(Creator.user_id == current_user.id)
    )

    creator = creator.scalar_one_or_none()

    if creator.user_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Authorized")

    product = await db.execute(
        select(Product)
        .options(selectinload(Product.creator))
        .where(Product.creator_id == creator.id)
        .where(Product.id == request.id)
    )
    product = product.scalar_one_or_none()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    for key, value in request:
        if value is not None:
            setattr(product, key, value)
    
    await db.commit()
    await db.refresh(product)
    
    return product

# Get Product (Single)
async def get_product(db: AsyncSession, request: Optional[UpdateProductDto]):
    query = select(Product).where(Product.id == request.id)
    result = await db.execute(query)
    product = result.scalars().first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    

    return product


# Get Product (List)
async def get_products(db: AsyncSession):
    
    products = await db.execute(
        select(Product)
    )
    
    products = products.scalars()
    
    if products is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product list not found")
    
    else:
        products = [product for product in products]
    
    return products