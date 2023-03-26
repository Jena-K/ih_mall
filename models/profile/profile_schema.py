from typing import List, Optional
from models.user.base_schema import UserBaseDto
from pydantic import BaseModel


class RegisterUserDto(UserBaseDto):
    password: str
    phone: str
    name: str


class ResponseRegisterUserDto(BaseModel):
    email: Optional[str]
    provider: Optional[str]

    class Config:
        orm_mode = True


class UpdateUserDto(BaseModel):
    email: Optional[str]
    provider: Optional[str]
    password: Optional[str]
    phone: Optional[str]
    name: Optional[str]


# AddressDto for User Display
class AddressDto(BaseModel):
    address: str
    detailed_address: str
    receiver_name: str
    phone: str
    is_default: bool

    class Config:
        orm_mode = True


class UserDisplayDto(UserBaseDto):
    phone: Optional[str]
    name: str
    address: List[AddressDto]

    class Config:
        orm_mode = True


class LoginUserDto(UserBaseDto):
    password: str


class UserAuth(BaseModel):
    id: int
    name: str
    email: str