import sqlalchemy
from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, Enum
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from models.creator.creator_model import Creator
from models.enums import ProductStatus
from models.product.category_model import Category
# from modules.product.domain.material import Material
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "product_table"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("category_table.id"))
    category = relationship("Category", back_populates="products")
    creator_id = Column(Integer, ForeignKey("creator_table.id"))
    creator = relationship("Creator", back_populates="products")
    name = Column(String)
    description = Column(String)
    status = Column(Enum(ProductStatus), nullable=False, server_default=ProductStatus.pending.name)
    price = Column(Integer)
    discounted_price = Column(Integer)
    stock = Column(Integer, default=0)
    ordering_number = Column(Integer)
    material_id = Column(Integer, ForeignKey("material_table.id"))
    material = relationship("Material", back_populates="products")
    options = relationship("Option", back_populates="product")
    product_images = relationship("ProductImage", back_populates="product")
    is_handmade = Column(Boolean, default=False)
    is_recommanded = Column(Boolean, default=False)
    keywords = relationship('KeywordProduct', back_populates='product')
    likes = relationship('ProductLike', back_populates='product')
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
