from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base

# from modules.product.domain.material import Material
from sqlalchemy.orm import relationship

keyword_product = Table(
    "keyword_product",
    Base.metadata,
    Column("keyword_id", Integer, ForeignKey("keyword_table.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("product_table.id"), primary_key=True),
)

class Keyword(Base):
    __tablename__ = 'keyword_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    products = relationship("Product", secondary=keyword_product, back_populates="keywords")

