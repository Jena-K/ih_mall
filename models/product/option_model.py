import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, Enum
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.orm import relationship

class Option(Base):
    __tablename__ = 'option_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    added_price = Column(Integer)
    stock = Column(Integer)
    product_id = Column(Integer, ForeignKey("product_table.id"))
    product = relationship("Product", back_populates="options")
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