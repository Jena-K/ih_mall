from typing import Optional
from pydantic import BaseModel


class ProfileBaseDto(BaseModel):
    
    class Config:
        orm_mode = True


class AddressBaseDto(BaseModel):
    address: str
    detailed_address: str
    receiver_name: str
    phone: str
    is_default: Optional[bool]