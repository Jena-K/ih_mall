from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base

# from modules.product.domain.material import Material
from sqlalchemy.orm import relationship

class KeywordProduct(Base):
    __tablename__ = 'keyword_product'

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey('keyword_table.id'))
    product_id = Column(Integer, ForeignKey('product_table.id'))
    keyword = relationship('Keyword', back_populates='products')
    product = relationship('Product', back_populates='keywords')

class Keyword(Base):
    __tablename__ = 'keyword_table'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    products = relationship('KeywordProduct', back_populates='keyword')

