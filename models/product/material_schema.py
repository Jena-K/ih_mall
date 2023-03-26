from typing import List, Optional
from pydantic import BaseModel

class CreateMaterial(BaseModel):
    creator_id: int
    name: str
    material: str
    coating: str
    size: str
    origin: str
    caution: str

class ResponseCreateMaterial(BaseModel):
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
