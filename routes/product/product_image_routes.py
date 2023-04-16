from typing import List
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.product_image_schema import CreateProductImageDto, ResponseCreateProductImageDto, UpdateProductImageDto
from repositories import product_image_repository
from auth.users import current_active_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/product_image", tags=["product_image"])

# Create Product
@router.post("/", response_model=ResponseCreateProductImageDto)
async def create_product_image(
    image: CreateProductImageDto = Depends(),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_active_user),
):
    product_image = await product_image_repository.create_product_images(db, current_user, image)
    return product_image

# Update Product
# @router.patch("/", response_model=ResponseCreateProductImageDto)
# async def update_product_image(request: UpdateProductImageDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
#     product_image = await product_image_repository.update_product_image(db, current_user, request)
#     return product_image

# # Get Product
# @router.get("/", response_model=ResponseCreateProductImageDto)
# async def get_image(request: UpdateProductImageDto, db: Session = Depends(get_async_session)):
#     product_image = await product_image_repository.get_product_image(db, request)
#     return product_image

# Get Product List
# @router.get("/product_images_all", response_model=List[ResponseCreateProductImageDto])
# async def update_address(db: Session = Depends(get_async_session)):
#     product_images = await product_image_repository.get_product_images(db)
#     return product_images