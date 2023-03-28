from typing import Optional
from pydantic import BaseModel, validator
from enum import Enum
from models.enums import ProductStatus

class CreateProductDto(BaseModel):
    category_id: int
    name: str
    description: str
    price: int
    discounted_price: int
    stock: Optional[int]
    material_id: Optional[int]
    is_handmade: Optional[bool]


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
    material_id: Optional[int]
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