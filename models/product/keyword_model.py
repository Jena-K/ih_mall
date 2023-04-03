from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base

# from modules.product.domain.material import Material
from sqlalchemy.orm import relationship

class Keyword(Base):
    __tablename__ = 'keyword_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    product_id = Column(Integer, ForeignKey("product_table.id"))
    products = relationship("Product", back_populates="keywords")