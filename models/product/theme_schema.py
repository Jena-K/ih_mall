from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class CreateThemeProductDto(BaseModel):
    product_id: int
    theme_id: int


class ResponseCreateThemeProductDto(BaseModel):
    id: int
    product_id: int
    theme_id: int

    class Config:
        orm_mode = True


class ThemeProductIdDto(BaseModel):
    id: int


class CreateThemeDto(BaseModel):
    name: Optional[str]
    start_at: date
    end_at: date


class ResponseCreateThemeDto(BaseModel):
    id: int
    name: str
    start_at: date
    end_at: date

    class Config:
        orm_mode = True


class UpdateThemeDto(BaseModel):
    id: int
    name: Optional[str]
    start_at: Optional[date]
    end_at: Optional[date]


class GetThemeDto(BaseModel):
    id: int


