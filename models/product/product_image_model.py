import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.orm import relationship

class ProductImage(Base):
    __tablename__ = "product_image_table"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product_table.id"))
    product = relationship("Product", back_populates="product_images")
    url = Column(String)