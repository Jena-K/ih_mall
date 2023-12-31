from typing import Optional
from pydantic import BaseModel, Field


class CreateCreatorDto(BaseModel):
    nickname: str = Field(title="작가 닉네임")
    phone: str = Field(title="작가 전화번호")
    businessNumber: str = Field(title="사업자 번호")
    businessName: str = Field(title="사업자 이름")
    representative: str = Field(title="대표자 명")
    representativeType: str = Field(title="대표자 유형")
    businessRegistrationCertification: str = Field(title="사업자 등록증")
    address: str = Field(title="작가 주소")
    sns: str = Field(title="작가 sns")
    picture_url: Optional[str]


class CreateResponseCreatorDto(BaseModel):
    id: int
    user_id: int = Field(title="연동 유저 ID")
    nickname: str = Field(title="작가 닉네임")
    phone: str = Field(title="작가 전화번호")
    businessNumber: str = Field(title="사업자 번호")
    businessName: str = Field(title="사업자 이름")
    representative: str = Field(title="대표자 명")
    representativeType: str = Field(title="대표자 유형")
    businessRegistrationCertification: str = Field(title="사업자 등록증")
    address: str = Field(title="작가 주소")
    sns: str = Field(title="작가 sns")
    is_certified: bool
    picture_url: Optional[str]

    class Config:
        orm_mode = True


class UpdateCreatorDto(BaseModel):
    nickname: Optional[str] = Field(title="작가 닉네임")
    phone: Optional[str] = Field(title="작가 전화번호")
    businessNumber: Optional[str] = Field(title="사업자 번호")
    businessName: Optional[str] = Field(title="사업자 이름")
    representative: Optional[str] = Field(title="대표자 명")
    representativeType: Optional[str] = Field(title="대표자 유형")
    businessRegistrationCertification: Optional[str] = Field(title="사업자 등록증")
    address: Optional[str] = Field(title="작가 주소")
    sns: Optional[str] = Field(title="작가 sns")
    picture_url: Optional[str]


class GetCreatorDto(BaseModel):
    id: int


class SimpleCreatorDTO(BaseModel):
    id: int
    nickname: str
