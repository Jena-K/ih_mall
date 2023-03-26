from typing import Optional
from pydantic import BaseModel

from models.profile.base_schema import AddressBaseDto, UserBaseDto
from models.profile.profile_model import User


# UserDto for Address
class UserDto(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    user_id: Optional[str]

    class Config:
        orm_mode = True


class CreateAddressDto(AddressBaseDto):
    user = UserDto


class AddressDisplayDto(AddressBaseDto):
    user: UserDto

    class Config:
        orm_mode = True
