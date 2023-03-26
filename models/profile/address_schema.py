from typing import Optional
from pydantic import BaseModel

from models.profile.base_schema import AddressBaseDto
from models.profile.profile_model import Profile



class CreateAddressDto(AddressBaseDto):
    pass


class AddressDisplayDto(AddressBaseDto):
    
    class Config:
        orm_mode = True
