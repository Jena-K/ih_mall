from typing import Optional
from pydantic import BaseModel, Field


class CreateBankInformationDto(BaseModel):
    bank_name: str = Field(title="은행명")
    account_holder_name: str = Field(title="계좌주명")
    account_number: str = Field(title="계좌번호")
    is_issue_cash_receipt: bool


class CreateResponseBankInformationDto(BaseModel):
    id: int
    bank_name: str = Field(title="은행명")
    account_holder_name: str = Field(title="계좌주명")
    account_number: str = Field(title="계좌번호")
    is_issue_cash_receipt: bool

    class Config:
        orm_mode = True


class UpdateBankInformationDto(BaseModel):
    bank_name: Optional[str] = Field(title="은행명")
    account_holder_name: Optional[str] = Field(title="계좌주명")
    account_number: Optional[str] = Field(title="계좌번호")
    is_issue_cash_receipt: Optional[bool]