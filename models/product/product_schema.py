from typing import Optional, List
from pydantic import BaseModel, validator
from enum import Enum
from models.enums import ProductStatus
from models.product.material_model import Material
from models.product.product_model import Product


class OptionDtoForCreateProductDto(BaseModel):
    name: str
    added_price: int
    stock: int


class KeywordDtoForCreateProductDto(BaseModel):
    name: str


class CreateProductDto(BaseModel):
    category_id: int
    name: str
    description: str
    price: int
    discounted_price: int
    stock: Optional[int]
    material_id: Optional[int]
    product_images: Optional[List[int]]
    is_handmade: Optional[bool]
    options: Optional[List[OptionDtoForCreateProductDto]]
    keywords: Optional[List[KeywordDtoForCreateProductDto]]


class ProductImageDto(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]

    class Config:
        orm_mode = True


class OptionDto(BaseModel):
    id: int
    name: Optional[str]
    added_price: Optional[int]
    stock: Optional[int]
    product_id: Optional[int]

    class Config:
        orm_mode = True


class MaterialDto(BaseModel):
    creator_id: Optional[int]
    name: Optional[str]
    material: Optional[str]
    coating: Optional[str]
    size: Optional[str]
    origin: Optional[str]
    caution: Optional[str]

    class Config:
        orm_mode = True


class ResponseCreateProductDto(BaseModel):
    id: int
    category_id: int
    creator_id: int
    name: str
    description: str
    status: ProductStatus
    price: int
    discounted_price: int
    stock: int
    ordering_number: int
    is_handmade: bool
    is_recommanded: bool

    class Config:
        orm_mode = True


class UpdateProductDto(BaseModel):
    id: int
    category_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    discounted_price: Optional[int]
    stock: Optional[int]
    material_id: Optional[int]
    is_handmade: Optional[bool]