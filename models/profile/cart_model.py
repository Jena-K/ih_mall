

from sqlalchemy import Column, UUID
from sqlalchemy.sql.sqltypes import Integer
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.orm import relationship


class Cart(Base):
    __tablename__ = "cart_table"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref="Users")
    product_id = Column(Integer, ForeignKey("product_table.id"), nullable=False)
    product = relationship("Product", backref="Products")
    option_id = Column(Integer, ForeignKey("option_table.id"))
    option = relationship("Option", backref="Options")
    cnt = Column(Integer, nullable=False)


