import enum


class RoleType(enum.Enum):
    member = "member"
    creator = "creator"
    admin = "admin"

class ProductStatus(enum.Enum):
    pending= "심사대기"
    rejected = "심사거절"
    on_sale = "판매중"
    sold_out = "품절"
    closed = "판매중단"
    deleted= "삭제"