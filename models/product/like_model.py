from sqlalchemy import Column, Table
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base

# from modules.product.domain.material import Material
from sqlalchemy.orm import relationship

class Like(Base):
    __tablename__ = 'like_table'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_table.id'))
    product_id = Column(Integer, ForeignKey('product_table.id'))
    creator_id = Column(Integer, ForeignKey('creator_table.id'))
    user = relationship('KeywordProduct', back_populates='users')
    product = relationship('KeywordProduct', back_populates='likes')
    creator = relationship('KeywordProduct', back_populates='creators')

