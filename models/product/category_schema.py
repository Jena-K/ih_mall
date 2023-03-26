from typing import List, Optional
from pydantic import BaseModel

class CreateCategory(BaseModel):
    name: str
    url: str

class ResponseCreateCategory(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


class UpdateUserDto(BaseModel):
    password: Optional[str]
    phone: Optional[str]
    name: Optional[str]
