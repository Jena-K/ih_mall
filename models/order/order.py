import sqlalchemy
from sqlalchemy import UUID, Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.orm import relationship


class OrderItem(Base):
    __tablename__ = "order_item_table"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", backref="creator", primaryjoin="User.id == Creator.user_id")
    product_id = Column(Integer, ForeignKey("product_table.id"), nullable=False)
    product = relationship("Product", backref="Products")
    option_id = Column(Integer, ForeignKey("option_table.id"))
    option = relationship("Option", backref="Options")
    order_id = Column(Integer, ForeignKey("order_table.id"), nullable=False)
    order = relationship("Order", back_populates="order_items")
    cnt = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
    )
    updated_at = Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )

class Order(Base):
    __tablename__ = "order_table"
    id = Column(Integer, primary_key=True, index=True)
    order_items = relationship("OrderItem", back_populates="order")
    address = Column(String)
    detailed_address = Column(String)
    receiver_name = Column(String)
    phone = Column(String)
    payment_method = Column(String)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
    )
    updated_at = Column(
        sqlalchemy.DateTime,
        nullable=False,
        server_default=sqlalchemy.func.now(),
        onupdate=sqlalchemy.func.now(),
    )

    