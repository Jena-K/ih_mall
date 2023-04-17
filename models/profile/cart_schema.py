
from typing import List
from pydantic import BaseModel


class OptionDTO(BaseModel):
    option_id: int
    cnt: int

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


class ResponseCartDto(BaseModel):
    id: int
    items: List[ResponseItemDTO]

    class Config:
        orm_mode = True


class ResponseCartListDTO(BaseModel):
    # creator_id: int
    creator_nickname: str
    items: List[ResponseItemDTO]


class DeleteCartDto(BaseModel):
    ids: List[int]


class UpdateCartDTO(BaseModel):
    id: int
    cnt: int
