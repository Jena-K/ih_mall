from typing import Optional
from pydantic import BaseModel

from models.user.base_schema import AddressBaseDto, UserBaseDto
from models.user.user_model import User


# UserDto for Address
class UserDto(BaseModel):
    name: str
    phone: Optional[str]
    email: str

    class Config:
        orm_mode = True


class CreateAddressDto(AddressBaseDto):
    user = UserDto


class AddressDisplayDto(AddressBaseDto):
    user: UserDto

    class Config:
        orm_mode = True
