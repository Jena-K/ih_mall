from typing import List, Optional
from models.profile.base_schema import ProfileBaseDto
from pydantic import BaseModel


class RegisterProfileDto(ProfileBaseDto):
    phone: str
    name: str
    picture_url: Optional[str]


class ResponseRegisterProfileDto(BaseModel):
    email: Optional[str]
    phone: Optional[str]
    provider: Optional[str]
    picture_url: Optional[str]

    class Config:
        orm_mode = True


class UpdateProfileDto(BaseModel):
    phone: Optional[str]
    name: Optional[str]
    picture_url: Optional[str]


# AddressDto for User Display
class AddressDto(BaseModel):
    address: str
    detailed_address: str
    receiver_name: str
    phone: str
    is_default: bool

    class Config:
        orm_mode = True


class ProfileDisplayDto(ProfileBaseDto):
    phone: Optional[str]
    name: Optional[str]
    # address: List[AddressDto]

    class Config:
        orm_mode = True


class LoginProfileDto(ProfileBaseDto):
    password: str


class UserAuth(BaseModel):
    id: int
    name: str
    email: str