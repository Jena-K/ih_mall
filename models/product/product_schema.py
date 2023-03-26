from typing import Optional
from pydantic import BaseModel, validator
from enum import Enum
from models.enums import ProductStatus

class CreateProduct(BaseModel):
    category_id: int
    creator_id: int
    name: str
    description: str
    price: int
    discounted_price: int
    stock: int
    material_id: Optional[int]
    is_handmade: bool
    is_recommanded: bool


class ResponseCreateProduct(BaseModel):
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
    