from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from infrastructure.database import User, get_async_session
from models.product.product_schema import CreateProductDto, ResponseCreateProductDto, UpdateProductDto
from repositories import product_repository
from auth.users import current_active_user

router = APIRouter(prefix="/product", tags=["product"])

# Create Product
@router.post("/", response_model=ResponseCreateProductDto)
async def create_product(request: CreateProductDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    product = await product_repository.create_product(db, current_user, request)
    return product

# Update Product
@router.patch("/update", response_model=ResponseCreateProductDto)
async def create_category(request: UpdateProductDto, db: Session = Depends(get_async_session), current_user: User = Depends(current_active_user)):
    product = await product_repository.update_product(db, current_user, request)
    return product

# Get Product
@router.get("/", response_model=ResponseCreateProductDto)
async def update_address(request: UpdateProductDto, db: Session = Depends(get_async_session)):
    product = await product_repository.get_product(db, request)
    return product

# # Get Product List
@router.get("/product_all", response_model=List[ResponseCreateProductDto])
async def update_address(db: Session = Depends(get_async_session)):
    products = await product_repository.get_products(db)
    return products