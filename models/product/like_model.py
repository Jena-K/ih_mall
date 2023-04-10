from sqlalchemy import Column, Table
from sqlalchemy.schema import ForeignKey
from infrastructure.database import Base
from sqlalchemy.sql.sqltypes import UUID, Integer, String

# from modules.product.domain.material import Material
from sqlalchemy.orm import relationship

class ProductLike(Base):
    __tablename__ = 'product_like_table'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", backref="productlike", primaryjoin="User.id == ProductLike.user_id")
    product_id = Column(Integer, ForeignKey("product_table.id"))
    product = relationship("Product", back_populates="likes")


class CreatorLike(Base):
    __tablename__ = 'creator_like_table'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID, ForeignKey("user.id"))
    user = relationship("User", backref="creatorlike", primaryjoin="User.id == CreatorLike.user_id")
    creator_id = Column(Integer, ForeignKey("creator_table.id"))
    creator = relationship("Creator", back_populates="likes")