from typing import Optional
from pydantic import BaseModel, Field


class CreateDeliveryPolicyDto(BaseModel):
    vendor: str = Field(title="배송업체명")
    primary_fee: str = Field(title="배송요금")
    is_semi_registered: bool = Field(title="준등기")
    advanced_fee: int = Field(title="추가요금")
    free_shipping_amt: int = Field(title="무료배송 주문액")
    est_departure: str = Field(title="배송 소요일자")
    refund_policy: str = Field(title="환불규정")
    


class CreateResponseDeliveryPolicyDto(BaseModel):
    id: int
    vendor: str = Field(title="배송업체명")
    primary_fee: str = Field(title="배송요금")
    is_semi_registered: bool = Field(title="준등기")
    advanced_fee: int = Field(title="추가요금")
    free_shipping_amt: int = Field(title="무료배송 주문액")
    est_departure: str = Field(title="배송 소요일자")
    refund_policy: str = Field(title="환불규정")

    class Config:
        orm_mode = True


class UpdateDeliveryPolicyDto(BaseModel):
    vendor: Optional[str] = Field(title="배송업체명")
    primary_fee: Optional[str] = Field(title="배송요금")
    is_semi_registered: Optional[bool] = Field(title="준등기")
    advanced_fee: Optional[int] = Field(title="추가요금")
    free_shipping_amt: Optional[int] = Field(title="무료배송 주문액")
    est_departure: Optional[str] = Field(title="배송 소요일자")
    refund_policy: Optional[str] = Field(title="환불규정")


class GetDeliveryPolicyDto(BaseModel):
    id: int