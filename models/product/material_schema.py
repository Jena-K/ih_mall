from typing import List, Optional
from pydantic import BaseModel

class CreateMaterialDto(BaseModel):
    name: str
    material: str
    coating: str
    size: str
    origin: str
    caution: str

class ResponseCreateMaterialDto(BaseModel):
    id: int
    creator_id: int
    name: str
    material: str
    coating: str
    size: str
    origin: str
    caution: str

    class Config:
        orm_mode = True

class UpdateMaterialDto(BaseModel):
    id: int
    name: Optional[str]
    material: Optional[str]
    coating: Optional[str]
    size: Optional[str]
    origin: Optional[str]
    caution: Optional[str]