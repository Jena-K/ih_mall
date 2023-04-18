
from typing import List
from pydantic import BaseModel, Field


class OptionDTO(BaseModel):
    option_id: int
    cnt: int = Field(title='옵션 수량')


class ItemDTO(BaseModel):
    product_id: int
    option_id: int
    cnt: int


class CreateCartDto(BaseModel):
    product_id: int
    options: List[OptionDTO]


class ResponseItemDTO(BaseModel):
    id: int
    product_id: int
    option_ids: List[int]
    cnt: int


class ResponseCartDTO(BaseModel):
    id: int
    product_id: int
    option_id: int
    cnt: int


class DeleteCartDto(BaseModel):
    ids: List[int]


class UpdateCartDTO(BaseModel):
    id: int
    cnt: int


class SimpleCartItemDto(BaseModel):
    id: int
    name: str
    price: int
    option_id: int
    option_name: str
    cnt: int


class ResponseCartListDTO(BaseModel):
    # creator_id: int
    nickname: str
    items: List[SimpleCartItemDto]

