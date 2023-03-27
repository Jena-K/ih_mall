from typing import List, Optional
from pydantic import BaseModel

class CreateCategoryDto(BaseModel):
    name: str
    url: str

class ResponseCreateCategoryDto(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True

class UpdateCategoryDto(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]

class GetCategoryDto(BaseModel):
    id: int