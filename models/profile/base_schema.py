from typing import Optional
from pydantic import BaseModel


class ProfileBaseDto(BaseModel):
    
    class Config:
        orm_mode = True


class AddressBaseDto(BaseModel):
    id: Optional[int]
    address: str
    detailed_address: str
    receiver_name: str
    phone: str
    is_default: Optional[bool]

    class Config:
        orm_mode = True
