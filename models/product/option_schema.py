from typing import Optional, List
from pydantic import BaseModel, validator

class CreateOptionDto(BaseModel):
    name: str
    added_price: int
    stock: int
    product_id: int


class ResponseCreateOptionDto(BaseModel):
    id: int
    name: str
    added_price: int
    stock: int
    product_id: int

    class Config:
        orm_mode = True


class UpdateOptionDto(BaseModel):
    id: int
    name: Optional[str]
    added_price: Optional[int]
    stock: Optional[int]
    product_id: Optional[int]